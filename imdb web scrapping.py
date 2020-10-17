#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Scraping IMDB website using Python 

#If the data you’re looking for is on an web page, however, then the solution to all these problems is web scraping.
# We will scrap the all the Game of thrones episodes from the IMDB website.
# Importing required libraries and modules
# Using the IMDB website 
from requests import get
url = 'https://www.imdb.com/title/tt0944947/episodes?season=8'
response = get(url)
print(response.text[:350])
# Requesting from the server the content of the web page by using get(), and store the server’s response in the variable response.


# In[3]:


# View the website by inspecting element o0r just by pressing f12 for better understanding. 


# In[4]:


# Parsing response.text by creating a BeautifulSoup object, and assign this object to html_soup. The html.parser argument indicates that we want to do the parsing using Python’s built-in HTML parser.
from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')


# In[5]:


# Ignoring warning
import warnings
warnings.filterwarnings('ignore')


# In[6]:


# We will grab all of the instances of <div class="info" ...> </div> from the page; there is one for each episode.
# find_all() returned a ResultSet object –episode_containers– which is a list containing all the DIV tags.
episode_containers = html_soup.find_all('div', class_='info')


# In[7]:


# The HTML attributes are the dictionary’s keys. The values of the HTML attributes are the values of the dictionary’s keys.
# Extracting Title of Episodes by calling title attribute from the <a> tag.
episode_containers[0].a['title']


# In[8]:


# Episode number in the <meta> tag, under the content attribute. 
episode_containers[0].meta['content']


# In[9]:


# Extracting Airdate of episodes
episode_containers[0].find('div', class_='airdate').text.strip()


# In[10]:


# Extracting IMDB Rating of episodes
episode_containers[0].find('span', class_='ipl-rating-star__rating').text


# In[11]:


episode_containers[0].find('span', class_='ipl-rating-star__total-votes').text


# In[12]:


# Extracting Episode description.
episode_containers[0].find('div', class_='item_description').text.strip()


# In[13]:


# declaration of list
community_episodes = []

# For every season in the series -range depends on the show
for sn in range(1,9):
    # Request from the server the content of the web page by using get(), and store the server’s response in the variable response, just as we did earlier.
    response = get('https://www.imdb.com/title/tt0944947/episodes?season=' + str(sn))

    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')

    # Select all the episode containers from the season's page
    episode_containers = page_html.find_all('div', class_ = 'info')

    # For each episode in each season
    for episodes in episode_containers:
            # Getting the info of each episode on the page
            season = sn
            episode_number = episodes.meta['content']
            title = episodes.a['title']
            airdate = episodes.find('div', class_='airdate').text.strip()
            rating = episodes.find('span', class_='ipl-rating-star__rating').text
            total_votes = episodes.find('span', class_='ipl-rating-star__total-votes').text
            desc = episodes.find('div', class_='item_description').text.strip()
            # Compiling the episode info
            episode_data = [season, episode_number, title, airdate, rating, total_votes, desc]

            # Append the episode info to the complete dataset
            community_episodes.append(episode_data)


# In[14]:


# Creating a dataFrame to gather all info at one place.
import pandas as pd 
community_episodes = pd.DataFrame(community_episodes, columns = ['season', 'episode_number', 'title', 'airdate', 'rating', 'total_votes', 'desc'])
# Viewing the Dataframe
community_episodes.head()


# In[15]:


# Now time for some Data cleaning.
# As you can see th etotal votes is extracted with the parentheses,so we need to remove that.
community_episodes['total_votes'].unique()


# In[18]:


# function to remove parenthese
def remove_str(votes):
    for r in ((',',''), ('(',''),(')','')):
        votes = votes.replace(*r)
        
    return votes


# In[19]:


community_episodes['total_votes'] = community_episodes.total_votes.apply(remove_str).astype(int)

# Checking if done successfully
community_episodes.head()


# In[ ]:


# Converting the rating column into numeric type as it was extracted as string.
community_episodes['rating'] = community_episodes.rating.astype(float)


# In[ ]:


# Manupulating the airdate column as real date and time format.
community_episodes['airdate'] = pd.to_datetime(community_episodes.airdate)
community_episodes.info()


# In[ ]:


community_episodes.head()


# In[ ]:


# Finally, Converting the dataset into CSV file and save it.
community_episodes.to_csv('Game_Of_Thrones_Episodes_IMDb_info.csv',index=False)


# In[ ]:


# End of the script.




