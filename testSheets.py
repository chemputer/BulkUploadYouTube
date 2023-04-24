import pygsheets
import pandas as pd
gc = pygsheets.authorize(client_secret='E:\\Projects\\Repos\\PyWoWSStats\\oauth.json')

sh=gc.open('AOD WoWS Port Inactivity')
wks=sh[0]
wks.sort_range((1,1),(10,150),2,"DESCENDING")
wks.clear("*")
wks=sh[1]
wks.sort_range((1,1),(10,150),2,"DESCENDING")
wks.clear("*")

print(gc.drive.list(q="mimeType='application/vnd.google-apps.spreadsheet'", fields="files(name, parents), nextPageToken, incompleteSearch"))
