import dropbox
import os
import dropbox.files

with open("TOKEN.txt","r") as f:
    TOKEN = f.read()

dbx = dropbox.Dropbox(TOKEN)
folder1 = 'Apps'
folder2 = 'dropbox1'

def upload_all_local_files():
    for file in os.listdir("local_files"):
        with open(os.path.join("local_files",file),"rb") as f:
            data = f.read()
            dbx.files_upload(data, f"/{folder1}/{folder2}/{file}")
upload_all_local_files()
def download_files_from_folder(folder_path):
    try:
        entries = dbx.files_list_folder(folder_path).entries
    except dropbox.exceptions.HttpError as err:
        print(f"Error listing folder '{folder_path}': {err}")
        return

    for entry in entries:
        # Extracting the folder structure from the Dropbox path
        folders = entry.path_display.split('/')

        # Creating local folder structure
        local_folder = os.path.join("local_files", *folders[:-1])
        os.makedirs(local_folder, exist_ok=True)

        # Local path for the file
        local_path = os.path.join(local_folder, entry.name)

        try:
            metadata, res = dbx.files_download(entry.path_display)
            with open(local_path, "wb") as f:
                f.write(res.content)
            print(f"File '{entry.name}' downloaded to {local_path}")
        except dropbox.exceptions.HttpError as err:
            print(f"Error downloading '{entry.name}': {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Specify the Dropbox folder path you want to download
folder_to_download = '/Apps/dropbox1/'

# Uncomment the following line to download files from the specified folder
download_files_from_folder(folder_to_download)





