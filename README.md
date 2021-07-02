# WoWS Inactivity Checker 

## Purpose
This is designed for personal use, but I figured I may as well share it. It's designed to check any number of ports via their clan ID, getting the members of said ports, and checking 
to see if they are over 5 days (to send a warning that they are inactive), and at 14 days (to give a last warning and remove if necessary). This can either be run as a standalone script, outputting to the terminal output, or use the Discord Webhooks to post this periodically to a channel in your Discord server. *Some* experience in Python is required, although you may be able to figure it out intuitively if you have at least some grasp of programming and follow the comments.

## Installation Instructions
Clone the repo to somewhere on your computer, and then ensure you have Python installed, then run (in an admin cmd/powershell terminal on Windows, or with sudo on Linux, you can use a virtualenv or install it as a user and not an admin with the -u switch before the -r, but both are beyond the scope of this) from within the directory where you cloned the repo:

```python
python -m pip install -r requirements.txt
```
to install the required packages. Alternatively, you can manually install them by running `python -m pip install wowspy wargaming datetime prettyprint requests discord_webhooks`
but the requirements.txt method is easier. 

Then simply modify the script as needed:
* rename example-config.py to config.py
* get your own API key [from wargaming](https://developers.wargaming.net/applications/), add that to config.py
* get your clan IDs, which can be done a couple different ways, searching via [this tool](https://developers.wargaming.net/reference/all/wows/clans/list/) can be used, add them to config.py, ensuring to add the names of the variables to the import function at the beginning of getInactives.py, i.e. `from config import apikey, NA_ClanID, NA_NCTA_ClanID, RU_ClanID, EU_ClanID, ASIA_ClanID, ASIA2_ClanID, DiscordWebhookURL` change NA_ClanID and the rest to whatever names you've used, and also make sure to replace their uses later on (using the find and replace function is helpful here).
* (Optional) add your DiscordWebURL to the config.py file, after generating it. 
* Make any modifications to the script as needed to fit your clan
* to run it, simply `python .\getInactives.py` from within the repo directory. 
* create a scheduled task to run it on a schedule, using Task Scheduler on Windows, or Cron on Linux.
