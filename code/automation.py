#import webdriver
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
from selenium.common.exceptions import InvalidSessionIdException

#storing country name 
urlls = ["/d/benin","/d/botswana","/d/cameroon","/d/cape-verde","/d/egypt","/d/eritrea","/d/ethiopia","/d/ghana","/d/ivory-coast","/d/kenya","/d/madagascar",
"/d/malawi","/d/mauritius","/d/morocco","/d/mozambique","/d/namibia","/d/reunion","/d/rwanda","/d/senegal","/d/seychelles","/d/south-africa","/d/tanzania",
"/d/tunisia","/d/uganda","/d/zambia","/d/zimbabwe","/d/armenia","/d/azerbaijan","/d/bhutan","/d/cambodia","/d/china","/d/cyprus","/d/georgia","/d/india",
"/d/indonesia","/d/israel","/d/japan","/d/jordan","/d/kazakhstan","/d/kyrgyzstan","/d/laos","/d/lebanon","/d/malaysia","/d/maldives","/d/mongolia",
"/d/myanmar-burma","/d/nepal","/d/oman","/d/pakistan","/d/philippines","/d/saudi-arabia","/d/singapore","/d/south-korea","/d/sri-lanka","/d/taiwan",
"/d/tajikistan","/d/thailand","/d/turkmenistan","/d/united-arab-emirates","/d/uzbekistan","/d/vietnam","/d/australia","/d/fiji","/d/new-zealand",
"/d/papua-new-guinea","/d/albania","/d/andorra","/d/austria","/d/belarus","/d/belgium","/d/bosnia","/d/bulgaria","/d/croatia","/d/czech-republic",
"/d/denmark","/d/england","/d/estonia","/d/finland","/d/france","/d/germany","/d/greece","/d/hungary","/d/iceland","/d/ireland","/d/italy","/d/jersey",
"/d/kosovo","/d/latvia","/d/lithuania","/d/macedonia","/d/malta","/d/moldova","/d/montenegro","/d/netherlands","/d/northern-ireland","/d/norway","/d/poland",
"/d/portugal","/d/romania","/d/russia","/d/scotland","/d/serbia","/d/slovakia","/d/slovenia","/d/spain","/d/svalbard","/d/sweden","/d/switzerland","/d/turkey",
"/d/ukraine","/d/wales","/d/canada","/d/greenland","/d/usa","/d/argentina","/d/belize","/d/bolivia","/d/brazil","/d/chile","/d/colombia","/d/costa-rica","/d/cuba",
"/d/dominican-republic","/d/ecuador","/d/el-salvador","/d/guatemala","/d/guyana","/d/honduras","/d/jamaica","/d/mexico","/d/nicaragua","/d/panama","/d/peru",
"/d/saint-vincent-and-the-grenadines","/d/uruguay","/d/venezuela","/d/virgin-island-british"]

#creating empty list
result = []

