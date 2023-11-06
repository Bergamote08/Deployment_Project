## Deployment_Project_Getaround

GetAround is a platform similar to Airbnb, but for cars, allowing individuals to rent cars for a few hours or days. Founded in 2009, it has experienced rapid growth, with over 5 million users and approximately 20,000 cars available worldwide in 2019. The challenge is to analyze the issue of delays in returning rented cars. These delays can lead to problems for the next drivers and affect the owners' revenue. To address this problem, GetAround wishes to implement a minimum time interval between two rentals but needs to determine the duration of this interval and which cars should be affected. To make this decision, GetAround requires data analysis, including the impact on owners' revenue, the number of affected rentals, the frequency of delays, and the number of problematic cases resolved based on the chosen parameters.

In addition to these analyses, a data science team is working on price optimization using machine learning and requires an endpoint to provide pricing forecasts. To successfully complete this project, it is recommended to build a dashboard, develop an API endpoint for forecasts, and host the API online.

This document provides instruction to deploy the dashboard and API

## Web Dashboard
The Dashboard is published on streamlit. It gives information concerning the delay analysis.
The code for our Dashboard can be found in the "Dashboard" section of this repo and hosted locally using the following command : streamlit run app.py

## API
The API was build to provide an endpoint for pricing forecast.
The code for our API can be found in the "API" section of this repo and hosted locally using the following command : python api.py

## Author
I would like to credit Caroline Mathius and Yann Vii, as I used his GitHub repository as a reference.
