import streamlit as st
import pandas as pd
from models import Example

input_df = None

st.title('Deep Learning for Bioreactor Modelling and Control-Optimization')
st.markdown("""
This app performs allows Bioreactor start up to determine their feedstock characteristics and 
 optimize their process through forecasting and control.
""")

# Displaying full data
st.sidebar.header('User Input file')

# uploading csv file
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV file with recorded data to display them and obtain your feedstock characteristics", type=["csv"])
number = st.sidebar.number_input('Select a number between 0 and 10', min_value=0, max_value=10, value=0, step=1)



if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
#   input_df = Example().example_data[example_number-1]
else:
    example = st.sidebar.selectbox(label='Or select an example file',
                                   options=(
                                       'Example 1', 'Example 2', 'Example 3'))
    if 'Example 1' in example:
        input_df = pd.read_csv("Example1.csv")
    elif 'Example 2' in example:
        input_df = pd.read_csv("Example2.csv")
    elif 'Example 3' in example:
        input_df = pd.read_csv("Example3.csv")
    # try:
    # example_number = int(example.split(" ")[1])
    # prepared = Example()
    # st.sidebar.write(prepared.disp_example(example_number))
    # input_df = prepared.display_data[example_number]

# 1. display recorded data from csv file table and graph
st.header('Your bioreactor recorded data ')
st.write("Currently using the example file selected, upload your dataset to see your results")
if input_df is not None:
    if st.checkbox('Show dataset'):
        st.subheader('Recorded for a 24 hour period')
        st.write(input_df[:96])
    st.subheader('Dissolved oxygen')
    st.line_chart(x="Time (hour)", y="DO (mol/L)", data=input_df)
    st.subheader('Nitrate concentration')
    st.line_chart(x="Time (hour)", y="NO3 (mol/L)", data=input_df)
    st.subheader('Ammonia concentration')
    st.line_chart(x="Time (hour)", y="NH4+ (mol/L)", data=input_df)
    if st.checkbox('Show pH'):
        st.subheader('pH')
        st.line_chart(x="Time (hour)", y="pH", data=input_df)
    else:
        st.subheader('Hydrogen ion concentration')
        st.line_chart(x="Time (hour)", y="H+ (mol/L)", data=input_df)
else:
    st.write('Awaiting CSV file to be uploaded.')

# 2. Prediction of feedstocks parameters
st.header('Prediction of feedstock parameters')
st.markdown("""
    Based on your recorded data, your feedstock characteristics are the following: 
    """)
prediction_example = Example(input_df)
st.write(prediction_example.predict_())

if uploaded_file is None:
    st.write('Awaiting CSV file to be uploaded. Using example files.')

    st.header('Known Input-Characteristics')
    st.markdown("""
            Below are displayed the actual data for feedstocks characteristics so you can compare with the prediction. 
            """)

    # Reading feedstock characteristics for examples files
    ex1_df = pd.read_csv("feedstock1.csv")
    ex2_df = pd.read_csv("feedstock2.csv")
    ex3_df = pd.read_csv("feedstock3.csv")

    # Displaying feedstock characteristics depending on the example file chosen by the user
    if 'Example 1' in example:
        st.write(ex1_df)
    elif 'Example 2' in example:
        st.write(ex2_df)
    elif 'Example 3' in example:
        st.write(ex3_df)

st.markdown("""
Data are expressed in UNIT (mol/L)

S_SASin	= Readily biodegradable substrate

X_SASin	= Slowly biodegradable organic matter concentration

S_NHASin = Soluble ammonia nitrogen concentration

S_NDASin = Soluble biodegradable organic nitrogen concentration

X_NDASin = Particulate (slowly) biodegradable organic nitrogen
""")
