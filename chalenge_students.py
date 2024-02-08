import os.path
import math

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
  # the spreadsheet ID can be found in the spreadsheet URL
  values = getData("10FdFjl30y7ZI6DQ7so1MTQzf8sIXUptUPLGwPzbOjoU","A2:F27")

  if not values:
      print("No data found.")
      return
  
  # find the total number of classes
  total_classes = int(values[0][0].split()[-1])

  # iterates over the students
  for i in range(2, len(values)):
    reg_number = values[i][0]
    name = values[i][1]
    num_absences = int(values[i][2])

    # line LOG
    print(f"\n LOG: {values[i]}")

    # average grande between the 3 tests in a scale from 0 to 10
    avg = (int(values[i][3])+int(values[i][4])+int(values[i][5]))/30
    print(f" avg -> {str(avg)}")
    
    # verify the situation of the student
    if(num_absences/total_classes > 0.25):
      values[i].append("Reprovado por Falta")
      values[i].append("0")
    elif(avg<5):
      values[i].append("Reprovado por Nota")
      values[i].append("0")
    elif(avg>=7):
      values[i].append("Aprovado")
      values[i].append("0")
    elif(avg>=5 and avg<7):
      values[i].append("Exame Final")
      # calculate the minimun grade for approval in the final exam
      naf = 10-avg
      values[i].append(math.ceil(naf))
      print(f" naf -> {math.ceil(naf)} ")
    else:
      values[i].append("ERROR!")

      
  #update_values(
  #    "1CM29gwKIzeXsAppeNwrc8lbYaVMmUclprLuLYuHog4k",
  #    "A1:C2",
  #    "USER_ENTERED",
  #    [["A", "B"], ["C", "D"]],
  #)



def getData(spreadsheetId: str, range: str):
  """
    Uses the Google API to get the values from the spreadsheet.
  """

  # If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
  
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
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




"""def update_values(spreadsheet_id, range_name, value_input_option, _values):
  "Update the values in a specific range of cells in the spreadsheet."
  
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

  creds= Credentials.from_authorized_user_file("token.json", SCOPES)
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    values = [
        [
            # Cell values ...
        ],
        # Additional rows ...
    ]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
"""






if __name__ == "__main__":
  main()