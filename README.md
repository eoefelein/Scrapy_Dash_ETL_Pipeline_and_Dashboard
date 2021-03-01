# Scrapy_Dash_ETL_Pipeline_and_Dashboard
Implementing Scrapy, this project reads in data on tiny house listings and stores to a Postgres SQL database. That data is then cleaned and explored to produce the dashboard linked here. 

The first map consists of four layers, with the layer labeled General Clusters, displaying where tiny homes are densely concentrated. The price, property_type and area layers clusters homes by each named variable using K_Means. The states which are outlined in that layer's color indicate the clustered variable is spatially correlated. Meaning similar objects are close together. This was calculated using the Local Spatial Autocorrelation (LISAs) Local Moran’s I statistic.
