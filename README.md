# FoodVendor

One iconic feature of New York are its food vendors lining the streets in busy areas. However, there is an issue where food vendors are distributed inefficiently. Many vendors may flock to one popular area, completing neglecting another popular area. For example, today, 8 similar food carts were spotted in Herald Square while significantly fewer seen near Bryant Park, while another day it is more even.


<p align="center">
<img src="https://github.com/bsun1220/cubist_info/blob/main/images/example.png" alt="drawing" width="600"/>
</p>

We propose an app **FoodVendor** to promote business cooperation and efficiency. A vendor can check **FoodVendor** to check where they go for the day. When they have decided on a location, they can indicate this so other vendors are better prepared. This creates a network effect where more vendors will join the app so there is greater accuracy for everyone.

<p align="center">
<img src="https://github.com/bsun1220/cubist_info/blob/main/images/logo.png" alt="drawing" width="300"/>
</p>

# Historical Motivation
Below, we measure the most populat Citi Bike locations and use this as a corollary for population density. We chose Citi Bike over subway because of ease of use for historical data, where we use bike availability for to measure population inflow and outflow into certain regions. 
<p align="center">
<img src="https://github.com/bsun1220/cubist_info/blob/main/images/day_of_week.png" alt="drawing" width="450"/>
  <img src="https://github.com/bsun1220/cubist_info/blob/main/images/start_hours.png" alt="drawing" width="450"/>
</p>

We started analysis with historical data to get a better sense of popular areas in New York. We first conduct exploratory data analysis, finding peaks from 8AM-10AM and 4-6PM on the weekdays and 4-7PM on the weekends. We use CitiBike ride destinations as a proxy for popularity – there is no MTA data that indicates location popularity. We identify a list of the top 50 destination stations from 4-7PM as locations vendors should consider, targeting employees finishing their work day.

<p align="center">
  <img src="https://github.com/bsun1220/cubist_info/blob/main/images/map2.png" alt="drawing" width="450"/>
</p>
This is during 4 pm to 7 pm on Weekdays. We have 2 main findings. First, we see major outflow from business-dominant areas towards a) residential areas and b) restaurant heavy areas). Second, we see a lot of convergent outflow. This thesis provides a strong basis for our assumption of using transit flows to predict population density. 
<p align="center">
<img src="https://github.com/bsun1220/cubist_info/blob/main/images/map1.png" alt="drawing" width="450"/>
</p>

# Game Theoretic Implications
For food availability, we can treat this as a game theory problem. Each food vendor is attempting to choose a location which maximizes population density while accounting for food vendor density. Population limit incentives prevent all of the food vendors from choosing the most populated area. **Food Vendor** is designed to promote truthseeking between food vendors to discentive inefficiencies in vendor allocation. By reducing information assymetry, vendors are more willing to allocate towards least populated areas, improving access to the NYC population. To calculate our price index, we look at a combination of 1) historical transition probabilities between 2 important cites and 2) current recent outflow. 
<p align="center">
<img src="https://github.com/bsun1220/cubist_info/blob/main/images/top.png" alt="drawing" width="300"/>
</p>

# Setting up the webapp

```
git clone https://github.com/jamesg6197/P72-Hackathon.git
cd P72-Hackathon
pip install -r requirements.txt # install dependencies
python manage.py makemigrations #generate data models
python manage.py migrate
python manage.py csp_background #run csp realtime streaming in the background to populate database asynchronously
python manage.py runserver #start webapp server

```
