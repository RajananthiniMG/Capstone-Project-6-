from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelBinarizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import pickle
import streamlit as st
import re

st.set_page_config(
    page_title="Industrial Copper Modeling",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Welcome to Industrial Copper Modeling\n- [Get Help](https://www.extremelycoolapp.com/help)\n- [Report a Bug](https://www.extremelycoolapp.com/bug)"
    }
)

st.write("""
<div style='text-align:center'>
    <h1 style='color:#C909AA;'>Industrial Copper Modeling Application</h1>
</div>
""", unsafe_allow_html=True)


menu = option_menu(None,["Home","PREDICT SELLING PRICE", "PREDICT STATUS"],
        icons=['house', 'bar-chart-line-fill','chat-left-text'], 
        menu_icon="cast",
        default_index=0, 
        orientation="horizontal")


if menu == "Home":
    st.title('Welcome to Industrial Copper Modeling')
    st.write("""
    This application allows you to predict the selling price and status of industrial copper based on various input parameters. 
    Whether you're involved in the copper industry or interested in data-driven insights, this tool is designed to assist you.
    
    ### Key Features:
    - Predict selling price of industrial copper.
    - Predict status (e.g., won or lost) based on given attributes.
    - User-friendly interface for easy navigation and input.
    
    ### How to Use:
    - Select the desired prediction task from the menu.
    - Input relevant attributes such as quantity, thickness, width, etc.
    - Click the 'Predict' button to see the results.
    
    ### About Industrial Copper:
    Industrial copper plays a crucial role in various industries including manufacturing, construction, and electronics. 
    Predicting its selling price and status can help businesses make informed decisions and optimize their operations.
    
    ### Data Sources:
    The application utilizes proprietary datasets and industry-standard parameters for accurate predictions.
    
    ### Feedback and Support:
    Your feedback is valuable to us! If you encounter any issues or have suggestions for improvement, 
    please don't hesitate to reach out to us.
    
    ### Updates and Version History:
    Version 1.0: Initial release with basic prediction capabilities.
    
    ### Privacy Policy:
    This application does not collect any user data or use cookies. Your privacy is important to us.
    
    ### Terms of Use:
    By using this application, you agree to abide by the terms of use outlined in the [Terms of Use](#) section.
    
    """)

