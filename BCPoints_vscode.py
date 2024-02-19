#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)


def bcpoints(df,vendor):
      Data=df
      r_s=['Active','Serving Notice Period']
      r_f=['Business','Collection','Credit','Credit Ops','DCL-Business','Retail Assets']
      r_sf=['Branch Credit Ops','Business MIS','Business-DCL','Business-IGL','Business-Retail Assets','Collection-IGL',
    'Collection-Retail Assets','Credit - Microfinance','Credit-IGL','IGL','Retail Assets - Collection','Retail Assets - Sales',
     'Surabhi - DCL']
      r_jt=['ABM-Business','ABM-Collection','Assistant Branch Manager','Assistant Branch Manager - RM','Assistant Branch Manager - RO',
      'Assistant Branch Manager (IBH)','Assistant Collection Manager','Branch Credit Manager','Branch Manager',
      'Branch Manager - Trainee','Branch Sales Manager','Business Manager','Collection and Recovery Executive',
      'Collection Manager','Collection Officer','Collection Officer-SB','Customer Relationship Officer','Operation Executive',
      'Relationship Leader','Relationship Manager','Relationship Officer','Sales Officer - Surabhi','Senior Branch Manager',
      'Senior Branch Sales Manager','Senior Collection and Recovery Executive','Senior Collection Manager','Senior Collection Officer',
      'Senior Customer Relationship Officer','Senior Executive',"Senior Officer",'Senior Operation Executive','Senior Relationship Manager',
      'Senior Relationship Officer','Senior Sales Officer - Surabhi','Temp Trainee CRO','Trainee CRO','Trainee Relationship Manager',
      'Trainee Relationship Officer','Trainee SO']
      data=Data[Data["Employeement_Status"].isin(r_s) & Data["Function"].isin(r_f) & Data["SubFunction"].isin(r_sf) & 
          Data["JobTitle"].isin(r_jt)]
      split_data=data["BranchID_Description"].str.split("-",expand= True)
      data[['BranchID', 'BranchName', 'State1','test']] = split_data
      #data.drop("BranchID_Description",axis=1,inplace=True)
      split_data=data["BranchID"].str.split(" ",expand= True)
      data[["Branch_ID",'Branch_Name', 'State_1']] = split_data
      data['BRANCH_NAME'] = data['BranchName'].fillna(data['Branch_Name'])
      # Drop the original columns if needed
      #data = data.drop(['Branch_Name', 'BranchName',"BranchID"], axis=1)
      data['Employee_Code'] = data['Employee_Code'].astype(int)
      conditions = [data['LOB'] =="IGL",data['LOB'] =="DCL",data['LOB'] =="Retail Assets"]
      values = ['sm', 'Dcl', 'il']
      data["login1"]=np.select(conditions,values)
      data["login"]=data["login1"]+data["Employee_Code"].astype(str)
      conditions1 = [data['LOB'] =="IGL",data['LOB'] =="DCL",data['LOB'] =="Retail Assets"]
      values1 = ['IGL Loan', 'Cattle Loan', 'Retail Loan']
      data["Product"]=np.select(conditions1,values1)
      RO = data[data['BranchName'].str.startswith('RO ') | data["BranchName"].str.endswith(' RO')].index
      data.drop(RO, inplace =True)
      data=data[data["BranchName"]!="HO"]
      ZO = data[data['State1'].str.startswith('ZO') | data['State1'].str.endswith('ZO') | data['State1'].str.endswith('RO') ].index
      data.drop(ZO,inplace=True)
      data["Aitel"]=data["login"].str.upper()
      conditions2 = [data['LOB'] =="IGL",data['LOB'] =="DCL",data['LOB'] =="Retail Assets"]
      values2 = ['Smfl', 'Smfldcl', 'mel']
      data["LOB_Ref"]=np.select(conditions2,values2)
      data["Pasword"]=data["LOB_Ref"]+"@"+"1234"
      conditions3 = [data['LOB'] =="IGL",data['LOB'] =="DCL",data['LOB'] =="Retail Assets"]
      values3 = ['smfl', 'smfldcl', 'smflretail']
      data["LOB_Ref1"]=np.select(conditions3,values3)
      data["branch_login_id"]=data["LOB_Ref1"]+data["Branch_ID"]
      conditions4 = [data['LOB'] =="IGL",data['LOB'] =="DCL",data['LOB'] =="Retail Assets"]
      values4 = ['Smfl', 'Smfldcl', 'Smflretail']
      data["LOB_Ref2"]=np.select(conditions4,values4)
      data["branch_login_password"]=data["LOB_Ref2"]+"@"+data["Branch_ID"]
      numeric_columns = ['Employee_Code', 'Branch_ID']
      # Convert specified columns to numeric
      data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
      # Display the resulting DataFrame
      data=pd.DataFrame(data)
      # data.to_excel("up.xlsx",index=False)
      if vendor == 'spice money':
            Spice_col=["login","Employee_Name","Branch_ID","BRANCH_NAME","State","Product"]
            Spice_Names=["Input Parameter 1 ( Agent ID)","Input Parameter 2 ( Agent Name)","Input Parameter 3 ( Branch ID)",
            "Input Parameter 4 ( Branch Name)","Input Parameter 5 ( State)","Input Parameter 6 ( Product Name)"]
            Spice_data=data[Spice_col]
            Spice_data.columns=Spice_Names
            Spice_data=pd.DataFrame(Spice_data)
            #Spice_data.to_excel("SPICE-05-01-2024.xlsx",index=False)
            return Spice_data.head(10)
      else:
            return 0
