from wowspy import Wows
from pprint import pp
from config import apikey, NA_ClanID
from datetime import datetime, timedelta
api_key = apikey
my_api=Wows(api_key)
NA_Clan_ID = NA_ClanID
fiveDaysAgo = datetime.now() - timedelta(days = 5)
fourteenDaysAgo = datetime.now() - timedelta(days = 14)

def unixToUTC(unixTime):
    utc_time = datetime.utcfromtimestamp(unixTime)
    final_utc_time = utc_time #.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")
    return final_utc_time

def main():
    clan_members = my_api.clan_details(my_api.region.NA,NA_Clan_ID)["data"][str(NA_Clan_ID)]['members_ids']
    overFive = []
    overFourteen = []
    for member_id in clan_members:
        stats = my_api.player_personal_data(my_api.region.NA,member_id,fields='last_battle_time,nickname')
        lbt_unix = int(stats["data"][f'{member_id}']["last_battle_time"])
        nickname = stats["data"][f'{member_id}']["nickname"]
        lbt_utc = unixToUTC(lbt_unix)
        lbt_utc_str = lbt_utc.strftime("%Y-%m-%d %H:%M:%S(UTC)")
        if lbt_utc < fiveDaysAgo:
            overFive.append(f"{nickname} was last on {lbt_utc_str}")
        if lbt_utc < fourteenDaysAgo:
            overFourteen.append(f"{nickname} was last on {lbt_utc_str}")
            #print(f'{nickname} last battle was on {lbt_utc}')
            
    print(f'\nMembers over 5 days since LBT:\n')
    for member in overFive:
        print(f'{member}\n')
    print(f'\nMembers over 14 days since LBT:\n')
    for member in overFourteen:
        print(f'{member}\n')
    #print(clan_members)



if __name__ == '__main__':
    main()