from wowspy import Wows
from pprint import pp
import csv
import re
from config import apikey
api_key = apikey
my_api=Wows(api_key)

def getAccountID (pname):
    print(pname)
    pid_response = my_api.players(my_api.region.NA,pname,fields='account_id',limit=1)
    playerid = pid_response['data'][0]['account_id']
    return playerid

def getStatsFromID(account_id,name):
    stats = my_api.player_personal_data(my_api.region.NA,account_id,fields='statistics.pvp')
    battles = stats['data'][str(account_id)]['statistics']['pvp']['battles']
    wins = stats['data'][str(account_id)]['statistics']['pvp']['wins']
    losses = stats['data'][str(account_id)]['statistics']['pvp']['losses']
    max_frags = stats['data'][str(account_id)]['statistics']['pvp']['max_frags_battle']
    survived = stats['data'][str(account_id)]['statistics']['pvp']['survived_battles']
    damage = stats['data'][str(account_id)]['statistics']['pvp']['damage_dealt']
    winloss = wins/battles * 100
    avgdmg = damage/battles
    survivalperc = survived/battles * 100
    return name, battles, winloss, avgdmg, max_frags, survivalperc 


def getStatsFromPname(pname):
    a = []
    a += pname
    a += getStatsFromID(getAccountID(pname))
    return a
    
    


#function writeCSVout(pname,battles,wrate, avgdmg, maxfrags, surivalrate):
def main():
    names = []
    for line in open("E:\\Projects\\repos\\PyWoWSStats\\test.csv"):
        csvrow = re.sub(r"\s*,\s*", " ", line)
        csv_row = csvrow.split()
        names += csv_row
    
    fields = ["Player Name", "Battles", "Win Rate", "Average Damage", "Max Frags", "Survival Rate"]
    rows = []
    
    for name in names:
        
        try:
            pid_response = my_api.players(my_api.region.NA,name,fields='account_id',limit=1)
            playerid = pid_response['data'][0]['account_id']
            #print(str(name) + ": \t" + str(playerid))
            sol = getStatsFromID(playerid,name)
            print(sol)
            rows += sol 
        except:
            print(str(name) + " threw an error")
    
    filename = 'E:\\Projects\\repos\\PyWoWSStats\\testout.csv' 
    with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
        csvwriter.writerow(fields) 
        
    # writing the data rows 
        csvwriter.writerows(rows)
        print("done")
    
if __name__ == '__main__':
    main()