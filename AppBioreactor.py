import streamlit as st
import pandas as pd
from numpy.core.defchararray import strip

#import numpy as np
#import plotly.figure_factory as ff
#import matplotlib.pyplot as plt
from models import Example

input_df = None

st.title('Deep Learning for Bioreactor Modelling and Control-Optimization')
st.markdown("""
This app performs allows Bioreactor start up to determine their feedstock characteristics and 
 optimize their process through forecasting and control.
""")
#Displaying full data

st.sidebar.header('User Input file')
#st.sidebar.markdown('''
#[Example 1 CSV input file](https://raw.githubusercontent.com/AmandaC31/Bioreactor-Modelling/main/Example1.csv)

#[Example 2 CSV input file](https://raw.githubusercontent.com/AmandaC31/Bioreactor-Modelling/main/Example2.csv)

#[Example 3 CSV input file](https://raw.githubusercontent.com/AmandaC31/Bioreactor-Modelling/main/Example3.csv)

#''')
#with st.sidebar:

    #print(example_number)
#uploading csv file
uploaded_file = st.sidebar.file_uploader("Upload your CSV file with recorded data to display them and obtain your feedstock characteristics", type=["csv"])
if uploaded_file is not None:
   input_df = pd.read_csv(uploaded_file)
#elif not(example_number == 1234):
#   input_df = Example().example_data[example_number-1]
else:
    st.write("Select an example file to try:")
    example = st.sidebar.selectbox(label='Use Example',
                                   options=(  # '<None selected>',
                                       'Example 1', 'Example 2', 'Example 3'))
    # try:
    example_number = int(example.split(" ")[1])
    prepared = Example()
    st.sidebar.write(prepared.disp_example(example_number))
    input_df = prepared.display_data[example_number]

# 1. display recorded data from csv file table and graph
st.header('Your bioreactor recorded data ')
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
        st.line_chart( x="Time (hour)", y="pH", data=input_df)
    else :
        st.subheader('Hydrogen ion concentration')
        st.line_chart( x="Time (hour)", y="H+ (mol/L)", data=input_df)
else:
    st.write('Awaiting CSV file to be uploaded.')

# 2. Prediction of feedstocks parameters
st.header('Prediction of feedstock parameters')
if input_df is not None:
    st.markdown("""
    Based on your recorded data, your feedstock characteristics are the following: 
    """)
else:
    st.write('Awaiting CSV file to be uploaded.')







# Reads in saved prediction model
#load_clf = pickle.load(open('XXX.plk', 'rb'))

# Apply model to make predictions
#prediction = load_clf.predict(input_df)


#st.write([prediction])


# 3. Forecasting data

        #return features
#st.header('Forecasting')
#input_df_1 = user_input_features()
#st.write(input_df_1)

st.markdown("""
The forecasting option is still in progress and will soon be available!
""")




#df.hist()
#st.pyplot()


#st.area_chart(input_df["Days"])