#looping to get the url of country one by one
for url in urlls:
   #create an instance of Chrome with the path of the driver that we downloaded through the websites of the respective browser
   driver = webdriver.Chrome('./chromedriver')
   #use the .get() method of the driver to load a website url.
   #getting the url of a country 
   driver.get('https://www.tourradar.com'+url)
   # wait for 10 seconds while opening the second country
   time.sleep(10)

  
   destination_urls = []
   #storing country name 
   country_name = url
   while(True):
      #taking xpath of a next button
      page_load_button = driver.find_elements_by_xpath('//button[@class="pagination__link js-ah-hidden-link"]/span[text()="Next "]')
      print(page_load_button,"testing")
      #taking x path of each page of a country
      urls = driver.find_elements_by_xpath('//a[@class="blank tourLink"]')
      print(len(urls))
      #loop to extract destination url of a country
      for url in urls:
         #collecting url of destinations one by one in a list
         destination_urls += [url.get_attribute('href')]

      #checking for the next button  
      if page_load_button:
         #click next button
         page_load_button[0].click()
         #wait for 20 seconds while opening second page of a country
         time.sleep(20)
      else:
         break
      

   print(len(destination_urls))

   
   #loop to extract the each destination information
   for url in destination_urls:
      
      print(url)
      #create an instance of Chrome with the path of the driver that we downloaded through the websites of the respective browser
      driver = webdriver.Chrome('./chromedriver')
      print("Current session is {}".format(driver.session_id))
      #use try and except to remove invalid session ID error
      try:
         #getting url
         driver.get(url)
      except Exception as e:
         print(e.message)

      #get page_source
      html = driver.page_source

      soup = BeautifulSoup(html, features="html.parser")
      #close the current open page/session
      driver.close()
      continent=[]
      country=[]
      destination=[]
      days = []
      end_in =[]
      travel_style =[]
      age_range =[]
      max_group_size=[]
      hygiene =[]
      operated_in=[]
     
      #storing country name into dictionary
      info = {"country": country_name}

      #extract no of the day of the destination.
      for i in soup.select('.ao-tour-above-fold__length'):
         days.append(i.text)
      #replace unwanted string with empty string
      days=list(map(lambda st: str.replace(st,"Book with flexibility\n                \n                ",""),days))
      days=list(map(lambda st: str.replace(st," days            ",""),days))
      #join day info into dictionary
      info['days']=" ".join(days)
        
      #extract name of the destination.
      for i in soup.select('.ttip'):
         destination.append(i.text)
      #replace unwanted string with empty string
      destination=list(map(lambda st: str.replace(st,"\n            ",""),destination))
      destination=list(map(lambda st: str.replace(st,"        ', '', '', '', '', '', '', '', '', '', ''",""),destination))
      #join destination name into dictionary
      info['destination']=" ".join(destination)
   
      
      for i in soup.select('.ao-tour-above-fold__from-to'):
         end_in.append(i.text)
      #replace unwanted string with empty string  
      end_in=list(map(lambda st: str.replace(st,"\n     ",""),end_in))
      #join where tour end into dictionary                                                 
      info['end_in']=" ".join(end_in)
      

      for i in soup.select('.ao-tour-keep-exploring'):
         travel_style.append(i.text)
      #replace unwanted string with empty string 
      travel_style=list(map(lambda st: str.replace(st,"\n        Keep Exploring South Africa    South Africa Travel GuideComplete Safari Packing List: Clothes, Medicines, Gear & EssentialsSouth Africa from Cape TownSouth africa ExplorerSmall group tour5 days South africaOperators in AfricaAddo Elephant ParkExplorer toursAddo Elephant Park toursSouth Africa toursAfrica toursGarden RouteAddo Elephant Park",""),travel_style))
      #store travel style into dictionary 
      info['travel_style']=str(travel_style)
 

      #extract max_group_size.
      for i in soup.select('.ao-tour-above-fold__properties-list--group-size'):
         max_group_size.append(i.text)
      #store max_group_size into dictionary 
      info['max_group_size']=" ".join(max_group_size)



      for i in soup.select('.ao-tour-above-fold__properties-list--age-range'):
         age_range.append(i.text)
      #store age range into dictionary 
      info['age_range']=" ".join(age_range)



      for i in soup.select('.ao-tour-above-fold__properties-list--operated-in'):
         operated_in.append(i.text)
      info['operated_in']=" ".join(operated_in)



      for i in soup.select('.ao-tour-above-fold__properties-list--hygieneprotocol'):
         hygiene.append(i.text)
      #replace unwanted string with empty string 
      hygiene=list(map(lambda st: str.replace(st,"\n",""),hygiene))
      hygiene=list(map(lambda st: str.replace(st," ",""),hygiene))
      info['hygiene']=" ".join(hygiene)
 

      cost =[]
      for i in soup.select('.ao-tour-above-fold__main-price'):
         cost.append(i.text)
      info['cost']=str(cost)
  

      visiting_places =[]
      for i in soup.select('.ao-tour-places-you-will-see__slider-title'):
         visiting_places.append(i.text)
      info['visiting_places']=str(visiting_places)




      description =[]
      for i in soup.select('.aa-tour-itinerary__text'):
         description.append(i.text)
      #replace unwanted string with empty string 
      description=list(map(lambda st: str.replace(st,"\n     ",""),description))
      description=list(map(lambda st: str.replace(st,". \n",""),description))
      info['description']=" ".join(description)


      Over_all_rating=[]

      for i in soup.select('.ao-tour-reviews__overview-list-icon--svg-overall~ .ao-tour-reviews__overview-list-rating'):
         Over_all_rating.append(i.text)
      #replace unwanted string with empty string 
      Over_all_rating=list(map(lambda st: str.replace(st,"\n        ",""),Over_all_rating))
      Over_all_rating=list(map(lambda st: str.replace(st,"\n    ', '\n        4.6\n    ",""),Over_all_rating))
      info['over_al_rating']=" ".join(Over_all_rating)
     


      reviews=[]


      for i in soup.select('.js-am-tour-reviews__review-item-body'):
         reviews.append(i.text)
      #replace unwanted string with empty string 
      reviews=list(map(lambda st: str.replace(st,"\n    ",""),reviews))
      reviews=list(map(lambda st: str.replace(st,"\n\n    ",""),reviews))
      info['reviews']=str(reviews)





      transport_rating=[]

      for i in soup.select('.ao-tour-reviews__overview-list-icon--svg-transport~ .ao-tour-reviews__overview-list-rating'):
         transport_rating.append(i.text)
      #replace unwanted string with empty string 
      transport_rating=list(map(lambda st: str.replace(st,"\n        ",""),transport_rating))
      transport_rating=list(map(lambda st: str.replace(st,"\n    ",""),transport_rating))
      info['transport_rating']=" ".join(transport_rating)



      food_rating=[]

      for i in soup.select('.ao-tour-reviews__overview-list-icon--svg-meals~ .ao-tour-reviews__overview-list-rating'):
         food_rating.append(i.text)
      #replace unwanted string with empty string 
      food_rating=list(map(lambda st: str.replace(st,"\n        ",""),food_rating))
      food_rating=list(map(lambda st: str.replace(st,"\n    ",""),food_rating))
      info['food_rating']=" ".join(food_rating)




      guide_rating=[]

      for i in soup.select('.ao-tour-reviews__overview-list-icon--svg-guide~ .ao-tour-reviews__overview-list-rating'):
         guide_rating.append(i.text)
      #replace unwanted string with empty string 
      guide_rating=list(map(lambda st: str.replace(st,"\n",""),guide_rating))
      guide_rating=list(map(lambda st: str.replace(st," ",""),guide_rating))
      info['guide_rating']=" ".join(guide_rating)




      accommodation_rating=[]

      for i in soup.select('.ao-tour-reviews__overview-list-icon--svg-accommodation~ .ao-tour-reviews__overview-list-rating'):
         accommodation_rating.append(i.text)
      #replace unwanted string with empty string 
      accommodation_rating=list(map(lambda st: str.replace(st,"\n",""),accommodation_rating))
      accommodation_rating=list(map(lambda st: str.replace(st," ",""),accommodation_rating))
      info['accommodation_rating']=" ".join(accommodation_rating)
  


      tourOperator_rating=[]

      for i in soup.select('.ao-tour-reviews__overview-list-icon--svg-operator~ .ao-tour-reviews__overview-list-rating'):
         tourOperator_rating.append(i.text)
      #replace unwanted string with empty string 
      tourOperator_rating=list(map(lambda st: str.replace(st,"\n        ",""),tourOperator_rating))
      tourOperator_rating=list(map(lambda st: str.replace(st,"\n    ",""),tourOperator_rating))
      info['tourOperator_rating']=" ".join(tourOperator_rating)
 

      tourOperator=[]

      for i in soup.select('.ao-tour-above-fold__properties-list--operator-name'):
         tourOperator.append(i.text)
      info['tourOperater']=" ".join(tourOperator)



      highlights=[]

      for i in soup.select('.ao-tour-highlights__facts-item'):
         highlights.append(i.text)
      info['highlights']=" ".join(highlights)


      total_reviews=[]
      for i in soup.select('.ao-tour-sticky-bar__rating-text'):
         total_reviews.append(i.text)
      #replace unwanted string with empty string 
      total_reviews=list(map(lambda st: str.replace(st,"\n",""),total_reviews))
      total_reviews=list(map(lambda st: str.replace(st," ",""),total_reviews))
      info['total_review']=" ".join(total_reviews)
  



      reviews_date=[]
      for i in soup.select('.am-tour-reviews__review-item-title-date'):
         reviews_date.append(i.text)
      #replace unwanted string with empty string 
      reviews_date=list(map(lambda st: str.replace(st,".",""),reviews_date))
      reviews_date=list(map(lambda st: str.replace(st," ",""),reviews_date))
      info['review_date']=" ".join(reviews_date)
      #append all infomation into result
      result.append(info)


   #wait for 20 second before loading the next country url
   time.sleep(20)
#create .json file
with open('result.json', 'w') as f:
   json.dump(result, f)



