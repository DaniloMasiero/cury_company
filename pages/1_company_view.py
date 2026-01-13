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

st.set_page_config( page_title='Company View', page_icon='📈', layout='wide')

# ------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------
def country_maps ( df1 ):
    columns = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    columns_groupby = ['City', 'Road_traffic_density']
    data_plot = df1.loc[:, columns].groupby(columns_groupby).median().reset_index()
    
    # Draw the map
    map = folium.Map()
    for index, location_info in data_plot.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
        location_info['Delivery_location_longitude']],
        popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
        
    folium_static(map , width=1024, height=600)

def order_share_by_week ( df1 ):
    # Deliveries per week / Unique delivery persons per week
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    # chart
    fig = px.line(df_aux, x='week_of_year', y='order_by_delivery')

    return fig

def order_by_week( df1 ):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime("%U")
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    # chart
    fig = px.line(df_aux, x='week_of_year', y='ID')

    return fig

def traffic_order_city ( df1 ) :
    columns = ['ID', 'City', 'Road_traffic_density']
    df_aux = df.loc[:, columns].groupby(['City', 'Road_traffic_density']).count().reset_index()
    df_aux['perc_ID'] = 100 * (df_aux['ID'] / df_aux['ID'].sum())
    # chart
    fig = px.bar(df_aux, x='City', y='ID', color='Road_traffic_density', barmode='group')

    return fig

def traffic_order_share( df1 ):
    
    
    columns = ['ID', 'Road_traffic_density']
    df_aux = df1.loc[:, columns].groupby('Road_traffic_density').count().reset_index()
    df_aux['perc_ID'] = 100 * (df_aux['ID'] / df_aux['ID'].sum())
    # chart
    fig = px.pie(df_aux, values='perc_ID', names='Road_traffic_density')

    return fig

def order_metric( df1 ):
    
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    df_aux.columns = ['order_date', 'qty_deliveries']
    
    # chart
    fig = px.bar(df_aux, x='order_date', y='qty_deliveries')
    
    return fig

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

# ---------------------------------start of the code's logical structure---------------------------------

#------------------------------------------------------------------
#Import dataset
#------------------------------------------------------------------
df = pd.read_csv('train.csv')

#------------------------------------------------------------------
#Cleaning data
#------------------------------------------------------------------
df1 = clean_code( df )

# =================================================================
# Sidebar
# =================================================================
st.header('Marketplace - Client View')

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

# =================================================================
# Layout
# =================================================================
tab1,tab2,tab3 = st.tabs( ['Management View', 'Tactical View', 'Geographic View'] )

with tab1:
    with st.container():
        # Number of orders per day
        st.header('Orders by day')
        fig = order_metric( df1 )
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1,col2 = st.columns(2)
        
        with col1:
            fig = traffic_order_share ( df1 )
            # Distribution of orders by traffic type
            st.header('Traffic order share')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2: 
            # Comparison of order volume by city and traffic type
            st.header('Traffic order city')
            fig = traffic_order_city ( df1 )
            st.plotly_chart(fig, use_container_width=True)
            
with tab2:
    with st.container():
        # Number of orders per week
        st.header('Orders by week')
        fig = order_by_week ( df1 )
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        st.header('Orders per delivery person per week')
        # Number of orders per delivery person per week
        fig = order_share_by_week ( df1 )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('# Country Map')
    # The central location of each city by traffic type
    country_maps ( df1 )

    



    