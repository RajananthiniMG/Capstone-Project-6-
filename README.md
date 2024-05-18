# Capstone-Project-6-
# Industrial Copper Modeling Application

## Overview
Welcome to the Industrial Copper Modeling Application! This Streamlit app provides predictive modeling capabilities for industrial copper based on various input parameters. Whether you need to predict the selling price or status of copper orders, this tool has you covered.

## Features
- Predict the selling price of industrial copper based on quantity, thickness, width, etc.
- Predict the status (e.g., won or lost) of copper orders using machine learning models.
- User-friendly interface for easy navigation and input.
- Real-time predictions with fast response times.

## How to Use
1. Install the necessary dependencies: Make sure you have Python installed on your system along with the required libraries listed in `requirements.txt`.
2. Clone the repository: Use `git clone` to download the project files to your local machine.
3. Navigate to the project directory: Use `cd` command to go to the directory where you cloned the repository.
4. Run the Streamlit app: Execute `streamlit run copperml.py` in your terminal to start the Streamlit server.
5. Access the app: Open the provided URL (usually `http://localhost:8501`) in your web browser to access the app.

## File Structure
- `copperml.py`: Main Python script containing the Streamlit application code.
- `requirements.txt`: List of Python dependencies required to run the application.

## Usage
- Once the app is running, you'll see a navigation menu with options to select:
  - **Home**: Overview of the application and its features.
  - **Predict Selling Price**: Interface for predicting the selling price of industrial copper.
  - **Predict Status**: Interface for predicting the status of copper orders.
- Select the desired option and input the relevant parameters.
- Click the "Predict" button to see the results.

## Dependencies
- Streamlit: For building the web application interface.
- Pandas, NumPy: For data manipulation and processing.
- Scikit-learn: For machine learning models and preprocessing.
- Pickle: For loading pre-trained models.
- Re: For regular expression pattern matching.
