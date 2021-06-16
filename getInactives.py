from wowspy import Wows
from pprint import pp
from config import apikey, NA_ClanID, NA_NCTA_ClanID, RU_ClanID, EU_ClanID, ASIA_ClanID, ASIA2_ClanID, DiscordWebhookURL
from datetime import datetime, timedelta
import requests
from discord_webhooks import DiscordWebhooks

api_key = apikey
my_api=Wows(api_key)
#change this to EU_ClanID, ASIA_ClanID, or RU_ClanID.
NA_C = NA_ClanID
NA2_C = NA_NCTA_ClanID
EU_C = EU_ClanID
ASIA_C = ASIA_ClanID
ASIA2_C = ASIA2_ClanID
RU_C = RU_ClanID
webhook_url = DiscordWebhookURL
# change your region by changing the end to EU or Asia or RU.
NA = my_api.region.NA
EU = my_api.region.EU
ASIA = my_api.region.AS
RU = my_api.region.RU 

fiveDaysAgo = datetime.now() - timedelta(days = 5)
fourteenDaysAgo = datetime.now() - timedelta(days = 14)

def unixToUTC(unixTime):
    utc_time = datetime.utcfromtimestamp(unixTime)
    final_utc_time = utc_time #.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")
    return final_utc_time

def getInactives(region, Clan_ID):
    clan_members = my_api.clan_details(region,Clan_ID)['data'][str(Clan_ID)]['members_ids']
    #print(clan_members)
    overFive = []
    overFourteen = []
    for member_id in clan_members:
        stats = my_api.player_personal_data(region,member_id,fields='last_battle_time,nickname')
        #print(stats)
        lbt = stats['data'][f'{member_id}']['last_battle_time']
        #print(lbt)
        lbt_unix = int(lbt)
        nickname = stats['data'][f'{member_id}']['nickname']
        lbt_utc = unixToUTC(lbt_unix)
        lbt_utc_str = lbt_utc.strftime("%Y-%m-%d %H:%M:%S (UTC)")
        if lbt_utc < fiveDaysAgo and lbt_utc > fourteenDaysAgo:
            overFive.append(f"{nickname} was last on {lbt_utc_str}")
        if lbt_utc < fourteenDaysAgo:
            overFourteen.append(f"{nickname} was last on {lbt_utc_str}")
            #print(f'{nickname} last battle was on {lbt_utc}')
        #return overFive,overFourteen
    o5 = ""
    o14 = ""
    if (len(overFive) > 0):
        print(f'\nMembers over 5 days since LBT:\n\n')
        o5 += f'Members over 5 days since LBT:\n\n'
    for member in overFive:
        print(f'{member}\n')
        o5 += f'{member}\n'
    if(len(overFourteen) > 0):
        print(f'\nMembers over 14 days since LBT:\n\n')
        o14 += f'\nMembers over 14 days since LBT:\n\n'
    for member in overFourteen:
        print(f'{member}\n')
        o14 += f'{member}\n'
    tot = o5 + o14
    return tot
    #print(f'\n Rest of the clan, not inactive:\n')
    #print(clan_members)

def getStringInactives(r, c):
    na5,na14 = getInactives(r,c)
    tna5 = f"Over 5 days since LBT:\n"
    tna14 = f"Over 14 days since LBT:\n"
    for m in na5:
        tna5 += f'{m}\n'
    for m in na14:
        tna14 += f'{m}\n'
    total = tna5 + tna14
    return total
  
#def main():
 
    # webhook = DiscordWebhooks(WEBHOOKURL)

    # webhook.set_content(title='Inactive Game Acounts', description='Shows a listing of the inactive game accounts for each region', \
    # color=0xF58CBA, timestamp=f'{(datetime.now()).strftime("%Y-%m-%d %H:%M:%S(UTC)")}')

    # # Attaches an author
    # webhook.set_author(name='InactivityChecker')

    # NA_NCOTS = getInactives(NA,NA_C)
    # NA_NCTA = getInactives(NA,NA2_C)
    # EU_NCOTS = getInactives(EU,EU_C)
    # ASIA_NCOTS = getInactives(ASIA,ASIA_C)
    # RU_NCOTS = getInactives(RU,RU_C)
    # pp(f'NA: \n {NA_NCOTS} \n')
    # pp(f'NA NCTA: \n {NA_NCTA} \n')
    # pp(f'EU NCOTS: \n {EU_NCOTS} \n')
    # pp(f'ASIA NCOTS: \n {ASIA_NCOTS} \n')
    # pp(f'RU NCOTS: \n {RU_NCOTS} \n')

    # webhook.add_field(name='NA NCOTS', value=f'{getStringInactives(NA,NA_C)}')
    # webhook.add_field(name='NA NCTA', value=f'{getStringInactives(NA,NA2_C)}')
    # webhook.add_field(name='EU NCOTS', value=f'{getStringInactives(EU,EU_C)}')
    # webhook.add_field(name='ASIA NCOTS', value=f'{getStringInactives(ASIA,ASIA_C)}')
    # webhook.add_field(name='RU NCOTS', value=f'{getStringInactives(RU,RU_C)}') 

    # webhook.add_field(name='NA NCOTS', value=f'{NA_NCOTS}')
    # webhook.add_field(name='NA NCTA', value=f'{NA_NCTA}')
    # webhook.add_field(name='EU NCOTS', value=f'{EU_NCOTS}')
    # webhook.add_field(name='ASIA NCOTS', value=f'{ASIA_NCOTS}')
    # webhook.add_field(name='RU NCOTS', value=f'{RU_NCOTS}')

    # webhook.send()


def main():
    
    url = DiscordWebhookURL
#for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content" : "Inactivity Report for Each NCOTS Server",
        "username" : "Inactivity Checker"
    }
    NA_NCOTS = getInactives(NA,NA_C)
    NA_NCTA = getInactives(NA,NA2_C)
    EU_NCOTS = getInactives(EU,EU_C)
    ASIA_NCOTS = getInactives(ASIA,ASIA_C)
    ASIA2_NCOTS = getInactives(ASIA,ASIA2_C)
    RU_NCOTS = getInactives(RU,RU_C)
    pp(f'NA: \n {NA_NCOTS} \n')
    pp(f'NA NCTA: \n {NA_NCTA} \n')
    pp(f'EU NCOTS: \n {EU_NCOTS} \n')
    pp(f'ASIA NCOTS: \n {ASIA_NCOTS} \n')
    pp(f'ASIA NCOTSZ: \n {ASIA2_NCOTS} \n')
    pp(f'RU NCOTS: \n {RU_NCOTS} \n')
#leave this out if you dont want an embed
#for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description" : f'```{NA_NCOTS}```',
            "title" : "NA NCOTS"
        },
        {
            "description" : f'```{NA_NCTA}```',
            "title" : "NA NCTA"
        },
        {
            "description" : f'```{EU_NCOTS}```',
            "title" : "EU NCOTS"
        },
        {
            "description" : f'```{ASIA_NCOTS}```',
            "title" : "Asia NCOTS"
        },
        {
            "description" : f'```{ASIA2_NCOTS}```',
            "title" : "Asia NCOTZ"
        },
        {
            "description" : f'```{RU_NCOTS}```',
            "title" : "RU NCOTS"
        }
    ]

    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

if __name__ == '__main__':
    main()  

