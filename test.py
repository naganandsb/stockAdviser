import pandas as pd
import numpy as np


dataf = pd.read_csv(r"C:\Users\Dell\Downloads\data.csv")
df_filtered = dataf.dropna(subset=['Date'])
# print(sum(df_filtered[df_filtered.Description =="Dmart"]["Expense (Debit)"].astype("float")))
df_filtered["Expense (Debit)"] = df_filtered["Expense (Debit)"].astype("float")
df_gruop = df_filtered.groupby(["Description"])

print(df_gruop["Expense (Debit)"].agg([np.sum,np.mean]).rename(columns={"sum": "Nag Sum","mean":"Nag Mean"}))


# Ser1 = pd.Series([1,2,3,4,5,6])
# print(Ser1.describe())