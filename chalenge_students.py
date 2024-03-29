import os.path
import math

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
  # the spreadsheet ID can be found in the URL of the document
  spreadsheetId = "10FdFjl30y7ZI6DQ7so1MTQzf8sIXUptUPLGwPzbOjoU"

  # read then values from the Google spreadsheet
  try:
    spreadsheet_values = getData(spreadsheetId,"A2:F27")
  except UnboundLocalError as err:
    print("The spreadsheet could not be accessed.")
    return
  
  # find the total number of classes
  total_classes = int(spreadsheet_values[0][0].split()[-1])

  # iterates over the students rows
  for i in range(2, len(spreadsheet_values)):
    reg_number = spreadsheet_values[i][0]
    name = spreadsheet_values[i][1]
    num_absences = int(spreadsheet_values[i][2])

    # row LOG
    print(f"\n LOG: {spreadsheet_values[i]}")

    # average grande between the 3 tests in a scale from 0 to 10
    avg = (int(spreadsheet_values[i][3])+int(spreadsheet_values[i][4])+int(spreadsheet_values[i][5]))/30
    print(f" avg -> {str(avg)}")
    
    # verify the situation of the student
    if(num_absences/total_classes > 0.25):
      spreadsheet_values[i].append("Reprovado por Falta")
      spreadsheet_values[i].append("0")
      print(" situation -> Reprovado por Falta")
    elif(avg<5):
      spreadsheet_values[i].append("Reprovado por Nota")
      spreadsheet_values[i].append("0")
      print(" situation ->Reprovado por Nota")
    elif(avg>=7):
      spreadsheet_values[i].append("Aprovado")
      spreadsheet_values[i].append("0")
      print(" situation -> Aprovado")
    elif(avg>=5 and avg<7):
      spreadsheet_values[i].append("Exame Final")
      print(" situation -> Exame Final ", end="")
      # calculate the minimun grade for approval in the final exam
      naf = math.ceil(10-avg)
      spreadsheet_values[i].append(naf)
      print(f"(naf -> {naf})")
    else:
      spreadsheet_values[i].append("ERROR!")

  results_list = [row[6:] for row in spreadsheet_values[2:]]

  # write the results in the Google spreadsheet
  update_values(
      spreadsheetId,
      "G4:H27",
      "USER_ENTERED",
      results_list
  )



def getData(spreadsheetId: str, range: str):
  """
    Uses the Google API to get the values from the spreadsheet.
  """

  # If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
  
  
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheetId, range=range)
        .execute()
    )
    values = result.get("values", [])

  except HttpError as err:
    print(err)
  
  return values



def update_values(spreadsheet_id, range_name, value_input_option, values):
  "Update the values in a specific range of cells in the spreadsheet."
  
  # If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  # update the values in the spreadsheet
  try:
    service = build("sheets", "v4", credentials=creds)
    body = {"majorDimension":"ROWS", "values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred while updating the spreadsheet: {error}")
    return error




if __name__ == "__main__":
  main()