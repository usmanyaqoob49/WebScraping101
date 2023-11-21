from bs4 import BeautifulSoup
import requests
import pandas as pd

#url of the website 
url= "https://www.investing.com/equities/pakistan-stock-exchange-historical-data"
#getting html page by requesting
html_page= requests.get(url)

print("Response Status Code: ", html_page.status_code)
#storing content of page
html_page= html_page.content

# #parsing the html page with lxml
soup= BeautifulSoup(html_page, 'lxml')

#---->Basically date by default on web was giving data of the one month so I have to access that date and change to get full data

#extracting the date
date_div= soup.find('div' , class_= 'flex flex-col justify-center flex-1 text-[#333] text-sm leading-5')
#now we have the date
if date_div is not None:
    print('Old date that was by default on website: ', date_div.text)
        # we need it to change the date
        #month/day/year
    date_div.string= '01/01/2023 - 01/19/2023'
    print('New date for the data scraping of stocks', date_div.text)

    #Now we need to extract rows of the table--> we do it by giving 'tr' that mean row and class of the row specified in html code of page
    trs=  soup.find_all('tr', class_= 'h-[41px]')

    #print(trs)

    # #to store the data
    data_list= []

    #now lets iterate over trs to get data and headers from each row
    for tr in trs:
        #extracting headers th and data td from each row 
        row_data= [td.text.strip() for td in tr.find_all(['td', 'th'])]
        # Create a dictionary for the row
        row_dict = {f'Column{i}': value for i, value in enumerate(row_data)}
        
        # Append the dictionary to the list
        data_list.append(row_dict)

    #making the dataframe from the list that have our dictionary
    df= pd.DataFrame(data_list)
    print(df)
    print(date_div.text)