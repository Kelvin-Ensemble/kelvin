import datetime
import shutil,os,sys

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from dotenv import load_dotenv

dotenv_file = ".env"
load_dotenv(dotenv_file)


def backupDatabase():
    def createZip(path,file_name):
        # use shutil to create a zip file
        try:
            shutil.make_archive(f"backup/{file_name}", 'zip', path, file_name)
            return True
        except FileNotFoundError as e:
            return False

    def init():
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile("mycreds.txt")
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
        gauth.SaveCredentialsFile("mycreds.txt")

    def googleAuthentication():
        # gauth.DEFAULT_SETTINGS['client_config_file'] = "client_secrets.json"
        gauth = GoogleAuth()
        gauth.GetFlow()
        gauth.flow.params.update({'access_type': 'offline'})
        gauth.flow.params.update({'approval_prompt': 'force'})
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
        return gauth, GoogleDrive(gauth)

    def upload_backup(drive, path, file_name):
        # create a google drive file instance with title metadata
        f = drive.CreateFile({'title': datetime.datetime.utcnow().strftime("%d%m%y-%H%M-") + file_name, 'parents': [{'id': '1K8jWsvmiIq-XkX4V30tiNzYb_AH7x_1Y'}]})
        # set the path to zip file
        f.SetContentFile(os.path.join(path, file_name))
        # start upload
        f.Upload()
        # set f to none because of a vulnerability found in PyDrive
        f = None

    if not createZip(os.getcwd(), "db.sqlite3"):
        sys.exit(0)

    auth, drive = googleAuthentication()

    upload_backup(drive, os.getcwd(), 'backup/db.sqlite3.zip')

backupDatabase()