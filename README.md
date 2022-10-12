# Job-Search-Bot
A screen-scraper created with Python and Selenium, that I created to help with Job Searching.

# What does it do?
Searching for jobs takes a while, and the bulk of that time is spent just finding jobs that you want. I made this script to help. It searches Indeed for whichever jobs you want and then emails any that may appeal to you. You can also add things to a blacklist to stop jobs coming up that aren't suitable. This is something I have been using daily, since I have set it up to automatically run every day upon my first login.

# Prerequisites
For the script to work you'll have to do a bit of a one-time setup. After you've done it though, you won't have to do it again.

### Python Prerequisites
You'll need to download Python of course, other than this all you'll need is Selenium. To get it type `pip install selenium` in a terminal.

### Geckodriver
This script is centered around using Firefox as the browser. You'll need to download the geckodriver executable from [here](https://github.com/mozilla/geckodriver/releases) and extract it to a location you know, for later.

### G-Mail Account for the Bot.
You'll need to create a new G-Mail account for the bot. It could be your own, however I wouldn't recommend it. These accounts cost nothing.

Once you've created the account you'll need to do a few things to get a special password that we can use in the Python script.

1. Goto [here](https://myaccount.google.com/u/0/security) and login to your bot account, then turn on 2FA for the account.
2. Once done goto [this link](https://myaccount.google.com/u/0/apppasswords) and login with your bot account.
3. Click 'Select App' and choose 'Other (Custom Name)' and type in anything. I called mine PythonBotScript.
4. Then click the 'Generate' button at the bottom.

This will generate an App Password for your account, that can be used with the script. Save this for later.

# Setup
Download this script and open the 'bot.py' file in a text editor.

At the top under all of the 'import' and 'from' imports you will see a section called '# VARS YOU SHOULD CHANGE' we are going to change the settings in here to make sure the script works.

`search_query` - Is the job you want to search for. For example "customer service advisor"

`search_location` - Is the city where you want the jobs to be in.

`your_email` - Is the email you want to send the jobs to. This IS NOT the bots email.

`bot_email` - Is the email address of the G-Mail account you made earlier for your bot.

`bot_email_password` - Is the App Password we created just above.

`geckodriver_location` - Is the full path to your geckodriver which we installed earlier.

This is an example of how it could look:

`search_query = "customer service advisor"`

`search_location = "london"`

`your_email = "dontnagithub@gmail.com"`

`bot_email = "mybot@gmail.com"`

`bot_email_password = "udkdjhfadvklad"`

`geckodriver_location = "/home/dontna/geckodriver"`

Once you've set all of this up once, you never have to do it again. You can also automate its running by using a CronJob on Linux, or by using Windows Task Scheduler in Windows 10+ (I think so, I don't use Windows much)

# Any issues?
Feel free to open an issue here on GitHub and I'll try to fix it ASAP.

# Forking My Projects?
All of my projects you can fork and utilise the code however you want. You don't need to give me credit, but can do if you would like.
