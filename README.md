# 	:bicyclist: Prediction demand Bicimad
Final Project  Master in Data Science (KSchool 2021-2022)


## :dart: Objective

The main objective of this project is to analyze and predict the hourly demand for Bicimad public service, building an interactive platform, to be used as a dashboard for bicimad's strategic and operational decision making, identifying demand patterns and predicting demand 14 days in advance, by area of madrid (divided by postal code) and globally.

## :memo: Instructions to run the project
First you need to download all the datasets available in the folder of **Data / Raw data**  and save them in the same folder as the jupyter notebooks.
Some datasets are downloaded via a google drive link, due to the size of these files. 
One of them is a zip file, containing one file per month, the file must be unzipped in the same folder as the notebooks and the other files.
All the libraries needed to execute the notebooks are in the file requirements.txt

All the notebooks are available on the folder Notebooks of the repo. They are:

 1. Exploring and preparing the data -> preparing and converting the raw data into datasets for the models
 2. Exploratory Data Analysis -> analyzing the data created on the first notebook (patterns in demand and demand per stations)
 3. Models for global demand -> machine learning models to analyze the aggregated demand of the service
 4. Models demand per zones -> machine learning models to analyze the demand per zone of Madrid

The data located in the file Data/processed data are files that are generated running the notebooks, and are used for other notebooks.
## 📊 Frontend

The frontend of the project has been developed with Streamlit [Click here to access the application](https://share.streamlit.io/paulamartinm/bicimad_prevision_tfm/main/Frontend/streamlit_app.py )

#### Menu 
At the top of the page is the menu (1) where you can switch between the two dashboards.
![alt text](https://github.com/paulamartinm/bicimad_prevision_tfm/blob/main/Frontend/manual_user/menu-frontend.png "menu-frontend")

#### Prediction of demand
Forecast of bycicle demand per hour for the next 24 hours or 14 days. And information about stations.
Filters:

* Period: 24 hours / 14 days
* Type of visualization:
    * All stations: aggregated demand
    * Demand per zones: prediction for each zone for which demand has been modelled.

Depending on the type of visualization there are different filters available:

* Demand per zones:
    * Postal code
    * Comparison of all zones or individual zones

* All stations:
    * Model: different machine learning models or comparison between them

![alt text](https://github.com/paulamartinm/bicimad_prevision_tfm/blob/main/Frontend/manual_user/prediction-demand-I.png "prediction-demand-I")

![alt text](https://github.com/paulamartinm/bicimad_prevision_tfm/blob/main/Frontend/manual_user/prediction-demand-II.png "prediction-demand-II")

![alt text](https://github.com/paulamartinm/bicimad_prevision_tfm/blob/main/Frontend/manual_user/prediction-demand-III.png "prediction-demand-III")


#### Dashboard demand
Dashboard with information about historical data of demand.

Filters:
* Year
* Month
* Type of visualization: all stations or demand per zones
* Postal code (if demand per zones is selected)
* Bottom information: evolution of demand (shows the time series evolution of demand) or stations information (information about stations and location)

![alt text](https://github.com/paulamartinm/bicimad_prevision_tfm/blob/main/Frontend/manual_user/dashboard-demand-I.png "dashboard-demand-I")
