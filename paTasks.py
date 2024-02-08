activate_this_file = "/home/ExoBen/.virtualenvs/kelvin-venv/bin/activate_this.py"

exec(open(activate_this_file).read(), {'__file__': activate_this_file})

import datetime
import shutil,os,sys

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

print("Loaded venv")

os.chdir("/home/ExoBen/kelvin")


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
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            gauth.GetFlow()
            gauth.flow.params.update({'access_type': 'offline'})
            gauth.flow.params.update({'approval_prompt': 'force'})
            auth_url = gauth.GetAuthUrl()
            print("Please use this link to obtain the code and paste it below. It can be found in the redirect link.", auth_url)
            code = input("CODE: ")
            gauth.Auth(code)
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")



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
    print("Backup success!")

backupDatabase()