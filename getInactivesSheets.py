#! /usr/bin/env python3

from wowspy import Wows
from pprint import pp
# config file
from config import APIKEY,AOD_A,AOD_B,AOD_C,AOD_D,AOD_EU,AOD_CZ_EU,EXCLUDED_USERS,OAUTH_KEY_LOCATION
from datetime import datetime, timedelta
# google sheets stuff
import pygsheets
import pandas as pd
# health check stuff
import requests


# authenticate!
gc = pygsheets.authorize(client_secret=OAUTH_KEY_LOCATION)
#gc = pygsheets.authorize(client_secret=OAUTH_KEY)

# create an instance of the WoWS API with my API Key
my_api=Wows(APIKEY)

# just putting all the regions even though we only use NA and EU.
NA = my_api.region.NA
EU = my_api.region.EU
ASIA = my_api.region.AS
RU = my_api.region.RU 


# Create empty dataframe using panda
df = pd.DataFrame()
# Open the sheet by name
sh=gc.open('AOD WoWS Port Inactivity')
# go to page 1
wks=sh[0]
# index to A1
wks.set_dataframe(df,(0,0))

# exclude the following users, i.e. officers alt accounts and such.
excludeUsers = EXCLUDED_USERS

# silly math stuff to get date 30 and 60 days ago
thirtyDaysAgo = datetime.now() - timedelta(days = 30)
sixtyDaysAgo = datetime.now() - timedelta(days = 60)

# create lists for 30 day and 60 day Nicknames, Profile Links, Days since Last Battle, and Date of Last Battle
nicks1 = ["Nickname"]
links1 = ["Profile Link"]
ports1 = ["Port"]
days_lbt1 = ["Days Since Last Battle"]
lbt_time1 = ["Date of Last Battle"]
nicks2 = ["Nickname"]
ports2 = ["Ports"]
links2 = ["Profile Link"]
days_lbt2 = ["Days Since Last Battle"]
lbt_time2 = ["Date of Last Battle"]

#change unix time to UTC
def unixToUTC(unixTime):
    utc_time = datetime.utcfromtimestamp(unixTime)
    final_utc_time = utc_time #.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")
    return final_utc_time

# use the clan ID to return the clan name as a string (reverse lookup, essentially)
def getClanID(CID):
    if CID == AOD_A:
        return "AOD_A"
    elif CID == AOD_B:
        return "AOD_B"
    elif CID == AOD_C:
        return "AOD_C"
    elif CID == AOD_D:
        return "AOD_D"
    elif CID == AOD_EU:
        return "AOD (EU)"
    elif CID == AOD_CZ_EU:
        return "AODCZ (EU)"
    else:
        return "Uh, WTF? ERROR."

# actually do the work with the Wargaming API
def getInactives(region, Clan_ID):
    # get the clan member's ID's for the given port
    clan_members = my_api.clan_details(region,Clan_ID)['data'][str(Clan_ID)]['members_ids']
    #print(clan_members)

    # create lists for members that are exceeding 30 days and 60 days, respectively.
    overThirty = []
    overSixty = []

    # check each member in each port, grab their nickname, and last battle time to be able to compile a list of 
    # usernames + days since last battle
    for member_id in clan_members:
        stats = my_api.player_personal_data(region,member_id,fields='last_battle_time,nickname')
        #print(stats)
        lbt = stats['data'][f'{member_id}']['last_battle_time']
        #print(lbt)
        lbt_unix = int(lbt)
        nickname = stats['data'][f'{member_id}']['nickname']
        # if the nickname is one of the excluded users, just skip them. This is reserved for officer's alt accounts primarily.
        if nickname in excludeUsers:
            continue
        
        # do a bunch of confusing stuff with time

        # WG gives us the LBT in unix time, so change that to a datetime in UTC.
        lbt_utc = unixToUTC(lbt_unix)
        # make that datetime object a string we can work with and read in a specific format.
        lbt_utc_str = lbt_utc.strftime("%Y-%m-%d (UTC)")

        # do the math to see how many days it's been since the last battle and now.
        days_since_lbt = datetime.now() - lbt_utc
        
        # if it's over 30 days but less than or equal to 60 days, then put them on the 30day list.
        if lbt_utc < thirtyDaysAgo and lbt_utc >= sixtyDaysAgo:
            ports1.append(getClanID(Clan_ID))
            # get nickname
            nicks1.append(nickname)
            # NA links
            if region == NA:
                links1.append(("https://profile.worldofwarships.com/statistics/"+str(member_id)))
            # make sure if they're EU the link actually freaking works    
            if region == EU:
                links1.append(("https://profile.worldofwarships.eu/statistics/"+str(member_id)))
            lbt_time1.append(str(lbt_utc_str))
            days_lbt1.append(str(days_since_lbt.days))
            overThirty.append(f"{nickname} was last on {lbt_utc_str}, {days_since_lbt.days} days ago")
        
        # if it's over 60 days then put them in the over 60 day list.
        if lbt_utc < sixtyDaysAgo:
            # get nickname
            nicks2.append(nickname)
            ports2.append(getClanID(Clan_ID))

            # link if NA
            if region == NA:
                links2.append(("https://profile.worldofwarships.com/statistics/"+str(member_id)))
            # link if EU
            if region == EU:
                links2.append(("https://profile.worldofwarships.eu/statistics/"+str(member_id)))
            lbt_time2.append(str(lbt_utc_str))
            days_lbt2.append(str(days_since_lbt.days))
            overSixty.append(f"{nickname} was last on {lbt_utc_str}, {days_since_lbt.days} days ago")
            #print(f'{nickname} last battle was on {lbt_utc}')
        #return overThirty,overSixty
    o30 = ""
    o60 = ""
    # priinting members to console if over 30 and over 60.
    if (len(overThirty) > 0):
        #print(f'\nMembers over 30 days since LBT:\n\n')
        o30 += f'Members over 30 days since LBT:\n\n'
    for member in overThirty:
        #print(f'{member}\n')
        o30 += f'{member}\n'
    if(len(overSixty) > 0):
        #print(f'\nMembers over 60 days since LBT:\n\n')
        o60 += f'\nMembers over 60 days since LBT:\n\n'
    for member in overSixty:
        #print(f'{member}\n')
        o60 += f'{member}\n'
    tot = o30 + o60
    return tot
    #print(f'\n Rest of the clan, not inactive:\n')
    #print(clan_members)

