#!/usr/bin/env python
# coding: utf-8

# <center>
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/Images/SN_logo.png" width="300" alt="cognitiveclass.ai logo">
# </center>
# 

# <h1>Extracting Stock Data Using a Web Scraping</h1>
# 

# Not all stock data is available via the API in this assignment; you will use web-scraping to obtain financial data. You will be quizzed on your results.  
#  You will extract and share historical data from a web page using the BeautifulSoup library.
# 

# <h2>Table of Contents</h2>
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     
# 1. Extracting data using BeautifulSoup
#    
#     <ul> 
#     <li> Download the web page Using Requests Library </li>
#     <li> Parse HTML on a web page using BeautifulSoup </li>
#     <li> Extract data and duild a data frame </li>
# 
#     </ul>
# 
# 2. Extracting data using pandas
# 3. Exercise
# <p>
#     Estimated Time Needed: <strong>30 min</strong></p>
# </div>
# 
# <hr>
# 

# In[1]:


#!pip install pandas==1.3.3
#!pip install requests==2.26.0
get_ipython().system('mamba install bs4==4.10.0 -y')
get_ipython().system('mamba install html5lib==1.1 -y')
get_ipython().system('pip install lxml==4.6.4')
#!pip install plotly==5.3.1


# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In Python, you can ignore warnings using the warnings module. You can use the filterwarnings function to filter or ignore specific warning messages or categories.
# 

# In[3]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# ## Using Webscraping to Extract Stock Data Example
# 

# We will extract Netflix stock data [https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html).
# 

# <center> 
#     
# #### In this example, we are using yahoo finance website and looking to extract Netflix data.
# 
# </center>
#     <br>
# 
#   <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/Images/netflix.png"> </center> 
#   
# <center> Fig:- Table that we need to extract </center>
# 

# On the following web page we have a table with columns name (Date, Open, High, Low, close, adj close volume) out of which we must extract following columns  
# 
# * Date 
# 
# * Open  
# 
# * High 
# 
# * Low 
# 
# * Close 
# 
# * Volume 
# 
# 

# # Steps for extracting the data
# 1. Send an HTTP request to the web page using the requests library.
# 2. Parse the HTML content of the web page using BeautifulSoup.
# 3. Identify the HTML tags that contain the data you want to extract.
# 4. Use BeautifulSoup methods to extract the data from the HTML tags.
# 5. Print the extracted data
# 

# ### Step 1: Send an HTTP request to the web page
# 

# You will use the request library for sending an HTTP request to the web page.<br>
# 

# In[4]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"


# The requests.get() method takes a URL as its first argument, which specifies the location of the resource to be retrieved. In this case, the value of the url variable is passed as the argument to the requests.get() method, because you will store a web page URL in a url variable.
# 
# You use the .text method for extracting the HTML content as a string in order to make it readable.
# 

# In[5]:


data  = requests.get(url).text
print(data)


# ### Step 2: Parse the HTML content
# 

# <hr>
# <hr>
# <center>
# 
# # What is parsing?
# In simple words, parsing refers to the process of analyzing a string of text or a data structure, usually following a set of rules or grammar, to understand its structure and meaning.
# Parsing involves breaking down a piece of text or data into its individual components or elements, and then analyzing those components to extract the desired information or to understand their relationships and meanings.</center>
# <hr>
# <hr>
# 

# Next you will take the raw HTML content of a web page or a string of HTML code which needs to be parsed and transformed into a structured, hierarchical format that can be more easily analyzed and manipulated in Python. This can be done using a Python library called <b>Beautiful Soup</b>.
# 

# ## Parsing the data using the BeautifulSoup library
# * Create a new BeautifulSoup object.
# <br>
# <br>
# <b>Note: </b>To create a BeautifulSoup object in Python, you need to pass two arguments to its constructor:
# 
# 1. The HTML or XML content that you want to parse as a string.
# 2. The name of the parser that you want to use to parse the HTML or XML content. This argument is optional, and if you don't specify a parser, BeautifulSoup will use the default HTML parser included with the library.
# here in this lab we are using "html5lib" parser.
# 

# In[8]:


type(data)


# In[9]:


soup = BeautifulSoup(data, 'html5lib')


# ### Step 3: Identify the HTML tags
# 

# As stated above, the web page consists of a table so, we will scrape the content of the HTML web page and convert the table into a data frame.
# 

# You will create an empty data frame using the <b> pd.DataFrame() </b> function with the following columns:
# * "Date"
# * "Open"
# * "High" 
# * "Low" 
# * "Close"
# * "Volume"
# 

# In[10]:


netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])


