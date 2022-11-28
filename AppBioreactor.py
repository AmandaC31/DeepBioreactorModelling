import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from models import Example, COLUMN_NAMES

INPUT_COLUMNS = ["DO (mg/L)", "NO3 (mol/L)", "NH4+ (mol/L)", "H+ (mol/L)"]

EXAMPLE_FILES = {
    "Example 1": " 2.5333 54.3444 152.4775 230.2444 10.613 9.0738 7.3795.txt",
    "Example 2": "17.3849 24.8445 299.8846 238.6679 16.4459 12.9376 5.6324.txt",
    "Example 3": " 19.6928 132.1088 196.1891 405.7093 44.7409 6.1851 21.0619.txt",
    "Example 4": " 23.0925 96.1212 78.9769 68.371 56.4159 11.0712 16.1851.txt",
    "Example 5": " 31.3123 45.7654 357.4069 339.8457 17.9782 7.3822 5.139.txt",
    "Example 6": "40.7401 21.357 319.2671 104.6469 20.7508 7.8462 29.0392.txt"
}

EXAMPLE_SOLUTIONS = {
    "Example 1": [54.3444, 230.2444, 10.613, 9.0738, 7.3795],
    "Example 2": [24.8445, 238.6679, 16.4459, 12.9376, 5.6324],
    "Example 3": [132.1088, 405.7093, 44.7409, 6.1851, 21.0619],
    "Example 4": [96.1212, 68.371, 56.4159, 11.0712, 16.1851],
    "Example 5": [45.7654, 339.8457, 17.9782, 7.3822, 5.139],
    "Example 6": [21.357, 104.6469, 20.7508, 7.8462, 29.0392]
}

# defining variables ahead of the program to not break anything
input_df = None
DO_col = 0
NO3_col = 1
NH4_col = 2
MH_col = 3

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
st.sidebar.markdown("""
If you don't have your own file to upload you can try this beautiful one: 
[Example File](https://raw.githubusercontent.com/AmandaC31/DeepBioreactorModelling/master/Example1.csv)
""")

if uploaded_file is not None:
    if st.sidebar.checkbox('File with header?'):
        input_df = pd.read_csv(uploaded_file)
    else:
        input_df = pd.read_csv(uploaded_file, header=None)

else:
    example = st.sidebar.selectbox(label='Or select an example file',
                                   options=(
                                       'Example 1', 'Example 2', 'Example 3', 'Example 4', 'Example 5', 'Example 6'))
    input_df = pd.read_csv(EXAMPLE_FILES[example], names=INPUT_COLUMNS)


DO_col = st.sidebar.number_input(
    'Column of Dissolved Oxygen (mg/L) (1st=0): ', min_value=0, max_value=512, value=0, step=1
)
NO3_col = st.sidebar.number_input('Column of NO3 (mol/L): ', min_value=0, max_value=512, value=1, step=1)
NH4_col = st.sidebar.number_input('Column of NH4 (mol/L): ', min_value=0, max_value=512, value=2, step=1)
MH_col = st.sidebar.number_input('Column of H+ (mol/L): ', min_value=0, max_value=512, value=3, step=1)
time = np.arange(0.25, 24.25, 0.25)

try:
    assert not (
            DO_col == NO3_col or DO_col == NH4_col or DO_col == MH_col or NO3_col == NH4_col or NO3_col == MH_col or
            NH4_col == MH_col
    )

except AssertionError:
    st.sidebar.write(Warning("You cannot have two different variables in the same column. \n"
                             "For the input data shape we expect (samples, variables)"))

try:
    assert (DO_col == 0 and NO3_col == 1 and NH4_col == 2 and MH_col == 3)

except AssertionError:
    st.write(Warning("When using examples columns need to be the following: Dissolved Oxygen Column = 0, "
    "NO3 Column = 1, NH4 Column = 2, H+ Column = 3"))


# 1. display recorded data from csv file table and graph
st.header('Your bioreactor recorded data ')
st.write("Currently using the example file selected, upload your dataset to see your results")
if input_df is not None:
    if st.checkbox('Show dataset'):
        st.subheader('Recorded for a 24 hour period')
        st.write(input_df[:96])

    st.subheader('Dissolved Oxygen Concentration')
    fig1, ax1 = plt.subplots()
    ax1.plot(time, input_df.iloc[:96, DO_col])
    ax1.set(xlabel="Time (hours)", ylabel="DO (mg/L)")
    st.pyplot(fig1)

    st.subheader('Nitrate Concentration')
    if st.checkbox('Show -log(mol/L)'):
        fig2, ax2 = plt.subplots()
        ax2.plot(time, -np.log10(input_df.iloc[:96, NO3_col].to_numpy()))
        ax2.set(xlabel="Time (hours)", ylabel="NO3 (-log(mol/L))")
        st.pyplot(fig2)
    else:
        fig2, ax2 = plt.subplots()
        ax2.plot(time, input_df.iloc[:96, NO3_col])
        ax2.set(xlabel="Time (hours)", ylabel="NO3 (mol/L)")
        st.pyplot(fig2)

    st.subheader('Ammonia Concentration')
    if st.checkbox('Show -log(mol/L)'):
        fig3, ax3 = plt.subplots()
        ax3.plot(time, -np.log10(input_df.iloc[:96, NH4_col].to_numpy()))
        ax3.set(xlabel="Time (hours)", ylabel="NH4+ (-log(mol/L))")
        st.pyplot(fig3)
    else:
        fig3, ax3 = plt.subplots()
        ax3.plot(time, input_df.iloc[:96, NH4_col])
        ax3.set(xlabel="Time (hours)", ylabel="NH4+ (mol/L)")
        st.pyplot(fig3)

    st.subheader('Hydrogen Ion Concentration')
    if st.checkbox('Show pH'):
        fig4, ax4 = plt.subplots()
        ax4.plot(time, -np.log10(input_df.iloc[:96, MH_col].to_numpy()))
        ax4.set(xlabel="Time (hours)", ylabel="pH (-log(mol/L))")
        st.pyplot(fig4)
    else:
        fig4, ax4 = plt.subplots()
        ax4.plot(time, input_df.iloc[:96, MH_col])
        ax4.set(xlabel="Time (hours)", ylabel="H+ (mol/L)")
        st.pyplot(fig4)
else:
    st.write('Awaiting CSV file to be uploaded.')

# 2. Prediction of feedstocks parameters
st.header('Prediction of feedstock parameters')
st.markdown("""
    Based on your recorded data, your feedstock characteristics are the following: 
    """)
prediction_example = Example(input_df, DO_col=DO_col, NO3_col=NO3_col, NH4_col=NH4_col, MH_col=MH_col)
st.write(prediction_example.predict_())

if uploaded_file is None:
    st.write('Awaiting CSV file to be uploaded. Using example files.')

    st.header('Known Input-Characteristics')
    st.markdown("""
            Below are displayed the actual data for feedstocks characteristics so you can compare with the prediction. 
            """)

    # Reading feedstock characteristics for examples files
    true_vals = pd.DataFrame([EXAMPLE_SOLUTIONS[example]], columns=COLUMN_NAMES[1:])
    st.write(true_vals)

st.markdown("""
Data are expressed in the following mg/L
""")
