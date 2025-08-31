# 📌 Install required libraries if missing (only run once)
# !pip install pytrends pandas matplotlib plotly prophet

import pandas as pd
pd.set_option('future.no_silent_downcasting', True)
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import plotly.express as px
from prophet import Prophet
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



# STEP 1: Connect to Google Trends using Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# STEP 2: Search for "Cloud Computing" keyword
keywords = ["Cloud Computing", "Artificial Intelligence", "Machine Learning", "Data Science", "Blockchain"]
pytrends.build_payload(keywords, cat=0, timeframe="today 12-m")  # past 12 months
time.sleep(5)  # just a pause so Google doesn't block us


# STEP 3: Interest Over Time / Check how popular it was over time
# This shows how "Cloud Computing" was searched during last 12 months
iot = pytrends.interest_over_time()
iot = iot.sort_values(by="Cloud Computing", ascending = False)
iot = iot.head(10)
print("Interest Over TIME")
print(iot)
# Visual graph for humans to see trend changes
plt.figure(figsize=(10,5))
plt.plot(iot.index, iot["Cloud Computing"], marker="o")
plt.title("Search Interest Over Time - Cloud Computing")
plt.xlabel("Date")
plt.ylabel("Search Interest (0-100)")
plt.show()


# STEP 4: Look at specific past period (Jan 2024 - Feb 2024)/Historical hour Interest
pytrends.build_payload(keywords, cat=0, timeframe='2024-01-01 2024-02-01', geo='', gprop='')
hist_data = pytrends.interest_over_time()
print("\n📊 Interest Over a Historical Period:")
print(hist_data.head(10))


# STEP 5: Which countries search the most? / Interest by Region
region_data = pytrends.interest_by_region()
region_data = region_data.sort_values(by="Cloud Computing", ascending=False).head(10)
print("\n🌍 Interest by Region (Top 10):")
print(region_data)
# Bar chart: countries vs interest
region_data.reset_index().plot(x='geoName', y='Cloud Computing', figsize=(10,5), kind="bar", color="skyblue")
plt.title("Interest by Region - Cloud Computing")
plt.show()


# STEP 6: What else do people search for (related queries)?/Related Topics and Queries
try:
    pytrends.build_payload(kw_list=['Cloud Computing'])
    related_queries = pytrends.related_queries()
    print("\n🔥 Related Queries for Cloud Computing:")
    print(related_queries["Cloud Computing"]["top"].head())
except (KeyError, IndexError):
    print("No related queries found for 'Cloud Computing'")


# STEP 7: Keyword suggestions from Google
# This tells us other search keywords Google suggests
keywords = pytrends.suggestions(keyword='Cloud Computing')
df_suggestions = pd.DataFrame(keywords).drop(columns='mid')
print("\n💡 Keyword Suggestions for Cloud Computing:")
print(df_suggestions.head())


# 8. Compare Two Specific Keywords
# Eg: Which is more popular: AI vs ML?
compare_keywords = ["Artificial Intelligence", "Machine Learning"]
pytrends.build_payload(compare_keywords, timeframe="today 12-m")
comparison = pytrends.interest_over_time()
print("\n--- AI vs ML Popularity (Last 12 Months) ---")
print(comparison.head())
comparison.plot(figsize=(10,5))
plt.title("AI vs ML Popularity")
plt.show()


# 9. Seasonal / Weekly Pattern Check
# Let's zoom in on last 3 months (weekly data)
pytrends.build_payload(["Data Science"], timeframe="today 3-m")
weekly_trend = pytrends.interest_over_time()
print("\n--- Weekly Search Interest for Data Science (Last 3 Months) ---")
print(weekly_trend.head())
weekly_trend.plot(figsize=(10,4))
plt.title("Weekly Search Interest for Data Science")
plt.show()


# 10. Long-Term Trend (5 Years)
pytrends.build_payload(["Blockchain"], timeframe="today 5-y")
long_term = pytrends.interest_over_time()
print("\n--- Blockchain Popularity (Last 5 Years) ---")
print(long_term.head())
long_term.plot(figsize=(12,6))
plt.title("Blockchain Popularity in Last 5 Years")
plt.show()



# 11. "Which country loves AI the most?"
pytrends.build_payload(["Artificial Intelligence"], timeframe="today 12-m")
ai_region = pytrends.interest_by_region(resolution="COUNTRY")
print("\nTop 5 Countries searching for AI:")
print(ai_region.sort_values("Artificial Intelligence", ascending=False).head(5))


# 12. "Are two keywords searched together?" (Correlation Check)
correlation = iot.corr()
print("\nCorrelation Between Topics:")
print(correlation)




