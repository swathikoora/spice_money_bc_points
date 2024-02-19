import numpy as np 
import pandas as pd 

def sum_designation(df,des):
    return df[df['Designation']== des]['Salary'].sum()