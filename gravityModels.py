
##### Trade in goods 2011-2016 ###

# wget -O tradeInGoods_import.xlsx  "https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodscountrybycommodityimports/2011to2016/countrybycommodityimports.xlsx"
# wget -O tradeInGoods_export.xlsx "https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodscountrybycommodityexports/2011to2016/countrybycommodityexports.xlsx"

from pathlib import Path
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

#%%
## UK imports and exports
UK_imports_df = pd.read_excel(Path().joinpath('2-gravity_models_trade/data/', 'tradeInGoods_import.xlsx'), sep="\t")
UK_export_df = pd.read_excel(Path().joinpath('2-gravity_models_trade/data/', 'tradeInGoods_export.xlsx'), sep="\t")

UK_export_df = UK_export_df.rename(columns={i : str(i)+"exports" for i in list(range(2011, 2017))}).rename(columns = {"Country description":"Country"})
UK_imports_df = UK_imports_df.rename(columns={i : str(i)+"imports" for i in list(range(2011, 2017))}).rename(columns = {"Country description":"Country"})

UK_export_df = UK_export_df[~UK_export_df.Country.isin(["Whole world","Extra EU 28 (Rest of World)","Total EU(28)"])]
UK_imports_df = UK_imports_df[~UK_imports_df.Country.isin(["Whole world","Extra EU 28 (Rest of World)","Total EU(28)"])]

UK_totalexports_2015 = UK_export_df[ UK_export_df["Commodity description"] == "Total"][["Country", "2015exports"]].copy()
UK_totalimports_2015 = UK_imports_df[ UK_imports_df["Commodity description"] == "Total"][["Country", "2015imports"]].copy()

#%%
## Country pairwise distances
# Taken from http://egallic.fr/en/closest-distance-between-countries/
country_pairwise_distances_df = pd.read_csv("https://gist.githubusercontent.com/mtriff/185e15be85b44547ed110e412a1771bf/raw/1bb4d287f79ca07f63d4c56110099c26e7c6ee7d/countries_distances.csv", sep=",")
UK_to_country_distance_df = country_pairwise_distances_df[country_pairwise_distances_df.pays1 == "UK"].copy()


#%%
## Economy sizes (GDP)
GDP_by_countrywiki_df = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")
GDP_perUN_df = GDP_by_countrywiki_df[5]

GDP_perUN_df.columns = ["rank","country","GDP"]
GDP_perUN_df.country = GDP_perUN_df.country.str.replace("\s*\[n?\s*\d+\]\s*$", "")

GDP_perUN_df.GDP = GDP_perUN_df.GDP.astype(float)
GDP_perUN_df = GDP_perUN_df[~GDP_perUN_df.GDP.isna()].copy()


#%%
## Commonwealth countries
commonwealth_nations_df = pd.read_html("https://en.wikipedia.org/wiki/Member_states_of_the_Commonwealth_of_Nations")[0]

commonwealth_nations_df.Country = commonwealth_nations_df.Country.str.replace("\[\w\]","")
## EU countries
EU_nations_df = pd.read_html("https://en.wikipedia.org/wiki/Member_state_of_the_European_Union")[1]


#### Inspect the data for country codes that don't correspond. Use the ONS imports/exports names as the standard to map *to* ###


#%%
# Append distances to table
UK_totalexports_2015[~UK_totalexports_2015.Country.isin(UK_to_country_distance_df.pays2.unique())].sort_values(by = "2015exports", ascending = False)

# RoI, FYR Macedonia and US are not mapped correctly
UK_to_country_distance_df[UK_to_country_distance_df.pays2.str.contains("Ireland", case=False)]
UK_to_country_distance_df.loc[UK_to_country_distance_df.pays2 == "Ireland", "pays2"] = "Republic of Ireland"

UK_to_country_distance_df[ UK_to_country_distance_df.pays2.str.contains("USA", case=False)]
UK_to_country_distance_df.loc[UK_to_country_distance_df.pays2 == "USA", "pays2"] = "United States inc Puerto Rico"

