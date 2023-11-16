from bs4 import BeautifulSoup
import requests
import time

#we want to get python jobs from timejobs.com
#to get html text we will give link and .text will give us the html code of the page
html_text = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=").text
soup = BeautifulSoup(html_text, 'lxml')

#asking user to enter some skills he is not familiar with so that we do not print inforamtion about those jobs
print("Enter Skills you are not familiar with to proceed further write 'done': ")
unfamiliar_skills= []
while True:
    user_input= input('>')
    #when write done exit from loop
    if user_input== 'done':
        break
    else:
    #otherwise if skill is entered append it in the list
        unfamiliar_skills.append(user_input)
def find_jobs():
    #if you open inspect you will know that jobs are listed with <li> tag
    #and class name of all the item is "clearfix job-bx wht-shd-bx"
    jobs= soup.find_all('li', class_="clearfix job-bx wht-shd-bx" )

    #now jobs have list of all jobs so we have to iterate over this to get each
    for index, job in enumerate(jobs):
        #--------------Now we want only jobs that are posted recently---------------------
        #In every job there is Line Written "Posted - days ago"
        #And that information is also under the <span> tag and class= "sim-posted"
        published_date= job.find('span', class_= 'sim-posted').text
        #we only want jobs with "Posted few days ago"
        if 'few' in published_date:
            #in job name of the company is under <h3> tag with class name as joblist-comp-name
            #we will get text and will remove whitespace
            company_name= job.find('h3', class_= 'joblist-comp-name').text.strip()


            #now to get skills for the job
            #so it is under <span> tag with class name = srp-skills
            skills= job.find('span', class_= 'srp-skills').text.strip()
        

            #now to get more info we need a link of the header
            #it is under header, <h2> tag and link is then in <a> tag and to get link only we will access href
            more_job_info= job.header.h2.a['href']

            #flag for the skipping the job
            skip_job= False

            #we will print only those Ads that do not have the unfamiliar skills that were entered by the user
            for skill in unfamiliar_skills:
                #if unfamiliar skill is found in skills required
                if skill in skills:
                    #make the flag true
                    skip_job= True
                    #and exit the loop
                    #so loop will be terminated even one unfamiliar skill is found
                    break
                    
            #if flag is false -->means we have not found single unfmailiar skill in the list entered by the user
            if skip_job==False:
                #so we will write the information about post in the file
                with open(f'job_ads/{index}.txt', 'w') as file:
                    file.write(f"Company Name: {company_name}")
                    file.write(f"Skills Required: {skills}")
                    file.write(f"Published: {published_date}")
                    file.write(f"More Information about Job: {more_job_info}")
                print('File Saved.')
if __name__=='__main__':
    #we want this program to fetch jobs every 10 min
    while True:
        find_jobs()
        print('Waititng...')
        time.sleep(600)