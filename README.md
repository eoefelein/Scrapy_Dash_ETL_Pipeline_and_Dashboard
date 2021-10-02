# Scrapy_Dash_ETL_Pipeline_and_Dashboard
Using the Scrapy and Selenium frameworks, this project reads in data on tiny home listings and stores them to a PostgreSQL database. The notebook linked here (https://nbviewer.jupyter.org/github/eoefelein/Scrapy_Dash_ETL_Pipeline_and_Dashboard/blob/main/Tiny_House_SQL_Analysis.ipynb) contains the project data analysis, conducted in SQL. Finally, the data is analyzed using clustering and spatial correlation techniques using the Local Moran’s I statistic to produce the dashboard linked here: https://tiny-house-dashboard.uc.r.appspot.com/ 

The first map consists of four layers, with the layer labeled General Clusters displaying where tiny homes are densely concentrated. The price, property_type and area feature layers cluster homes by each named variable using K_Means. The states which are outlined in that feature layer's color indicate areas where the clustered variable is spatially correlated (meaning similar objects are close together). This was calculated using the Local Spatial Autocorrelation (LISAs) Local Moran’s I statistic.

This project is also featured in this article (https://towardsdatascience.com/structuring-your-dash-app-e33d8e70133e), where Edward Krueger and I explain how to correctly structure and format your Dash App for pain free deployment to the Google Cloud Platform. Stay tuned for our upcoming article on how to Dockerize and deploy a Dash app to Google's Cloud Run service.