UK_to_country_distance_df[ UK_to_country_distance_df.pays2.str.contains("Macedonia", case=False)]
UK_to_country_distance_df.loc[UK_to_country_distance_df.pays2 == "Macedonia", "pays2"] = "FYR Macedonia"


#%%
# Country GDPs
UK_totalexports_2015[~UK_totalexports_2015.Country.isin(GDP_perUN_df.country)].sort_values(by="2015exports", ascending=False)

GDP_perUN_df[ GDP_perUN_df.country.str.contains("United States", case=False)]
GDP_perUN_df.loc[GDP_perUN_df.country == "United States", "country"] = "United States inc Puerto Rico"

GDP_perUN_df[ GDP_perUN_df.country.str.contains("Ireland", case=False)]
GDP_perUN_df.loc[GDP_perUN_df.country == "Ireland", "country"] = "Republic of Ireland"

GDP_perUN_df[ GDP_perUN_df.country.str.contains("Macedonia", case=False)]
GDP_perUN_df.loc[GDP_perUN_df.country == "North Macedonia", "country"] = "FYR Macedonia"

GDP_perUN_df[ GDP_perUN_df.country.str.contains("Korea", case=False)]
GDP_perUN_df.loc[GDP_perUN_df.country == "Korea, South", "country"] = "South Korea"

#%%
# Members of trading blocks
EU_nations_df[~EU_nations_df["Country name"].isin(UK_totalexports_2015.Country)]
EU_nations_df.loc[EU_nations_df["Country name"] == "Ireland","Country name"] = "Republic of Ireland"
EU_nations_df.loc[EU_nations_df["Country name"] == "Czechia","Country name"] = "Czech Republic"

commonwealth_nations_df[~commonwealth_nations_df.Country.isin(UK_totalexports_2015.Country)]

#%%
# Create table
UK_gravity_model_data2015 = \
    UK_totalexports_2015.set_index("Country").\
        join(UK_totalimports_2015.set_index("Country")).\
        join(UK_to_country_distance_df[["pays2","dist"]].set_index("pays2")).\
        join(GDP_perUN_df[["country","GDP"]].set_index("country"))

UK_gravity_model_data2015["inEU"] = UK_gravity_model_data2015.index.isin(EU_nations_df["Country name"])
UK_gravity_model_data2015["inCommonwealth"] = UK_gravity_model_data2015.index.isin(commonwealth_nations_df["Country"])

UK_gravity_model_data2015 = UK_gravity_model_data2015[~UK_gravity_model_data2015.GDP.isna()]

UK_gravity_model_data2015["log(GDP/distance)"] = np.log10(UK_gravity_model_data2015.GDP/UK_gravity_model_data2015.dist)


UK_gravity_model_data2015["log(GDP/distance)"] = np.log10(1+UK_gravity_model_data2015.GDP/UK_gravity_model_data2015.dist)

UK_GDP = GDP_perUN_df[GDP_perUN_df.country == "United Kingdom"].GDP

UK_gravity_model_data2015["log( (GDP_i * GDP_j)/distance)"] = np.log10(float(UK_GDP)*UK_gravity_model_data2015.GDP/UK_gravity_model_data2015.dist)

UK_gravity_model_data2015["log(exports)"] = np.log10(1+UK_gravity_model_data2015["2015exports"])

# 186 countries worth of data

#&&
# Make some plots

UK_gravity_model_data2015.sort_values("log( (GDP_i * GDP_j)/distance)", ascending = False)


sns.lmplot(x="log( (GDP_i * GDP_j)/distance)", y="log(exports)", hue="inEU", data=UK_gravity_model_data2015,
           markers=["o", "x"], palette="Set1")

sns.lmplot(x="log( (GDP_i * GDP_j)/distance)", y="log(exports)", hue="inCommonwealth", data=UK_gravity_model_data2015,
           markers=["o", "x"], palette="Set1")

plt.show()

statsmodels


from sklearn.linear_model import LinearRegression


model = LinearRegression().fit()

