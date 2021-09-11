
"""travel recommendation using content based filtering"""

#import python liberaries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re, math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
#load clean travel dataset
df = pd.read_csv('/Users/ibtihalkhan/Downloads/clean_TourAndTravel_info.csv', low_memory=False)

#taking only useful features from the dataset
df1 =df[['destination','country','days','cost','travel_style']]

"""collecting meaningful words from travel_style coloumn that is given in text format"""

# creating a blank series 
category = pd.Series([])
i=0
#looping columns and rows of dataset
for index, row in df1.iterrows():
    #remove special charater and digits from te text
    text = re.sub("[^a-zA-Z]", " ",str(row['travel_style']))
    #collecting stop word i.e an,the,if and so on
    stop_words = set(stopwords.words('english')) 
    #print(stop_words)
    #splits a given text into words using the NLTK library
    word_tokens = word_tokenize(text) 
    #print(word_tokens)
    
    filtered_sentence = [] 
    
    # looping to collect meaniningful words from word_tokens
    for w in word_tokens: 
        if w not in stop_words: 
            #collect word that are not present in stop_words
            filtered_sentence.append(w) 

    Stem_words = []
    
    ps =PorterStemmer()
    for w in filtered_sentence:
        # stem is to shorten the lookup, and normalize sentences.
        #i.e Many variations of words carry the same meaning, other than when tense is involved.
        rootWord=ps.stem(w)
        #append words into stem_words
        Stem_words.append(rootWord)
    category[i]= Stem_words
    i = i+1
    #print(category)

# inserting new column with values of list into a dataframe after removing stop word(such as is,the,and,so on) made above       
df1.insert(4, "category", category)



#drop travel style coloumn
df1.drop(columns = ['travel_style'], inplace =True)
#set destination coloumn as an index
df1.set_index('destination', inplace=True)

# Now we will convert it from 'int' to 'String' type. 
df1['days'] = df1['days'].astype(str)
df1['cost'] = df1['cost'].astype(str)


"""collect all selected features into one coloumn called bag of words"""


#create bag_of_word empty coloumn in a datframe
df1["bag_of_words"] = ""
#take all coloumns of a dataframe 
columns = df1.columns

#loop through all the row of a columns of a dataframe
for index, row in df1.iterrows():
    words =""
    #extract all columns to combine features in a bag_of_word coloumn
    for col in columns:
        if col != 'days' and col!= 'cost' and col != 'country':
            words = words + ' '.join(row[col])+ ' '
            
        else:
            words = words + row[col] + ' '
    #collect features from word to a bag_of_word column 
    row['bag_of_words'] = words



#reset destination from index to coloumn
df1.reset_index(level=['destination'],inplace=True)


# Create our vectorizer
count = CountVectorizer()
#Converting our features into a vector
count_matrix = count.fit_transform(df1['bag_of_words']).toarray()


#calculate the similarity between the index extrcted 
#from a dataframe according to user preference with all the rows of bag_of_word coloumn 
cosine_sim = cosine_similarity(count_matrix)
cosine_sim



#convert days and cost columns from 'str' to 'float' type. 
df1['days'] = df1['days'].astype(float)
df1['cost'] = df1['cost'].astype(float)
#convert days and cost columns from 'float' to 'int' type. 
df1['days'] = df1['days'].astype(int)
df1['cost'] = df1['cost'].astype(int)
       
