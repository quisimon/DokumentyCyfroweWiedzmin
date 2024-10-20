from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def authenticate():
    g_auth = GoogleAuth()

    g_auth.LocalWebserverAuth()
    return GoogleDrive(g_auth)


def find_or_create_folder(drive, folder_name):
    folder_list = drive.ListFile({
        'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    }).GetList()
    
    if folder_list:
        return folder_list[0]['id']
    else:
        folder_metadata = {
            'title': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']


def upload_file(file_path, file_name, folder_name=""):
    drive = authenticate()

    if folder_name == "":
        file = drive.CreateFile({'title': file_name})

    else:
        folder_id = find_or_create_folder(drive, folder_name)
        file = drive.CreateFile({
            'title': file_name,
            'parents': [{'id': folder_id}]
        })

    file.SetContentFile(file_path)
    file.Upload()
    
    print(f"File '{file_name}' uploaded successfully with file ID {file['id']}")
