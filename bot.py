import datetime, ssl, smtplib, os, selenium.webdriver, time

from email.message import EmailMessage

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## VARS YOU SHOULD CHANGE ##

# Search Vars #
search_query = ""           # Job you would type into Indeed. Example: "customer service advisor"
search_location = ""        # The city you want to search for jobs in. Example: "London"
pages_to_scrape = 5         # The number of pages to scrape jobs from. Default: 5
job_cap = 25                # The number of jobs the bot has to find before E-Mailing them to you.

# Email Vars #  
your_email = ""             # The E-Mail you want the bot to send the jobs to.
bot_email = ""              # The E-Mail of the bot. (Must be GMail)
bot_email_password = ""     # The randomly generated code for your bot's email.
bot_name = "Job Bot"        # The name that will show up in your email. Some special characters won't work

# Misc Vars #
geckodriver_location = ""   # Location of geckodriver.

## END OF VARS YOU SHOULD CHANGE ##

def send_email(bot_email: str, bot_pass: str, bot_name: str, recipiant: str, message: str):
    email_address = bot_email
    email_password = bot_pass

    subject = f"[{datetime.datetime.now().strftime('%d/%m/%Y')}] Jobs To Check Out"
    
    em = EmailMessage()
    em['From'] = bot_name
    em['To'] = recipiant
    em['Subject'] = subject
    em.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, recipiant, em.as_string())

def get_blacklist():
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/blacklist.txt", "r") as f:
        return f.read().strip().split('\n')

def contains_blacklisted_words(text_to_check: str):
    blacklist = get_blacklist()

    for bad_word in blacklist:
        if text_to_check.lower().__contains__(bad_word):
            return True

    return False

def get_job_sent_list():
    jobs = []
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/sent_jobs.txt", "r") as f:
        for line in f.readlines():
            if line.strip() != '':
                jobs.append(line.lower().strip())

    return jobs

def job_sent_previously(job_title: str):
    sent_jobs = get_job_sent_list()

    if job_title.lower() in sent_jobs:
        return True

    return False

def add_to_previously_sent_jobs(job_dict: dict):
    job_titles = list(job_dict.keys())

    with open(f"{os.path.dirname(os.path.realpath(__file__))}/sent_jobs.txt", "a") as f:
        for title in job_titles:
            f.write(f"{title.strip()}\n")

def turn_dicts_to_string(job_dict: dict):
    job_keys = list(job_dict.keys())
    job_values = list(job_dict.values())

    string_list = []

    for job_title, job_url in zip(job_keys, job_values):
        temp_string = f"{job_title}: {job_url}"
        string_list.append(temp_string)

    return '\n'.join(string_list)

def urlify_text(text_tup: tuple):
    search_query, location = text_tup

    url_search_query = search_query.replace(' ', '+').lower()
    url_location = location.lower()

    return (url_search_query, url_location)

def scrape_indeed(search_query: str, location: str, pages: int, job_cap: int, geckodriver_path: str):

    job_dicts = {}
    
    url_search_query, url_location = urlify_text((search_query, location))

    bot = selenium.webdriver.Firefox(executable_path=geckodriver_path)

    for x in range(0, pages + 1):
        if len(job_dicts.keys()) >= job_cap:
            break
        elif x == pages and len(job_dicts.keys()) < job_cap:
            print("not enough jobs, adding a new page")
            pages += 1

        bot.get(f'https://uk.indeed.com/jobs?q={url_search_query}&l={location}&start={x*10}')

        WebDriverWait(bot, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cardOutline')))

        results = bot.find_elements(By.CSS_SELECTOR, 'div.cardOutline')

        for result in results:
            title = result.find_element(By.CSS_SELECTOR, 'a.jcs-JobTitle span').text

            blacklisted = contains_blacklisted_words(title)
            been_sent_before = job_sent_previously(title)

            if not blacklisted and not been_sent_before:
                url = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                job_dicts.update({title:url})

    bot.quit()
    return job_dicts

def main():
    if search_query == "" or bot_email == "" or bot_email_password == "" or your_email == "":
        print("No search query supplied.")
        return 1
    elif bot_email == "" or bot_email_password == "":
        print("Bot Email or Bot Password is empty. Please fix this and try again.")
        return 1
    elif your_email == "":
        print("You haven't supplied an email for the bot to send the jobs to.")
        return 1
    elif geckodriver_location == "":
        print("Please specify the full path to your geckodriver executable.")
        return 1

    indeed_jobs = scrape_indeed(search_query, search_location, pages_to_scrape, job_cap, geckodriver_location)
    message = turn_dicts_to_string(indeed_jobs)
    send_email(bot_email, bot_email_password, bot_name, your_email, message)
    add_to_previously_sent_jobs(indeed_jobs)
    return 0

if __name__ == "__main__":
    main()