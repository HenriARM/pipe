import pandas as pd

file_path = "data/test_task_data.csv"
data = pd.read_csv(file_path)

# Drop redundant or duplicate columns
if data["State"].equals(data["State.1"]):
    data = data.drop(columns=["State.1"])

if data["Country"].unique() == ["United States"]:
    data = data.drop(columns=["Country"])

if data["Transaction_id"].nunique() == data.shape[0]:
    data = data.drop(columns=["Transaction_id"])

data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")

if data["Year_Month"].equals(data["Date"].dt.strftime("%y-%b")):
    data = data.drop(columns=["Year_Month"])

# "3,499" -> 3499
data["Amount US$"] = data["Amount US$"].str.replace(",", "").astype(float)

# Identify rows where 'Individual_Price_US$' has '#VALUE!' and replace using logic
invalid_rows = data["Individual_Price_US$"].str.contains(r"[^\d.,]", na=False)
data.loc[invalid_rows, "Individual_Price_US$"] = (
    data.loc[invalid_rows, "Amount US$"] / data.loc[invalid_rows, "Quantity"]
)
data["Individual_Price_US$"] = (
    data["Individual_Price_US$"].str.replace(",", "").astype(float)
)

# Sort by customer_id and Date for recency calculations
data = data.sort_values(by=["Date"])

duplicate_customers = data.groupby("customer_id").filter(lambda x: len(x) > 1)
duplicate_customers = duplicate_customers.sort_values(by=["Date"])

# TODO: make some visualisations
# - avg spendings per category
# - most spending states
# ...

# TODO: tuples State-City and Product-Category will be highly correlated
