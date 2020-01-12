#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load 
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# In[2]:


#Provides the first 5 rows of the data file 
purchase_data.head()


# In[3]:


#Provides simple mathematical analysis of data set, useful for double checking values later on
purchase_data.describe()


# ## Player Count

# * Displays the total number of unique players
# 

# In[4]:


#Counting unique users by groupy by function
user_count = purchase_data.groupby("SN")["SN"].nunique().count()

#Creating basic table to display total unique users
user_total_table = pd.DataFrame([{"Total Unique Users":user_count}])
user_total_table


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[5]:


#Counts unique items by grouping unique item names
unique_items = purchase_data.groupby("Item ID")["Item ID"].nunique().count()

#Takes average value of the price column
avg_price = purchase_data["Price"].mean()

#Adds together all values in prices coliumn to provide total revenue
tot_sales = purchase_data["Price"].sum()

#Counts the number of rows in the data set to show total number of purchases
num_purchase = purchase_data.shape[0]

#Creating dictionary to assign to new dataframe, makes reading summary table easier
pd.options.display.float_format = '${:,.2f}'.format
summary_table = pd.DataFrame([{"Number of Unique Items": unique_items,"Average Price": round(avg_price,2),"Number of Purchases": num_purchase,"Total Revenue": round(tot_sales,2)}])
summary_table


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[6]:


#Grouping by gender and defining percentage of which genders are playing
genders_df = purchase_data.groupby("Gender")["SN"].nunique()

#Calculating percentage of players by gender
genders_perc_df = (genders_df/576)*100
genders_perc_df.round(2)

#Creating table to hold all relevant information
pd.options.display.float_format = '{:,.2f}%'.format
gender_demo_table = pd.DataFrame({"Gender Count":genders_df , "Gender Percentage":round(genders_perc_df,2)})
gender_demo_table


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[7]:


#Grouping purchase count by gender 
gender_purchases = purchase_data.groupby("Gender")["Item Name"].count()

#Finding average price of purchases grouped by gender rounded to 2 decimals
gender_avg = purchase_data.groupby("Gender")["Price"].mean()
gender_avg.round(2)

#Total spent on items grouped by gender
gender_total = purchase_data.groupby("Gender")["Price"].sum()
gender_total.round(2)

#Total spent per person from each gender
per_person_total = gender_total/genders_df
per_person_total.round(2)

#Creating the display table and applying formatting to make it all prettier
pd.options.display.float_format = '${:,.2f}'.format
gender_purch_table = pd.DataFrame({"Purchase Count":gender_purchases, "Average Purchase Price":round(gender_avg,2),"Total Purchase Value":gender_total, "Avg. Total Purchase per Person":round(per_person_total,2)})
gender_purch_table


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[8]:


# Establish bins for ages
age_bins = [0, 9.99, 14.99, 19.99, 24.99, 29.99, 34.99, 39.99, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

#Use cut function to place relevant data into bins for analysis
purchase_data["Age Group"] = pd.cut(purchase_data["Age"],age_bins, labels=group_names)

# Create new data frame with the added "Age Group" and group it
age_grouped = purchase_data.groupby("Age Group")

# Count total players by age category
total_count_age = age_grouped["SN"].nunique()

# Calculate percentages by age category 
percentage_by_age = (total_count_age/user_count) * 100

# Create data frame 
pd.options.display.float_format = '{:,.2f}%'.format

age_demographics = pd.DataFrame({"Percentage of Players": percentage_by_age, "Total Count": total_count_age})
age_demographics


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[9]:


# Count purchases by age group
purchase_count_age = age_grouped["Purchase ID"].count()

# Obtain average purchase price by age group 
avg_purchase_price_age = age_grouped["Price"].mean()

# Calculate total purchase value by age group 
total_purchase_value = age_grouped["Price"].sum()

# Calculate the average purchase per person in the age group 
avg_purchase_per_person_age = total_purchase_value/total_count_age

# Create data frame with obtained values and formatting
pd.options.display.float_format = '${:,.2f}'.format

age_demographics_purchase = pd.DataFrame({"Purchase Count": purchase_count_age,
                                 "Average Purchase Price": avg_purchase_price_age,
                                 "Total Purchase Value":total_purchase_value,
                                 "Average Purchase Total per Person": avg_purchase_per_person_age})
age_demographics_purchase


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[10]:


# Spending analysis for each individual user which will then be sorted by top spender
players_purchase_count_df = purchase_data.groupby("SN").count()["Price"].rename("Purchase Count")
players_average_price_df = purchase_data.groupby("SN").mean()["Price"].rename("Average Purchase Price")
players_total_df = purchase_data.groupby("SN").sum()["Price"].rename("Total Purchase Value")

#Convert to DataFrame.
total_user_data_df = pd.DataFrame({"Purchase Count":players_purchase_count_df,
                                   "Average Purchase Price": players_average_price_df,
                                   "Total Purchase Value": players_total_df})

#Sorting by top spenders and displaying the top 5, starting with the biggest spender
top_five_spenders = total_user_data_df.sort_values("Total Purchase Value", ascending=False)
top_five_spenders.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[11]:


# Total items purchased analysis.
items_purchase_count_df = purchase_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")
items_average_price_df = purchase_data.groupby(["Item ID", "Item Name"]).mean()["Price"].rename("Average Purchase Price")
items_value_total_df = purchase_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Value")

# Convert to DataFrame
items_purchased_df = pd.DataFrame({"Purchase Count":items_purchase_count_df,
                                   "Item Price":items_average_price_df,
                                   "Total Purchase Value":items_value_total_df,})

#Sorting by most popular items, and displaying the top 5 results
most_popular_items_df = items_purchased_df.sort_values("Purchase Count", ascending=False)
most_popular_items_df.head()


# ## Most Profitable Items
# 

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[12]:


#Sorting by most profitable items, and displaying the top 5 results
most_profitable_items_df = items_purchased_df.sort_values("Total Purchase Value", ascending=False)
most_profitable_items_df.head()


# # Written Analysis

# Their are 576 unique users Playerbase is primarily in their teens to late 20's. Purchase analysis shows that players in the age range 35-39 and <10 have higher average spending per transaction. To increase profitability consider marketing to the older or younger audience to increase profits and grow the community. Potentially develop a new game mode designed for young kids to increase total <10 playerbase. The gender discrepancy is large, males account for 84% of the player base. Market to women, or create characters that will excite and attract a larger female audience.
# 
# Oathbreaker, Last Hope of the Breaking Storm is the most popular and profitable item. Pursuit, Cudgel of Necromancy, is in the top 5 most popular items list, consider increasing the price to increase profitability. Lisosia93 is our biggest spender, send them a message or gift them a unique item as a thanks for their continued loyalty to encourage other players to spend more. Consider doing this for the top 5 spenders every month to increase competition in the community, driving up profits.