# Predict Selling Price Page
if menu == "PREDICT SELLING PRICE":

    #Here we declaring the possible values for the dropdown menus
    status_options = ['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM', 'Wonderful', 'Revised', 'Offered','Offerable']
    item_type_options = ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']
    country_options = [28., 25., 30., 32., 38., 78., 27., 77., 113., 79., 26., 39., 40., 84., 80., 107., 89.]
    application_options = [10., 41., 28., 59., 15., 4., 38., 56., 42., 26., 27., 19., 20., 66., 29., 22., 40., 25., 67.,
                           79., 3., 99., 2., 5., 39., 69., 70., 65., 58., 68.]
    product = ['611112', '611728', '628112', '628117', '628377', '640400', '640405', '640665',
               '611993', '929423819', '1282007633', '1332077137', '164141591', '164336407',
               '164337175', '1665572032', '1665572374', '1665584320', '1665584642', '1665584662',
               '1668701376', '1668701698', '1668701718', '1668701725', '1670798778', '1671863738',
               '1671876026', '1690738206', '1690738219', '1693867550', '1693867563', '1721130331', '1722207579']
    
    # Define the widgets for user input
    with st.container():
        col1, col3 = st.columns([5, 5])
        with col1:
            status = st.selectbox("Status", status_options, key=1)
            item_type = st.selectbox("Item Type", item_type_options, key=2)
            country = st.selectbox("Country", sorted(country_options), key=3)
            application = st.selectbox("Application", sorted(application_options), key=4)
            product_ref = st.selectbox("Product Reference", product, key=5)
       
        with col3:
            st.write(
                f'<h5 style="color:#ee4647;">NOTE: Min & Max given for reference, you can enter any value</h5>',
                unsafe_allow_html=True)
            quantity_tons = st.text_input("Enter Quantity Tons (Min:611728 & Max:1722207579)")
            thickness = st.text_input("Enter thickness (Min:0.18 & Max:400)")
            width = st.text_input("Enter width (Min:1, Max:2990)")
            customer_id = st.text_input("customer ID (Min:12458, Max:30408185)")
            
            
            submit_button = st.button(label="PREDICT SELLING PRICE")
            st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #004aad;
                    color: white;
                    width: 100%;
                }
                </style>
            """, unsafe_allow_html=True)

        flag = 0
        pattern = "^(?:\d+|\d*\.\d+)$"
        for i in [quantity_tons, thickness, width, customer_id]:
            if re.match(pattern, i):
                pass
            else:
                flag = 1
                break
                
        if submit_button and flag==1:
            if len(i)==0:
                st.write("please enter a valid number space not allowed")
            else:
                st.write("You have entered an invalid value: ",i)  
        elif submit_button and flag == 0:
            # Check if entered values exceed maximum limits
            if (float(quantity_tons) > 1722207579 or
                float(thickness) > 400 or
                float(width) > 2990 or
                float(customer_id) > 30408185):
                st.error("One or more input values exceed the maximum limit.")
            else:
                
                import pickle
                with open(r"C:\Users\rajan\OneDrive\Desktop\Copper ML\model.pkl", 'rb') as file:
                    loaded_model = pickle.load(file)
                with open(r'C:\Users\rajan\OneDrive\Desktop\Copper ML\scaler.pkl', 'rb') as f:
                    scaler_loaded = pickle.load(f)
                with open(r"C:\Users\rajan\OneDrive\Desktop\Copper ML\ohe_item_type.pkl", 'rb') as f:
                    t_loaded = pickle.load(f)
                with open(r"C:\Users\rajan\OneDrive\Desktop\Copper ML\ohe_status.pkl", 'rb') as f:
                    s_loaded = pickle.load(f)

                new_sample= np.array([[np.log(float(quantity_tons)),application,np.log(float(thickness)),float(width),country,float(customer_id),int(product_ref),item_type,status]])
                new_sample_ohe = t_loaded.transform(new_sample[:, [7]]).toarray()
                new_sample_be = s_loaded.transform(new_sample[:, [8]]).toarray()
                new_sample = np.concatenate((new_sample[:, [0,1,2, 3, 4, 5, 6,]], new_sample_ohe, new_sample_be), axis=1)
                new_sample1 = scaler_loaded.transform(new_sample)
                new_pred = loaded_model.predict(new_sample1)[0]
                st.write('## :green[Predicted selling price:] ', np.exp(new_pred))

# Predict Status Page
if menu == "PREDICT STATUS":

    #Here we declaring the possible values for the dropdown menus
    status_options = ['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM', 'Wonderful', 'Revised', 'Offered','Offerable']
    item_type_options = ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']
    country_options = [28., 25., 30., 32., 38., 78., 27., 77., 113., 79., 26., 39., 40., 84., 80., 107., 89.]
    application_options = [10., 41., 28., 59., 15., 4., 38., 56., 42., 26., 27., 19., 20., 66., 29., 22., 40., 25., 67.,
                           79., 3., 99., 2., 5., 39., 69., 70., 65., 58., 68.]
    product = ['611112', '611728', '628112', '628117', '628377', '640400', '640405', '640665',
               '611993', '929423819', '1282007633', '1332077137', '164141591', '164336407',
               '164337175', '1665572032', '1665572374', '1665584320', '1665584642', '1665584662',
               '1668701376', '1668701698', '1668701718', '1668701725', '1670798778', '1671863738',
               '1671876026', '1690738206', '1690738219', '1693867550', '1693867563', '1721130331', '1722207579']
    
     # Define the widgets for user input
    with st.container():
        col1, col3 = st.columns([5, 5])
        with col1:
            cquantity_tons = st.text_input("Enter Quantity Tons (Min:611728 & Max:1722207579)")
            cthickness = st.text_input("Enter thickness (Min:0.18 & Max:400)")
            cwidth = st.text_input("Enter width (Min:1, Max:2990)")
            ccustomer_id = st.text_input("customer ID (Min:12458, Max:30408185)")
            cselling = st.text_input("Selling Price (Min:1, Max:100001015)")

        with col3:
            st.write(' ')
            citem_type = st.selectbox("Item Type", item_type_options, key=21)
            ccountry = st.selectbox("Country", sorted(country_options), key=31)
            capplication = st.selectbox("Application", sorted(application_options), key=41)
            cproduct_ref = st.selectbox("Product Reference", product, key=51)
            csubmit_button = st.button(label="PREDICT STATUS")

        cflag = 0
        pattern = "^(?:\d+|\d*\.\d+)$"
        for k in [cquantity_tons, cthickness, cwidth, ccustomer_id, cselling]:
            if re.match(pattern, k):
                pass
            else:
                cflag = 1
                break

    if csubmit_button and cflag == 1:
        if len(k) == 0:
            st.write("please enter a valid number space not allowed")
        else:
            st.write("You have entered an invalid value: ", k)
    elif csubmit_button and cflag == 0:
            # Check if entered values exceed maximum limits
            if (float(cquantity_tons) > 1722207579 or
                float(cthickness) > 400 or
                float(cwidth) > 2990 or
                float(ccustomer_id) > 30408185):
                st.error("One or more input values exceed the maximum limit.")
            else:
                import pickle

                with open(r"C:\Users\rajan\OneDrive\Desktop\Copper ML\cmodel.pkl", 'rb') as file:
                    cloaded_model = pickle.load(file)

                with open(r"C:\Users\rajan\OneDrive\Desktop\Copper ML\cscaler.pkl", 'rb') as f:
                    cscaler_loaded = pickle.load(f)

                with open(r"C:\Users\rajan\OneDrive\Desktop\Copper ML\cohe_item_type.pkl", 'rb') as f:
                    ct_loaded = pickle.load(f)

                # Predict the status for a new sample
                new_sample = np.array([[np.log(float(cquantity_tons)), np.log(float(cselling)), capplication,np.log(float(cthickness)), float(cwidth), ccountry, int(ccustomer_id), int(cproduct_ref),citem_type]])
                new_sample_ohe = ct_loaded.transform(new_sample[:, [8]]).toarray()
                new_sample = np.concatenate((new_sample[:, [0, 1, 2, 3, 4, 5, 6, 7]], new_sample_ohe), axis=1)
                new_sample = cscaler_loaded.transform(new_sample)
                new_pred = cloaded_model.predict(new_sample)
                if new_pred == 1:
                    st.write('## :green[The Status is Won] ')
                else:
                    st.write('## :red[The status is Lost] ')

st.write(f'<h6 style="color:#ee4647;">App Created by M G Rajananthini</h6>', unsafe_allow_html=True)

