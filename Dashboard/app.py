import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import os
from PIL import Image

### Config
st.set_page_config(
    page_title="GetAround",
    page_icon="🚗",
    layout="wide"
)

### Load data
DATA_URL = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
delay_data = pd.read_excel(DATA_URL)

conditions = [
    (delay_data['delay_at_checkout_in_minutes'] <= 0),
    (delay_data['delay_at_checkout_in_minutes'] < 60),
    (delay_data['delay_at_checkout_in_minutes'] < 120),
    (delay_data['delay_at_checkout_in_minutes'] < 300),
    (delay_data['delay_at_checkout_in_minutes'] < 1440),
    (delay_data['delay_at_checkout_in_minutes'] >= 1440),
    (delay_data['delay_at_checkout_in_minutes'].isna())
]

labels = ['Early or On Time', '< 1 Hour', '1 to 2 Hours', '2 to 5 Hours', '5 to 24 Hours', '1 day or more', 'Unknown']
delay_data['delay'] = np.select(conditions, labels)

# Header
image = Image.open("logo.png")
st.image(image, width = 700)

# Title
st.title("Getaround Jedha Project : Delay Analysis 🕓 ")

#Description
st.markdown("""
    Welcome to this `streamlit` dashboard for the Getaround project. Here you will find analysis to help decide what is the best minimal delay between two rentals.
 
""")

@st.cache_data
def load_data(nrows):
    DATA_URL = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
    delay_data = pd.read_excel(DATA_URL)
    return delay_data

st.subheader("Load and showcase data")


data_load_state = st.text('Loading data...')
data = load_data(50)
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)    

st.subheader("Visualization")

checkin_type_counts = delay_data['checkin_type'].value_counts()
checkin_type_percentage = (checkin_type_counts / checkin_type_counts.sum()) * 100

fig1 = px.bar(
    x=checkin_type_counts.index,
    y=checkin_type_counts.values,
    title='Distribution of Checkin Types',
    labels={'x': 'Checkin Type', 'y': 'Count'}
)
fig1.update_traces(marker_color='skyblue')

percentage_text = [f'{p:.2f}%' for p in checkin_type_percentage]
fig1.update_traces(marker_color='skyblue', text=percentage_text, textposition='outside')

st.plotly_chart(fig1)


st.subheader("Analysis")
col1, col2 = st.columns(2)

    
with col1 :
    st.subheader("How often are drivers late for the next check-in?")

    # Build summary table
    # Calculate the number of total entries, late returns, on-time returns, and NaN
    total_entries = len(delay_data)
    late_returns_count = len(delay_data[delay_data['delay_at_checkout_in_minutes'] > 0])
    nan_count = delay_data['delay_at_checkout_in_minutes'].isna().sum()
    on_time_or_earlier_count = len(delay_data[delay_data['delay_at_checkout_in_minutes'] <= 0])

    # Calculate percentage for each category
    late_return_percentage = (late_returns_count / total_entries) * 100
    on_time_percentage = (on_time_or_earlier_count / total_entries) * 100
    NaN_percentage = (nan_count / total_entries) * 100

    # Display the results
    # Create a formatted string with line breaks
    formatted_text = (
    f"""Total Number of Entries: {total_entries}  
    Number of Late Returns: {late_returns_count}  
    Number of On Time or Earlier Returns: {on_time_or_earlier_count}  
    Number of NaN Values: {nan_count}  
    Percentage of Late Returns: {late_return_percentage:.2f}%  
    Percentage of On Time/Early Returns: {on_time_percentage:.2f}%  
    Percentage of NaN: {NaN_percentage:.2f}%"""
)

    # Use st.write to display the formatted text
st.write(formatted_text)

# Sub-section 2 : How does it impact the next driver ?
with col2:
    st.subheader("How does it impact the next driver ?")

    # Calculate the frequency of late check-ins
    late_checkins = delay_data[delay_data['delay_at_checkout_in_minutes'] > 0]
    late_checkin_frequency = (len(late_checkins) / len(delay_data)) * 100
    st.write("<u>Frequency of late check-ins</u>",unsafe_allow_html=True)
    st.write("Percentage of late check-ins:", f"{late_checkin_frequency:.2f}%")


# Histogram of delay distribution
    # Calculate the counts and percentages of each delay category
delay_counts = delay_data['delay'].value_counts()
delay_percentages = (delay_counts / delay_counts.sum()) * 100


# Create a histogram manually
fig2 = go.Figure(data=[
go.Bar(
    x=delay_counts.index,
    y=delay_counts,
    text=delay_percentages.round(2).astype(str) + '%',  # Add percentage to the text
    textposition='outside',  # Show text outside the bars
    marker=dict(color='lightblue'),  # Customize bar color
    )
])

# Customize the layout
fig2.update_layout(
    title='Distribution of Delays with Percentage Tags',
    xaxis=dict(title='Delay'),
        yaxis=dict(title='Count'),
        showlegend=False,
)
    # Show the chart on streamlit
st.plotly_chart(fig2)





### Side bar 
st.sidebar.header("Getaround Dashboard")
e = st.sidebar.empty()
e.write("")
st.sidebar.write("Made with 💖 by Charlotte A.")
