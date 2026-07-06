# Project Konbini (server)
Project Konbini is a work-in-progress unofficial app store for obsolete Android devices (Android 1.0+)

# TODO
  * Implement proper authorization system (tokens)
  * Implement a dev console to upload apps
  * Implement an admin panel for admins to manage published apps and approve unverified ones
  * Implement filtering by supported architectures
  * Implement a desktop (and maybe mobile) website

# Running
1. Install all the needed stuff from `requirements.txt`
2. Run a test server to see if everything works
   `python3 main.py`
3. If everything's okay, run the production server
   `gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:5000 main:app`
4. If you're using one of OldMarket's clients, you may need to go to settings and change the endpoint there.

# Uploading
## Apps
Uploading an app is a quite hard process that only an admin can do.

1. Put the app icon to `../icons`
2. Put the app screenshots to `../screenshots`
3. Put the app APK(s) to `../apks`
4. Add the app entry to the database (`app` table)

Restarting the server is not needed.

## Categories
Adding categories also requires editing the database. For this add the entry to the `category` table.

## Accounts
To register an account use the `POST /api/register` endpoint, with `username`, `email` and `password` fields in the body.
