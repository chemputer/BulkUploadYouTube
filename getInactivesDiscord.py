#! /usr/bin/env python3
from wowspy import Wows
from pprint import pp
from sys import argv
import argparse
from config import APIKEY,AOD_A,AOD_B,AOD_C,AOD_D,AOD_EU,AOD_CZ_EU,DISCORD_WEBHOOK_URL,EXCLUDED_USERS
from datetime import datetime, timedelta
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-d","--debug", action="store_true")
args = parser.parse_args()
if args.debug:
    print("debug worked!")
elif args.debug == False:
    print("debug failed!")
my_api=Wows(APIKEY)
# change your region by changing the end to EU or Asia or RU.
NA = my_api.region.NA
EU = my_api.region.EU
ASIA = my_api.region.AS
RU = my_api.region.RU 


excludeUsers = EXCLUDED_USERS

thirtyDaysAgo = datetime.now() - timedelta(days = 30)
sixtyDaysAgo = datetime.now() - timedelta(days = 60)


def unixToUTC(unixTime):
    utc_time = datetime.utcfromtimestamp(unixTime)
    final_utc_time = utc_time #.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")
    return final_utc_time

def getInactives(region, Clan_ID):
    clan_members = my_api.clan_details(region,Clan_ID)['data'][str(Clan_ID)]['members_ids']
    #print(clan_members)
    overThirty = []
    overSixty = []
    for member_id in clan_members:
        stats = my_api.player_personal_data(region,member_id,fields='last_battle_time,nickname')
        #print(stats)
        lbt = stats['data'][f'{member_id}']['last_battle_time']
        #print(lbt)
        lbt_unix = int(lbt)
        nickname = stats['data'][f'{member_id}']['nickname']
        if nickname in excludeUsers:
            continue
        lbt_utc = unixToUTC(lbt_unix)
        lbt_utc_str = lbt_utc.strftime("%Y-%m-%d (UTC)")
        days_since_lbt = datetime.now() - lbt_utc

        if lbt_utc < thirtyDaysAgo and lbt_utc >= sixtyDaysAgo:
            if region == NA:
                link=("https://profile.worldofwarships.com/statistics/"+str(member_id))
            # make sure if they're EU the link actually freaking works    
            if region == EU:
                link=("https://profile.worldofwarships.eu/statistics/"+str(member_id))
            overThirty.append(f"{nickname} last played {days_since_lbt.days} days ago, on {lbt_utc_str}\n profile link: {link}")
        if lbt_utc < sixtyDaysAgo:
            if region == NA:
                link=("https://profile.worldofwarships.com/statistics/"+str(member_id))
            # make sure if they're EU the link actually freaking works    
            if region == EU:
                link=("https://profile.worldofwarships.eu/statistics/"+str(member_id))
            overSixty.append(f"{nickname} last played {days_since_lbt.days} days ago, on {lbt_utc_str}\n profile link: {link}")

            #print(f'{nickname} last battle was on {lbt_utc}')
        #return overThirty,overSixty
    o30 = ""
    o60 = ""
    if (len(overThirty) > 0):
        #print(f'\nMembers over 30 days since LBT:\n\n')
        o30 += f'Members over 30 days since LBT:\n\n'
    for member in overThirty:
       # print(f'{member}\n')
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
NA_AOD_A = getInactives(NA,AOD_A)
print("AOD_A Done")
NA_AOD_B = getInactives(NA,AOD_B)
print("AOD_B Done")
NA_AOD_C = getInactives(NA,AOD_C)
print("AOD_C Done")
NA_AOD_D = getInactives(NA,AOD_D)
print("AOD_D Done")
# EU is included too!
EU_AOD = getInactives(EU,AOD_EU)
print("AOD (EU) Done")
EU_AODCZ = getInactives(EU,AOD_CZ_EU)
print("AODCZ (EU) Done")
print("All Port WG API calls finished")

# using pretty print to format this neatly when it outputs to console. Be sure to change the clan names as appropriate.
def printInactives():
    pp(f'AOD_A: \n {NA_AOD_A} \n')
    pp(f'AOD_B: \n {NA_AOD_B} \n')
    pp(f'AOD_C: \n {NA_AOD_C} \n')
    pp(f'AOD_D: \n {NA_AOD_D} \n')
    pp(f'AOD (EU): \n {EU_AOD} \n')
    pp(f'AOD_CZ (EU): \n {EU_AODCZ} \n')

def webhook():
    
    url = DISCORD_WEBHOOK_URL
#for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    
    # change the name here, as well as for each of the embeds below. The pp() statements simply show up on the terminal output, so if using discord webhook,
    # it's unnecessary.
    data = {
        "content" : "Inactivity Report for Each AOD Port",
        "username" : "Inactivity Checker"
    }

    

#leave this out if you dont want an embed
#for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        # each dict (the {key:pair, key:pair} portions) consitutes its own embed.
        
        {
            "description" : f'```{NA_AOD_A}```',
            "title" : "AOD_A"
        },
        {
            "description" : f'```{NA_AOD_B}```',
            "title" : "AOD_B"
        },
        {
            "description" : f'```{NA_AOD_C}```',
            "title" : "AOD_C"
        },
        {
            "description" : f'```{NA_AOD_D}```',
            "title" : "AOD_D"
        },
        {
            "description" : f'```{EU_AOD}```',
            "title" : "AOD (EU)"
        },
        {
            "description" : f'```{EU_AODCZ}```',
            "title" : "AODCZ (EU)"
        }
    ]

    result = requests.post(url, json = data)
    print("sending to discord")
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def main():
    webhook()
if __name__ == '__main__':
    #main()
    if args.debug:
        printInactives()

