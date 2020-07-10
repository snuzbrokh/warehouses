# Warehouse Lease Rates: WebScraping Project

This project focuses on exploratory data analysis on warehouse lease data obtained from an online leasing site. 
The scope covers all 50 states with over 9,000 unique listings. 

[Link to the blog post](https://nycdatascience.com/blog/student-works/warehouse-leasing/)


## Brief Directory Descriptions

Below is a brief description of each directory in this repo:
 - [data](https://github.com/snuzbrokh/warehouses/tree/master/data): Contains data on all active warehouse listings in the US at the time of scraping.
 - [notebook](https://github.com/snuzbrokh/warehouses/tree/master/notebook): Contains entire walkthrough of analysis in warehouses.ipynb and generated data.
 - [web_scraper](https://github.com/snuzbrokh/warehouses/tree/master/web_scraper): Contains code for scraper.


## Exploratory Data Products

Warehouse Connectivity By City:
This is an [interactive visualization](https://chart-studio.plotly.com/~snuzbrokh/34#plot) of average warehouse lease rates per location in the United States. The user can filter locations by the average price of warehouse leases as well as toggling options to see nearby ports and airports. The user can also toggle "Transport Length" which gives a measure of the average distance from that location to nearby transport hubs. 

![pic](https://github.com/snuzbrokh/warehouses/blob/master/pics/interactive_map.png)


Correlation Dashboard by State:
Lease rates across the US vary with respect to different features. Being near the coastal ports fetches high rates in California and New York but has no sway in Kansas or Oklahoma. How can we see what features correlate to higher rates? I created this [dashboard](https://chart-studio.plotly.com/~snuzbrokh/108#plot) to answer this question. 


![pic](https://github.com/snuzbrokh/warehouses/blob/master/pics/correlation_dashboard.png)