def getStringInactives(r, c):
    na30,na60 = getInactives(r,c)
    na30 = f"Over 30 days since LBT:\n"
    na60 = f"Over 60 days since LBT:\n"
    for m in na30:
        na30 += f'{m}\n'
    for m in na60:
        na60 += f'{m}\n'
    total = na30 + na60
    return total

#call the API for each port
print("AOD_A Done")
getInactives(NA,AOD_B)
print("AOD_B Done")
getInactives(NA,AOD_C)
print("AOD_C Done")
getInactives(NA,AOD_D)
print("AOD_D Done")
# EU is included too!
getInactives(EU,AOD_EU)
print("AOD (EU) Done")
getInactives(EU,AOD_CZ_EU)
print("AODCZ (EU) Done")
print("All Port WG API calls finished")

def sheets():
    print("Starting Google API calls...")
    #sheet 1
    wks=sh[0]
    # index to A1
    wks.set_dataframe(df,(0,0))
    # clear all entries
    wks.clear("*")
    wks.update_col(1,nicks1)
    print("nicks 30+ done")
    wks.update_col(2,ports1)
    print ("port 30+ done")
    wks.update_col(3,days_lbt1)
    print("lbt_days 30+ done")
    wks.update_col(4,lbt_time1)
    print("lbt_time 30+ done")
    wks.update_col(5,links1)
    print("30+ done")
    wks.frozen_rows=1
    wks.sort_range((1,1),(150,150),2,"DESCENDING")
    # switch to sheet two
    wks=sh[1]
    # index to A1
    wks.set_dataframe(df,(0,0))
    # clear all entries
    wks.clear("*")
    wks.update_col(1,nicks2)
    print("nicks 60+ done")
    wks.update_col(2,ports2)
    print ("port 30+ done")
    wks.update_col(3,days_lbt2)
    print("lbt_days 60+ done")
    wks.update_col(4,lbt_time2)
    print("lbt_time 60+ done")
    wks.update_col(5,links2)
    print("Completely done")
    wks.frozen_rows=1
    wks.sort_range((1,1),(150,150),2,"DESCENDING")

def healthCheckStart():

    try:
        requests.get("https://hc-ping.com/2ca93c6f-dac7-4656-85ce-f93c37c3870a/start", timeout=10)
    except requests.RequestException as e:
        # Log ping failure here...
        print("Ping failed: %s" % e)

def healthCheck():

    try:
        requests.get("https://hc-ping.com/2ca93c6f-dac7-4656-85ce-f93c37c3870a", timeout=10)
    except requests.RequestException as e:
        # Log ping failure here...
        print("Ping failed: %s" % e)

def main():
    healthCheckStart()
    sheets()
    healthCheck()
if __name__ == '__main__':
    main()  

