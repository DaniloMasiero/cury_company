import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🏠',
)


image_path= 'fast-shipping.png'
image = Image.open(image_path)
st.sidebar.image( image, width=120)

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( '''---''' )

st.write('# Cury Company Growth Dashboard')

st.markdown(
    '''
    Growth Dashboard built to track the growth metrics of Delivery Drivers and Restaurants.
    ### How to use this Growth Dashboard?
    - Business Vision:
      - General Vision: General behavioral metrics.
      - Tactical Vision: Weekly growth indicators.
      - Geographic Vision: Geolocation insights.
    - Strategic Vision:
      - Tracking weekly growth indicators
    - Guarantees Vision:
      - Weekly growth indicators for restaurants
    ### How to Ask for Help
    - Linkedin
      - https://www.linkedin.com/in/danilo-masiero/
      '''
)