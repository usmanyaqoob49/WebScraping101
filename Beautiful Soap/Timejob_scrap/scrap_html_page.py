from bs4 import BeautifulSoup
#we will try to access content of index.html
#opening the html file
with open("index.html", "r") as file:
    #content of file-->html code
    content= file.read()

    #getting content with Beautiful Soap
    #lxml is the parser we will be using--> we use parsers to interpret structure and extract relavent information
    soup= BeautifulSoup(content, 'lxml') 
    #to get whole page code 
    print(soup.prettify())
    print('**********************************************************************')
    #to get all the h5 tags
    tags= soup.find_all('h5')
    #to get only text in the tags
    for tag in tags:
        print(tag.text)

    print('======================================================================')
    #to get the price information of all the courses
            #to find course cards we will find div tags and in div tags class will 'card' 
            #all the course_cards have same class 
            #we wrote class_ so that Beautiful soap can understand that we are talking about html class and not the python Class
    course_card= soup.find_all('div', class_= 'card')
    #now iterating over courses
    for courses in course_card:
        #to grab h5 tags that are in our course_cards
        course_name= courses.h5.text
        #now for the price of the courses
        #it is in the <a> tag and text will give start for $ and we only want $
        course_price = courses.a.text.split(' ')[-1]
        print(f'{course_name} Costs {course_price}')