# <hr>
# <hr>
# <center>
# 
# ### Working on HTML table  </center>
# <br>
# 
# These are the following tags which are used while creating HTML tables.
# 
# * &lt;table&gt;: This tag is a root tag used to define the start and end of the table. All the content of the table is enclosed within these tags. 
# 
# 
# * &lt;tr&gt;: This tag is used to define a table row. Each row of the table is defined within this tag.
# 
# * &lt;td&gt;: This tag is used to define a table cell. Each cell of the table is defined within this tag. You can specify the content of the cell between the opening and closing <td> tags.
# 
# * &lt;th&gt;: This tag is used to define a header cell in the table. The header cell is used to describe the contents of a column or row. By default, the text inside a <th> tag is bold and centered.
# 
# * &lt;tbody&gt;: This is the main content of the table, which is defined using the <tbody> tag. It contains one or more rows of <tr> elements.
# 
# <hr>
# <hr>
# 
# 

# ### Step 4: Use a BeautifulSoup method for extracting data
# 

# 
# We will use <b>find()</b> and <b>find_all()</b> methods of the BeautifulSoup object to locate the table body and table row respectively in the HTML. 
#    * The <i>find() method </i> will return particular tag content.
#    * The <i>find_all()</i> method returns a list of all matching tags in the HTML.
# 

# In[11]:


# First we isolate the body of the table which contains all the information
# Then we loop through each row and find all the column values for each row
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    
    # Finally we append the data of each row to the table
    netflix_data = netflix_data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)    


# ### Step 5: Print the extracted data
# 

# We can now print out the data frame using the head() or tail() function.
# 

# In[12]:


netflix_data.head()


# # Extracting data using `pandas` library
# 

# We can also use the pandas `read_html` function from the pandas library and use the URL for extracting data.
# 

# <center>
# 
# ## What is read_html in pandas library?
# `pd.read_html(url)` is a function provided by the pandas library in Python that is used to extract tables from HTML web pages. It takes in a URL as input and returns a list of all the tables found on the web page. 
# </center>
# 

# In[13]:


read_html_pandas_data = pd.read_html(url)


# Or you can convert the BeautifulSoup object to a string.
# 

# In[ ]:


#read_html_pandas_data = pd.read_html(str(soup))


# Because there is only one table on the page, just take the first table in the returned list.
# 

# In[14]:


netflix_dataframe = read_html_pandas_data[0]

netflix_dataframe.head()


# # Exercise: use webscraping to extract stock data
# 

# Use the `requests` library to download the webpage [https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html). Save the text of the response as a variable named `html_data`.
# 

# In[16]:


import requests

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html"
html_data = requests.get(url).text



# Parse the html data using `beautiful_soup`.
# 

# In[17]:


from bs4 import BeautifulSoup

html_soup = BeautifulSoup(html_data, 'html5lib')


# <b>Question 1:</b> What is the content of the title attribute?
# 

# In[19]:


title = html_soup.find('title')
title


# Using BeautifulSoup, extract the table with historical share prices and store it into a data frame named `amazon_data`. The data frame should have columns Date, Open, High, Low, Close, Adj Close, and Volume. Fill in each variable with the correct data from the list `col`. 
# 

# In[26]:


amazon_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])

for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    
    amazon_data = amazon_data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)


# Print out the first five rows of the `amazon_data` data frame you created.
# 

# In[27]:


amazon_data.head(5)


# <b>Question 2:</b> What are the names of the columns in the data frame?
# 

# In[28]:


amazon_data.columns


# <b>Question 3:</b> What is the `Open` of the last row of the amazon_data data frame?
# 

# In[32]:


#amazon_data.head(-1) # to display last five rows and get the last index
Open_last_row = amazon_data.loc[68, "Open"]
print (Open_last_row)


# <h2>About the Authors:</h2> 
# 
# <a href="https://www.linkedin.com/in/joseph-s-50398b136/">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.
# 
# Azim Hirjani<br>
# Akansha yadav
# 

# ## Change Log
# 
# | Date (YYYY-MM-DD) | Version | Changed By    |       Change Description              |
# | ----------------- | ------- | ------------- | ------------------------------------- |
# |  02-05-2023       |   1.3   | Akansha yadav | Updated Lab content under maintenance |
# |  2021-06-09       | 1.2     | Lakshmi Holla |   Added URL in question 3             |
# |  2020-11-10       | 1.1     | Malika Singla |   Deleted the Optional part           |
# |  2020-08-27       | 1.0     | Malika Singla |   Added lab to GitLab                 |
# 
# <hr>
# 
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
# 
# <p>
# 
