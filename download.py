import os
from flask import send_from_directory
import app # Your internal module

def download_app(app_id, version: str | None = None):
    appdata = app.api_app(app_id)
    if type(appdata[0]) is not dict:
        print(appdata)
        return appdata

    apk_directory = os.path.abspath('../apks')

    versions = appdata[0]['versions']
    file_name = None
    if version:
        for i in versions:
            if i['version'] == version:
                file_name = i['apk_file'].lstrip('/')
    else:
        file_name = versions[-1]['apk_file'].lstrip('/')

    if not file_name:
        print(versions)
        return {"error": "No such version"}, 404
    
    if not os.path.exists(os.path.join(apk_directory, file_name)):
        print((os.path.join(apk_directory, file_name)))
        return {"error": "APK file not found on server"}, 404

    return send_from_directory(
        directory=apk_directory,
        path=file_name,
        as_attachment=True
    )

download_app_version = download_app

def app_icon(filename):
    apk_directory = os.path.abspath('../icons')
    file_name = filename.lstrip('/')

    if not os.path.exists(os.path.join(apk_directory, file_name)):
        return {"error": "Icon not found on server"}, 404

    return send_from_directory(
        directory=apk_directory,
        path=file_name,
    )

def app_sshot(package_name, file_name):
    apk_directory = os.path.abspath('../screenshots/'+package_name)
    file_name = file_name.lstrip('/')

    if not os.path.exists(os.path.join(apk_directory, file_name)):
        print("os.path.exists(os.path.join(apk_directory, file_name))")
        return {"error": "Screenshot not found on server"}, 404
    
    return send_from_directory(
        directory=apk_directory,
        path=file_name,
    )