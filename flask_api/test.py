from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import PyPDF2
from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials

drive_creds_filename = "mycreds.txt"
docs_creds_filename = "msa_service_account_key.json"

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile(drive_creds_filename)
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile(drive_creds_filename)

drive = GoogleDrive(gauth)

if (not drive):
    print("Google Drive was not initialized before this API call")
    sys.exit()

# Find the Google Doc file by title or file ID
folder_title = "MSA TV"
folder_id = None
file_title = "announcements"
file_id = None

# Find the folder by name
folder_list = drive.ListFile({'q': f"title='{folder_title}' and mimeType='application/vnd.google-apps.folder'"}).GetList()

# If the folder is found, use its ID
if len(folder_list) > 0:
    folder_id = folder_list[0]['id']
else:
    print("Folder not found")
    sys.exit()


# List all files in Google Drive with the given title
file_list = drive.ListFile({'q': f"'{folder_id}' in parents and title='{file_title}'"}).GetList()

# If the file is found, use its ID
if len(file_list) > 0:
    file_id = file_list[0]['id']

# Set up credentials
credentials = service_account.Credentials.from_service_account_file(
    docs_creds_filename, scopes=['https://www.googleapis.com/auth/documents']
)

# Create a service object
service = build('docs', 'v1', credentials=credentials)

# Get the document content
document = service.documents().get(documentId=file_id).execute()
document_content = document.get('body', {}).get('content', '')

# Extract and print the text content
doc_text = ''
for elem in document_content:
    if 'paragraph' in elem:
        doc_text += elem['paragraph']['elements'][0]['textRun']['content']

print(doc_text)







# # Define the scope and credentials
# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('msa_service_account_key.json', scope)

# # Authorize the client with the credentials
# client = gspread.authorize(credentials)

# # Open the Google Sheet using its URL or name
# sheet = client.open('MSA TV/Iqamahs').sheet1

# # Read all values in the sheet
# data = sheet.get_all_values()

# # Print the data
# for row in data:
#     print(row)

