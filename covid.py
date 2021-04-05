# Importing required packages
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import plotly
import plotly.graph_objects as go
import datetime as dt
import requests
from plotly.subplots import make_subplots

# Getting Data
# data can be used in CSV format too
url_request = requests.get("https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases/FeatureServer/1/query?where=1%3D1&outFields=*&outSR=4326&f=json") #Sauce url
url_json = url_request.json() # getting the data using request
df = pd.DataFrame(url_json['features']) # converting json into data frame
df['attributes'][0]

# Data Wrangling

# transforming data

data_list = df['attributes'].tolist()
data = pd.DataFrame(data_list)
data.set_index('OBJECTID')
data = data[['Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Recovered','Deaths','Active']] 
data.columns = ('State','Country','Last Update','Lat','Long','Confirmed','Recovered','Deaths','Active')
data['State'].fillna(value = '', inplace = True)
data

# cleaning data

def convert_time(t):
    t = int(t)
    return dt.datetime.fromtimestamp(t)

data = data.dropna(subset = ['Last Update'])
data['Last Update'] = data['Last Update']/1000
data['Last Update'] = data['Last Update'].apply(convert_time)
data

# Exploratory Data Analysis & Visualization

# Our analysis contains 'Ranking countries and provinces', 'Time Series' and 'Classification and Distribution'

# Ranking countries and provinces
# Top 5 confirmed countries (Bubble plot)

top5_confirmed = pd.DataFrame(data.groupby('Country')['Confirmed'].sum().nlargest(195).sort_values(ascending = False)) # Adjust the value of nlargest to change noumber of countries
fig1 = px.scatter(top5_confirmed, x = top5_confirmed.index, y = 'Confirmed', size = 'Confirmed', size_max = 100,  # adjust sizE_max value for bubble size
                color = top5_confirmed.index, title = 'Confirmed Cases of all Countries')
fig1.show()

# Top 5 active countries

top5_active = pd.DataFrame(data.groupby('Country')['Active'].sum().nlargest(5).sort_values(ascending = True))
fig4 = px.bar(top5_active, x = 'Active', y = top5_active.index, height = 600, color = 'Active', orientation = 'h',
             color_continuous_scale = ['paleturquoise','blue'], title = 'Top 5 Active Cases Countries')
fig4.show()

# Top 5 deaths countries (h-Bar plot)

top5_deaths = pd.DataFrame(data.groupby('Country')['Deaths'].sum().nlargest(5).sort_values(ascending = True))
fig2 = px.bar(top5_deaths, x = 'Deaths', y = top5_deaths.index, height = 600, color = 'Deaths', orientation = 'h',
            color_continuous_scale = ['deepskyblue','red'], title = 'Top 5 Death Cases Countries')
fig2.show()

# Top 5 recovered countries (Bar plot)

top5_recovered = pd.DataFrame(data.groupby('Country')['Recovered'].sum().nlargest(5).sort_values(ascending = False))
fig3 = px.bar(top5_recovered, x = top5_recovered.index, y = 'Recovered', height = 600, color = 'Recovered',
             title = 'Top 5 Recovered Cases Countries', color_continuous_scale = px.colors.sequential.Viridis)
fig3.show()


# Most affected states/provinces in largely affected countries
# Here we are going to extract top 4 affected countries' states data and plot it!

# Firstly, aggregating data with our dataset :
# Russia can be used to display the top affected states of Russia
topstates_russia = data['Country'] == 'Russia'
topstates_russia = data[topstates_russia].nlargest(5, 'Confirmed')

# Let's plot!

# Top states in Russia
fig6 = go.Figure(data = [
    go.Bar(name = 'Recovered Cases', x = topstates_russia['State'], y = topstates_russia['Recovered']),
    go.Bar(name = 'Active Cases', x = topstates_russia['State'], y = topstates_russia['Active']),
    go.Bar(name = 'Death Cases', x = topstates_russia['State'], y = topstates_russia['Deaths'])
])
fig6.update_layout(title = 'Most Affected States in Russia', barmode = 'stack', height = 600)
fig6.show()
    