# Function that takes in user preference such as country,days,cost as input and outputs most similar destination
#after calculate the similarity between the index extrcted 
#from a dataframe according to user preference with all the rows of bag_of_word coloumn 
def get_recommendations(user_input):
    
    
    # check if all three preferences were input by the user
    if user_input['country'] and user_input['days'] and user_input['cost']:
        #extract row according to user input
        idx = df1[(df1['country'] == user_input['country']) & (df1['cost'] <= user_input['cost']) & (df1['days'] <= user_input['days'])]
    # check if only country and days were input by the user
    elif user_input['country'] and user_input['days']:
        idx = df1[(df1['country'] == user_input['country']) & (df1['days'] <= user_input['days'])]
    elif user_input['country'] and user_input['cost']:
        idx = df1[(df1['country'] == user_input['country']) & (df1['cost'] <= user_input['cost'])]
    elif user_input['days'] and user_input['cost']:
        idx = df1[(df1['cost'] <= user_input['cost']) & (df1['days'] <= user_input['days'])]
    elif user_input['country']:
        idx = df1[df1['country'] == user_input['country']]
    elif user_input['days']:
        idx = df1[df1['days'] == user_input['days']]
    elif user_input['cost']:
        idx = df1[df1['cost'] == user_input['cost']]
    #if input is not given by the user then print invalid input
    else:
        print("\n\n")
        print("\ninvalid input")
        #exit from the get_reccomendation funtion
        return False
    #check if no row is extracted i.e no entry available with that preference
    if idx.empty:
        print("\nNo entry available with this preference")
        #exit from the get_reccomendation funtion
        return False
    else:
        # Get the index according to user input
        idx = idx.index[0]
    
    #get the similarity score of each row
    distance = cosine_sim[idx]
    #sort the similarity score in descending order and take top 5 maximum score
    dest_list = sorted(list(enumerate(distance)),reverse= True,key=lambda x: x[1])[1:6]

    #loop through to reccomend top five destination with thier cost and days
    for i in dest_list:
        print("\n")
        print(df1.iloc[i[0]].destination)
        print(df1.iloc[i[0]].cost)
        print(df1.iloc[i[0]].days)
        print("\n")


"""take input from user"""

#create dictionary
user ={'country' : None, 
             'days' : None, 
             'cost' : None} 
print("avilable countries in a dataset")
print("['benin' 'botswana' 'cameroon' 'cape-verde' 'egypt' 'eritrea' 'ethiopia''ghana' 'ivory-coast' 'kenya' 'madagascar' 'malawi' 'mauritius' 'morocco''mozambique' 'namibia' 'reunion' 'rwanda' 'senegal' 'seychelles''south-africa' 'tanzania' 'azerbaijan' 'bhutan' 'cambodia' 'china''cyprus' 'georgia' 'tunisia' 'uganda' 'zambia' 'zimbabwe' 'armenia''indonesia' 'israel' 'japan' 'jordan' 'kazakhstan' 'kyrgyzstan' 'laos''lebanon' 'malaysia' 'maldives' 'mongolia' 'myanmar-burma' 'india''sri-lanka' 'taiwan' 'tajikistan' 'thailand' 'turkmenistan''united-arab-emirates' 'uzbekistan' 'vietnam' 'australia' 'fiji''new-zealand' 'papua-new-guinea' 'albania' 'andorra' 'austria' 'belarus''belgium' 'bosnia' 'bulgaria' 'croatia' 'czech-republic' 'denmark''england' 'estonia' 'finland' 'france' 'germany' 'greece' 'hungary''iceland' 'ireland' 'italy' 'jersey' 'kosovo' 'latvia' 'lithuania''macedonia' 'malta' 'moldova' 'montenegro' 'netherlands''northern-ireland' 'norway' 'poland' 'portugal' 'romania' 'russia''scotland' 'serbia' 'slovakia' 'slovenia' 'spain' 'svalbard' 'sweden''switzerland' 'turkey' 'ukraine' 'wales' 'canada' 'greenland' 'usa''argentina' 'belize' 'bolivia' 'brazil' 'chile' 'colombia' 'costa-rica''cuba' 'dominican-republic' 'ecuador' 'el-salvador' 'guatemala' 'guyana''honduras' 'jamaica' 'mexico' 'nicaragua' 'panama' 'peru''saint-vincent-and-the-grenadines' 'uruguay' 'venezuela''virgin-island-british']")
#take input from user
user['country'] = input("Enter the one of the country name given in the list above: ")
user['cost'] = input("Enter the cost in euro")
user['days'] = input("Enter the no of days (duration of stay): ")

#if cost is input by the user
if user['cost']:
    #convert cost from str to int
    user['cost'] = int(user['cost'])
#if days is input by the user
if user['days']:
    #convert days from str to int
    user['days'] = int(user['days'])
print(user)
#calling funtion for reccomendation
get_recommendations(user)
