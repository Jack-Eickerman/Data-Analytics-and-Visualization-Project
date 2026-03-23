#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 11:20:24 2025

@author: jackeickerman
"""

#Here is the tool box / Library needed for the cleansing of data
import pandas as pd

#------------------------------------------------------------------------------

#Reading the data from the CSV file and putting it into a dataframe (df) via pandas
df = pd.read_csv('simulated_supply_chain_dataset.csv')

#------------------------------------------------------------------------------

#Identifying how many and where NAN values are in the df
print(df.isnull().sum())
print()

#------------------------------------------------------------------------------

#Cleansing data in the df by filling and replacing NAN values with statistical values
df['Region'] = df['Region'].fillna("Unknown")
df['Discount'] = df['Discount'].fillna("Unknown")
df['Supplier_Lead_Time'] = df['Supplier_Lead_Time'].fillna(df['Supplier_Lead_Time'].median())
df['Customer_Rating'] = df['Customer_Rating'].fillna(df['Customer_Rating'].median())
df['Returned?'] = df['Returned'].replace(1,"Yes")
df['Returned?'] = df['Returned?'].replace(0,"No")

#------------------------------------------------------------------------------

#Verifying if NAN values have been dealt with accordingly
print()
print(df.isnull().sum())

#------------------------------------------------------------------------------

#Using Spyder IDE python platform, you can use your kernel to idenitfy outliers in your df
#Setting a Pre-descriptor to identify which columns have outliers
descriptor_pre = df.describe()

#------------------------------------------------------------------------------

#There are significant outliers and inconsistent values in two columns of df
#Setting up equations to isolate outliers outside of three standard deviations
LowerBounds = df['Units_Sold'].mean() - 3*df['Units_Sold'].std()
UpperBounds = df['Units_Sold'].mean() + 3*df['Units_Sold'].std()

LowerBounds2 = df['Logistics_Cost'].mean() - 3*df['Logistics_Cost'].std()
UpperBounds2 = df['Logistics_Cost'].mean() + 3*df['Logistics_Cost'].std()

#------------------------------------------------------------------------------

#Identify lower and upper bounds of both columns
print()
print(LowerBounds)
print(UpperBounds)
print()
print(LowerBounds2)
print(UpperBounds2)
print()

#------------------------------------------------------------------------------

#Locating outliers above and below lower and upper bounds of Units_Sold column
#Locating outliers and inconsistencies above upper bounds and below 0 of Logistics_Cost
Units_Sold = df.loc[(df['Units_Sold'] > UpperBounds) | (df['Units_Sold'] < LowerBounds)]
Logistics_Cost = df.loc[(df['Logistics_Cost'] > UpperBounds2) | (df['Logistics_Cost'] < 0)]

#------------------------------------------------------------------------------

#Using variables listed above, idenification of outliers are confirmed and can be dropped 
#via manual input given how little there are
df = df.drop(df.index[[145,3313,3797,6524,10790,12515,16172,17306,18096,19262,
                       21269,22708,22861,25165,26023,26698,29101,31841,34233,
                       35576,37252,37702,38678,38720,39363,41150,41666,41758,
                       42711,43958,44488,47184,48090,48198,49906]], axis=0)

#------------------------------------------------------------------------------

#Setting a Post-descriptor to verify changes and account for anymore inconsistencies
descriptor_post = df.describe()

#------------------------------------------------------------------------------

#Final data cleansing and touch-ups 
Unknown = df.loc[(df['Discount'] == "Unknown")]
df = df.drop(df.index[df['Discount']=="Unknown"])
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df.drop_duplicates()

#------------------------------------------------------------------------------

#Final look at df
print(df)

#------------------------------------------------------------------------------

#Send cleansed dataset to a CSV file in a selected folder and printed confirmation that the dataset is saved
df.to_csv('Cleaned_Dataset.csv', index = False)
print()
print()
print("Dataset is saved")
