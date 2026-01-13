#libraries
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
import folium
import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Delivery View', page_icon='🛵', layout='wide')

# ------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------
def top_delivery ( df1 , top_asc ):

    df2 = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).max().sort_values(['City','Time_taken(min)'], ascending=top_asc).reset_index()
    
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

    return df3


def clean_code( df1 ):
    '''This function is responsible for cleaning the dataframe
    
        Types of cleaning:
        
        1. Removal of NaN data
        2. Change of data column type
        3. Removal of spaces from text variables
        4. Formatting of the date column
        5. Cleaning of the time column (removal of text from the numeric variable)

        Input: Dataframe
        Output: Dataframe
    '''
    #Cleaning
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    linhas_selecionadas = (df1['multiple_deliveries']) != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    df1.loc[:,'ID'] = df1.loc[:,'ID'].str.strip()
    df1.loc[:,'Road_traffic_density'] = df1.loc[:,'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
    df1.loc[:,'City'] = df1.loc[:,'City'].str.strip()
    df1.loc[:,'Festival'] = df1.loc[:,'Festival'].str.strip()
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1
    
# ------------------------------------------------------------------
#Import dataset
# ------------------------------------------------------------------
df = pd.read_csv('train.csv')

# ------------------------------------------------------------------
# Cleaning dataset
# ------------------------------------------------------------------
df1 = clean_code ( df )


# ================================================
# Sidebar
# ================================================
st.header('Marketplace - Delivery View')

image_path= 'fast-shipping.png'
image = Image.open(image_path)
st.sidebar.image( image, width=120)

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( '''---''' )

st.sidebar.markdown( '## Select a limit date')

date_slider = st.sidebar.slider(
    'What is the limit date?',
    value=datetime( 2022, 4 , 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='YYYY-MM-DD' )
st.sidebar.markdown( '''---''' )

traffic_options = st.sidebar.multiselect(
    'Wich traffic condition?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])
st.sidebar.markdown( '''---''' )

st.sidebar.markdown( '### Powered by Danilo Masiero' )

# Date filter
lines = df1['Order_Date'] < date_slider
df1 = df1.loc[lines,:]

# Traffic filter
lines = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[lines,:]

# ================================================
# Layout
# ================================================
tab1, tab2, tab3 = st.tabs (['Management View','_','_'] )

with tab1:
    with st. container():
        st.title('Overall Metrics')

        col1, col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:  
            # Oldest delivery person 
            oldest_age = df1.loc[:,"Delivery_person_Age"].max()
            col1.metric('Oldest age', oldest_age)

        with col2:
            # Youngest delivery person
            youngest_age = df1.loc[:,"Delivery_person_Age"].min()
            col2.metric('Youngest age',youngest_age)
            
        with col3:
            # Best vehicle condition
            best_condition = df1.loc[:,"Vehicle_condition"].max()
            col3.metric('Best vehicle condition', best_condition)

        with col4:
            # Worst vehicle condition
            worst_condition = df1.loc[:,"Vehicle_condition"].min()
            col4.metric('Worst vehicle condition',worst_condition)

    with st. container():
        st.markdown( '''---''' )
        st.title('Ratings')

        col1,col2=st.columns(2)
        with col1:
            st.markdown('##### Average rating by delivery person')
            # Average rating by delivery person
            df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
            df_avg_ratings_per_deliver.columns = ['delivery_person_id', 'avg_rating']
            st.dataframe(df_avg_ratings_per_deliver)

        with col2:
            st.markdown('##### Average rating by traffic type')
            # Average rating and standard deviation by traffic type
            df_avg_std_rating_by_traffic = df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean','std']})
            df_avg_std_rating_by_traffic.columns = ['delivery_mean','delivery_std']
            df_avg_std_rating_by_traffic.reset_index()
            st.dataframe(df_avg_std_rating_by_traffic)
            
            st.markdown('##### Average rating by weather conditions')
            # Average rating and standard deviation by weather conditions
            df_avg_std_rating_by_weather = df1.loc[:,['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean','std']})
            df_avg_std_rating_by_weather.columns = ['delivery_mean','delivery_std']
            df_avg_std_rating_by_weather.reset_index()
            st.dataframe(df_avg_std_rating_by_weather)

    with st.container():
        st.markdown( '''---''' )
        st.title('Delivery speed')

        col1,col2=st.columns(2)
        with col1:
            st.markdown('##### Top fastest delivery persons')
            # Top 10 fastest delivery persons by city
            df3 = top_delivery ( df1, top_asc=True )
            st.dataframe( df3 )

        with col2:
            st.markdown('##### Top slowest delivery persons')
            # Top 10 slowest delivery persons by city
            df3 = top_delivery ( df1, top_asc=False )
            st.dataframe( df3 )
            