from bs4 import BeautifulSoup
import requests
import time
import os
import glob

unfamiliar_skills = input(
    'Put some skill that you are not familiar with (if it is more than one, seperate them with comma) > ')
print(f"Filtering out {unfamiliar_skills}")

unfamiliar_skills = [x for x in unfamiliar_skills.replace(' ', '').split(',')]


def find_jobs():
    html_text = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text

    soup = BeautifulSoup(html_text, 'lxml')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):

        published_date = job.find('span', class_='sim-posted').span.text

        if 'few' in published_date:
            company_name = job.find(
                'h3', class_='joblist-comp-name').text.strip()

            skills = job.find(
                'span', class_='srp-skills').text.replace(' ', '').strip().split(',')

            more_info = job.header.h2.a['href']

            unf = 0
            for unfamiliar_skill in unfamiliar_skills:
                if unfamiliar_skill in skills:
                    unf = 1
                    break

            if unf == 0:
                skills = ', '.join(skills)

                with open(f"posts/{index}.txt", 'w') as f:
                    f.write(f"Company Name: {company_name}\n")
                    f.write(f"Required Skills: {skills}\n")
                    f.write(f"More Info: {more_info}\n")
                print(f"File saved: {index}.txt")


if __name__ == '__main__':
    while True:
        files = glob.glob(os.path.join('posts', "*.txt"))
        for f in files:
            os.remove(f)
        find_jobs()
        time_wait = 10
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)
