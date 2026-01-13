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
import numpy as np

st.set_page_config( page_title='Restaurant View', page_icon='🍽️', layout='wide')

# ------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------
def avg_std_time_on_traffic( df1 ):

    cols = ['City' , 'Time_taken(min)' , 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby( ['City','Road_traffic_density']).agg ( {'Time_taken(min)' : ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux,path=['City','Road_traffic_density'],values='avg_time',color='std_time',color_continuous_scale='RdBu',color_continuous_midpoint=np.average(df_aux['std_time']))

    return fig

def avg_std_time_graph( df1 ):
    cols = ['City' , 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby( 'City').agg ( {'Time_taken(min)' : ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace( go.Bar(name='Control',x=df_aux['City'],y=df_aux['avg_time'],error_y=dict(type='data',array=df_aux['std_time'])))
    fig.update_layout(barmode='group')

    return fig


def avg_std_time_delivery( df1, festival, op):
    '''
    This function calculates the average time and standard deviation of delivery time.
    Parameters:
        Input:
            - df: Dataframe with the necessary data for the calculation
            - op: Type of operation that needs to be calculated:
                    'avg_time': Calculates the average time
                    'std_time': Calculates the standard deviation of time.
        Output:
            - df: Dataframe with 2 columns and 1 row.  
    '''
    cols = ['Time_taken(min)' , 'Festival']
    df_aux = df1.loc[:, cols].groupby( ['Festival']).agg ( {'Time_taken(min)' : ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op],2)

    return df_aux

def distance ( df1, fig ):
        if fig == False:
            from haversine import haversine
            cols = [ 'Delivery_location_latitude' , 'Delivery_location_longitude' , 'Restaurant_latitude' , 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine( 
                                               (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                               (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            
            avg_distance = np.round(df1['distance'].mean(),2)
            return avg_distance

        else:
            from haversine import haversine
            cols = [ 'Delivery_location_latitude' , 'Delivery_location_longitude' , 'Restaurant_latitude' , 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine( 
                                               (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                               (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            
            avg_distance = df1.loc[:, ['City','distance']].groupby('City').mean().reset_index()
            fig = go.Figure( data= [go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])

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
# ------------------------------------------------------------------
#Import
# ------------------------------------------------------------------
df = pd.read_csv('train.csv')

# ------------------------------------------------------------------
# Cleaning dataset
# ------------------------------------------------------------------
df1 = clean_code ( df )

# ================================================
# Sidebar
# ================================================
st.header('Marketplace - Restaurant View')

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
    with st.container():
        st.title('Overall Metrics')

        col1,col2,col3,col4,col5,col6 = st.columns(6)
        with col1:

            delivery_unique = len ( df1.loc[:, 'Delivery_person_ID'].unique() )
            col1.metric('Delivery',delivery_unique)
            
        with col2:
            avg_distance = distance ( df1 , fig=False)
            col2.metric('Avg distance',avg_distance)
            
        with col3:
            df_aux = avg_std_time_delivery( df1, 'Yes', 'avg_time')
            col3.metric('Avg delivery',df_aux)
            
        with col4:
            df_aux = avg_std_time_delivery( df1, 'Yes', 'std_time')
            col4.metric('Std delivery',df_aux)
            
        with col5:
            f_aux = avg_std_time_delivery( df1, 'No', 'avg_time')
            col5.metric('Avg delivery',df_aux)
           
        with col6:
            df_aux = avg_std_time_delivery( df1, 'No', 'std_time')
            col6.metric('Std delivery',df_aux)         

    with st.container():
        st.markdown( '''---''' )
        st.title('Average delivery time by city')
        col1,col2 = st.columns(2)

        with col1:
            fig = avg_std_time_graph( df1 )
            st.plotly_chart(fig)

        with col2:
            cols = ['City' , 'Time_taken(min)' , 'Road_traffic_density']
            df_aux = df1.loc[:, cols].groupby( ['City','Road_traffic_density']).agg ( {'Time_taken(min)' : ['mean', 'std']} )
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)

        

    with st.container():
        st.markdown( '''---''' )
        st.title('Distribution time')
        
        col1,col2 = st.columns(2)
        with col1:
            fig = distance( df1, fig=True)
            st.plotly_chart(fig)
            
        with col2:
            fig = avg_std_time_on_traffic( df1 )
            st.plotly_chart(fig)







