import schedule
from datetime import datetime, date
import time
import requests
from bs4 import BeautifulSoup

#user input for a link to scrape
askLink = input('Enter a Link for scraping: ')
askInterval = input('Rerun interval in minutes: ')

#initial link calls
try:
    result = requests.get(askLink)
    print('Link called -> Status Code:' + str(result.status_code))
    result.raise_for_status()

    #page body
    src = result.content

    #beauts definition
    soup = BeautifulSoup(src, 'lxml')
    #find <a> tags
    tagLinks = soup.find_all("a")

    #request link
    def getLinkStatusCode(link):
        #try to call if valid successfull return the status code
        try:
            result = requests.get(link)
            result.raise_for_status()
            return str(result.status_code)
        #if timeouted
        except requests.exceptions.HTTPError as err:
            return str(err)
        except requests.exceptions.Timeout as err:
            return 'Timeouted' + str(err)
        #if too many redirects
        except requests.exceptions.TooManyRedirects as err:
            return 'Too many redirects' + str(err)
        #other errors
        except requests.exceptions.RequestException as err:
            return str(err)


    #main job declaration
    def job(tagLinks):
        print("\n\n\n ***New Job Started*** \n\n")
        #Variable definition 
        troubled = []
        good = []
        count = 1

        #loop through link list
        for link in tagLinks:

            #parse to take out the href attribute
            link = link['href']
            if link.startswith('http'):
                #if status code 200
                if getLinkStatusCode(link).startswith('2'):
                    print(str( count) + ')' + link + ' --> OK(' + getLinkStatusCode(link)  + '):' +  ' --> ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
                    #append to good array
                    good.append( str(count) + ')' + link  + ' --> ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
                    count += 1

                #if status code is true but not 200
                elif getLinkStatusCode(link) == True and getLinkStatusCode(link) != '200':
                    print( str(count) + ')' + 'Error' + getLinkStatusCode(link) + ' -->'  + ' --> ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
                    #append to troubled array
                    troubled.append( str(count) + ')' + link  + ' --> '  + ' --> ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\nError" + getLinkStatusCode(link) + "\n" )
                    count += 1

                #if status code is not true
                else:
                    print( str(count) + ')' + link + ' --> Error ' + getLinkStatusCode(link)  + ' --> ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
                    #append to troubled array
                    troubled.append( str(count) + ')' + link  + ' --> ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\nError" + getLinkStatusCode(link) + "\n" )
                    count += 1

        #Job Summary
        print("\n\n\n***Job Ended***\n")
        print("\nGood: " + str(len(good))+ "\n")
        for elem in good:
            print(elem)
        print("\nBad:" + str(len(troubled))+ "\n")
        for err in troubled:
            print(err)
        
        #"Nullify" variables to start values
        troubled = []
        good = []
        count = 1

    job(tagLinks)

    #set at what interval should the job rerun
    schedule.every(int(askInterval)).minutes.do(job, tagLinks)

    while 1:
        schedule.run_pending()
        time.sleep(1)

#Give out error if userlink does not
except requests.exceptions.HTTPError as err:
  print(str(err))
except requests.exceptions.RequestException as err:
  print(str(err))







    



