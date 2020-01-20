
##### Trade in goods 2011-2016 ###

# wget -O tradeInGoods_import.xlsx  "https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodscountrybycommodityimports/2011to2016/countrybycommodityimports.xlsx"
# wget -O tradeInGoods_export.xlsx "https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodscountrybycommodityexports/2011to2016/countrybycommodityexports.xlsx"

from pathlib import Path
import pandas as pd

## UK imports and exports
UK_imports_df = pd.read_excel(Path().joinpath('2-gravity_models_trade/data/', 'tradeInGoods_import.xlsx'), sep="\t")
UK_export_df = pd.read_excel(Path().joinpath('2-gravity_models_trade/data/', 'tradeInGoods_export.xlsx'), sep="\t")


## Country pairwise distances
# Taken from http://egallic.fr/en/closest-distance-between-countries/
country_pairwise_distances_df = pd.read_csv("https://gist.githubusercontent.com/mtriff/185e15be85b44547ed110e412a1771bf/raw/1bb4d287f79ca07f63d4c56110099c26e7c6ee7d/countries_distances.csv", sep=",")


## Economy sizes (GDP)
GDP_by_country_df = pd.read_csv("http://databank.worldbank.org/data/download/GDP.csv", skiprows=4)


## Commonwealth countries
commonwealth_nations_df = pd.read_html("https://en.wikipedia.org/wiki/Member_states_of_the_Commonwealth_of_Nations")


## EU countries
EU_nations_df = pd.read_html("https://en.wikipedia.org/wiki/Member_state_of_the_European_Union")



UK_export_df[ UK_export_df["Commodity description"] == "Total"][ ['Country code', "Country description", 2015] ]

### Trade in services 2017 ###
