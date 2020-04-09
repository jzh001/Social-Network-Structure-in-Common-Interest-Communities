'''
This is a web scraper to scrape music reviews from https://www.metal-archives.com

Based on the json files, this program extracts the following features from each review:
1. Band
2. Album
3. Author
4. Rating
5. Date
6. Review
7. Link

These data are then transferred to a csv file, reviews.csv.

Data is extracted from Year 2002 to to Year 2019. 

Total No. of Entries = 41130

Runtime: Around 5-10 min

'''

import requests
from bs4 import BeautifulSoup
import re
import json
f = open("reviews.csv", 'w+')
def scrape(year, month):#scrape for each year and month
    tmpstr = str(month)
    if len(tmpstr) == 1:
        tmpstr = '0' + tmpstr
    url = 'https://www.metal-archives.com/review/ajax-list-browse/by/date/selection/' + str(year) + '-' + tmpstr + '/'
    r = requests.get(url)
    #print(r.content)
    html_doc = r.content
    #print(r.content.decode())
    rawData = re.split('"',str(r.content.decode()))#converting json into string

    months = ['January','February','March','April','May','June','July','August','September','October','November','December']#to check for date

    link = [] #finding https
    review = [] #Review titles only
    rating = [] #As a percentage
    date = [] #month + date
    cnt = 1 #debugging counter
    prev = True #if previous word is part of the review
    for i in range(0,len(rawData)):
        word = rawData[i]
        if len(word) > 4 and word[:5] == "https" and word.split('/')[3] == 'reviews':
            #check for the first link where information on band, album and author can be extracted.
            #This is also the link of the review which can be analysed further later
            link.append(word)
            #print(cnt,word)
            #cnt += 1
        elif (rawData[i-1][:7] == ' title=') and word[:7] != ' class=':
            #find the title of the review
            review.append(word[:-1])
            i1 = i + 1
            while i1<len(rawData) and rawData[i1][:7] != ' class=':#when reviews have ""
                #print(i1)
                review[-1] += rawData[i1][:-1]
                i1 += 1
                #print(review[-1])
            #print(cnt,rawData[i+1][0] == ' ')

            #print(cnt,rawData[i-1])
            #cnt += 1
            
        elif len(word) > 0 and word.split()[0] == months[month-1]:
            #find the date
            date.append(word)
            #print(word)
            
        elif len(word) > 0 and word[-1] == '%' and word[0].isalpha() == False:
            #find the rating
            rating.append(word)
            #print(word)


    print(len(rating),len(link),len(review),len(date))
    #print(date[37])
    if len(review) != len(link) or len(review) != len(rating) or len(date) != len(review):
        print("ERROR year =",year,"month =",month)#check if no error, all should be equal due to constant no. of entries per page
        return -1
    for i in range(0,len(rating)):
        s = link[i]
        tmp = s.split('/')
        data = (tmp[4],tmp[5],tmp[7],rating[i],date[i]+' '+str(year),review[i],link[i])#band, album, author of review, rating, date, review, link
        for item in data:
            #print(item)
            try:
                item.encode('ascii')
            except UnicodeEncodeError:
                item = "Unknown" #username not in ascii
            f.write(item+',')
        #print(data)
        f.write('\n')#new entry
    return len(rating) # no error, return number of entries

def main():
    f.write('Band,Album,Author,Rating,Date,Review,Link\n')#headers
    total_entries = 0
    for year in range (2002,2020):
        print(year)#progress tracker
        for month in range (1,13):
            ret = scrape(year,month)
            if ret == -1:
                #if no. of entries not consistent
                print("ERROR")
                return 0
            total_entries += ret
        

    f.close()
    print("Total No. of Entries =",total_entries)
    print("Program terminated successfully with return value 0.")


#scrape(2006,7)
main()


