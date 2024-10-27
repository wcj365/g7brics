#!/usr/bin/env python3

import json
import requests
from pyjstat import pyjstat
import pandas as pd

url_topics ="http://api.worldbank.org/v2/{}/topic?format=json"
url_indicators = "http://api.worldbank.org/v2/{}/topic/{}/indicator?format=json&page={}"
url_indicator = "http://api.worldbank.org/v2/{}/indicator/{}?format=json"
url_countries = "http://api.worldbank.org/v2/{}/country?format=json&page={}"
url_wdidata = "http://api.worldbank.org/v2/{}/country/all/indicator/{}?date={}:{}&format=jsonstat"
url_languages = "http://api.worldbank.org/v2/languages?format=json"
url_cultures = "https://raw.githubusercontent.com/wcj365/public_data/master/national_culture_dimensions.csv"
url_dimensions = "https://raw.githubusercontent.com/wcj365/public_data/master/culture_dimensions.csv"


CULTURE_TOPIC_ID = "100"

DIMENSIONS = {"PDI" : 'Power Distance Index (PDI)',
              "IDV" : 'Individualism versus Collectivism (IDV)',
              "MAS" : 'Masculinity versus Femininity (MAS)', 
              "UAI" : 'Uncertainty Avoidance Index (UAI)',
              "LTO" : 'Long-Term Orientation versus Short-Term (LTO)',
              "IVR" : 'Indulgence versus Restraint (IVR)'}


DIMENSIONS_ZH = {"PDI" : '权力差距程度 (PDI)',
                 "IDV" : '个人主义程度 (IDV)',
                 "MAS" : '男性主义程度 (MAS)', 
                 "UAI" : '风险避免程度 (UAI)',
                 "LTO" : '长远导向程度 (LTO)',
                 "IVR" : '享受放纵程度 (IVR)'}

associated_countries = {
    "BRICS":"BRA,RUS,IND,CHN,ZAF",
    "5EYES":"CAN,GBR,AUS,NZL,USA,",
    "G7":"CAN,FRA,GBR,DEU,ITA,JPN,USA",
    "G8":"CAN,FRA,GBR,DEU,ITA,JPN,USA,RUS",
    "G20":"ARG,AUS,BRA,CAN,CHN,FRA,DEU,IND,IDN,ITA,JPN,KOR,MEX,RUS,SAU,ZAF,TUR,GBR,USA"
}


def  get_languages():
    
    resp = requests.get(url=url_languages)
    json_resp = json.loads(resp.text)
    lang_list =  [lang["code"] for lang in json_resp[1]]   
    return lang_list


def get_dimension_options(language): 
    
    options = DIMENSIONS_ZH.items() if language == "zh" else DIMENSIONS.items()
    
    dim_options =  [{"label" : value, "value" : key} for key, value in options]

    sorted_options = sorted(dim_options, key=lambda d: d['label']) 
   
    return sorted_options


"""
def get_dimension_options(): 
    
    df = get_indicators("en", CULTURE_TOPIC_ID)[["name", "id"]]
    df.rename(columns={"name" : "label", "id" : "value"}, inplace=True)
    return df.to_dict(orient="records")
"""    

def get_topics(language):
    resp = requests.get(url=url_topics.format(language))
    json_resp = json.loads(resp.text)
    df = pd.DataFrame(json_resp[1])
    df.loc[len(df.index)] = [CULTURE_TOPIC_ID, "NATIONAL CULTURE", "Hofstede six-dimensional national culture model. Source: https://www.hofstede-insights.com"] 
    return df
    
def get_topic_options(language):
    
    resp = requests.get(url=url_topics.format(language))
    json_resp = json.loads(resp.text)
    topic_options =  [{'label': topic["value"], 'value': topic["id"]} for topic in json_resp[1]]   
    topic_options.append({'label': "NATIONAL CULTURE", 'value': CULTURE_TOPIC_ID})
    return topic_options


def get_indicators(language, topic_id):   
    
    if topic_id == CULTURE_TOPIC_ID:
        return pd.read_csv(url_dimensions)       
    
    print("URL",url_indicators.format(language, topic_id, 1))
    
    resp = requests.get(url=url_indicators.format(language, topic_id, 1))
    json_resp = json.loads(resp.text)
    header = json_resp[0]
    contents = json_resp[1]

    for i in range(2, int(header["pages"]) + 1):
        resp = requests.get(url=url_indicators.format(language, topic_id, i))
        contents += json.loads(resp.text)[1] 

    _df = pd.DataFrame(contents)
    _df.drop(columns=["unit"], inplace=True)
    _df = _df[_df["name"] != ""]
    _df["source"] = _df["source"].apply(lambda source: source["value"] )
    
    return _df

    
def get_indicator_options(language, topic_id):
    
    if topic_id == CULTURE_TOPIC_ID:
        return get_dimension_options(language)  
    
    resp = requests.get(url=url_indicators.format(language, topic_id, 1))
    json_resp = json.loads(resp.text)
    header = json_resp[0]
    contents = json_resp[1]

    for i in range(2, int(header["pages"]) + 1):
        resp = requests.get(url=url_indicators.format(language, topic_id, i))
        contents += json.loads(resp.text)[1]

    indicator_options =  [{'label': indicator["name"].strip(), 'value': indicator["id"]} for indicator in contents if indicator["name"] != ""]   

    sorted_options = sorted(indicator_options, key=lambda d: d['label']) 

    return sorted_options
 
def get_indicator_labels(language, indicator_list):
    
    dimension_list = [x for x in indicator_list if x in DIMENSIONS]
    indicator_list = [x for x in indicator_list if x not in DIMENSIONS]
    
    indicator_labels = {}

    for indicator in indicator_list:

        resp = requests.get(url=url_indicator.format(language, indicator))
        json_resp = json.loads(resp.text)
        header = json_resp[0]
        contents = json_resp[1]
        indicator_labels[contents[0]["id"]] = contents[0]["name"]
            
    for dim in dimension_list:
        indicator_labels[dim] = DIMENSIONS_ZH[dim] if language == "zh" else DIMENSIONS[dim]       
            
    return indicator_labels  


def get_countries_only(language):

    resp = requests.get(url=url_countries.format(language, 1))
    json_resp = json.loads(resp.text)
    header = json_resp[0]
    contents = json_resp[1]

    for i in range(2, int(header["pages"]) + 1):
        resp = requests.get(url=url_countries.format(language, i))
        contents += json.loads(resp.text)[1]

    for content in contents:
        content["region"] = content["region"]["value"]
        content["adminregion"] = content["adminregion"]["value"]
        content["incomeLevel"] = content["incomeLevel"]["value"]
        content["lendingType"] = content["lendingType"]["value"]

    df = pd.DataFrame(contents)
    df = df[df["region"] != ""]
    df = df[df["region"] != "Aggregates"]  
    df.drop(columns=["adminregion"], inplace=True) 
    df.reset_index(drop=True, inplace=True)
    df_countries = df[["id", "name", "region", "incomeLevel", "lendingType"]]
    df_countries.columns = ["Country Code", "Country Name", "Region", "Income Group", "Lending Type"]
    
    return df_countries


def get_countries(language, regions, income_levels, lending_types, associations):

    df_countries = get_countries_only(language)
    
    if len(regions) > 0:
        df_countries = df_countries[df_countries["Region"].isin(regions)]
        
    if len(income_levels) > 0:
        df_countries = df_countries[df_countries["Income Group"].isin(income_levels)]
        
    if len(lending_types) > 0:
        df_countries = df_countries[df_countries["Lending Type"].isin(lending_types)]
        
    if len(associations) > 0:
        country_set = set()
        
        for association in associations:
            country_set = country_set.union(set(associated_countries[association].split(",")))
            
        df_countries = df_countries[df_countries["Country Code"].isin(country_set)]
        
    country_options = []
    for i in range(0, df_countries.shape[0]):
        _dict={}
        _dict["label"] = df_countries.iloc[i]["Country Name"]
        _dict["value"] = df_countries.iloc[i]["Country Code"]
        country_options.append(_dict)
 
    region_options = [{'label': region, 'value': region} for region in df_countries["Region"].unique()]
    income_options = [{'label': income, 'value': income} for income in df_countries["Income Group"].unique()]
    lending_options = [{'label': lending, 'value': lending} for lending in df_countries["Lending Type"].unique()]
    
    return df_countries, region_options, income_options, lending_options, country_options

   
def get_data(language, indicator_list, countries, year_begin, year_end):
       
    df_countries, _, _, _, _ = get_countries(language, [],[],[],[])
    
    if len(countries) != 0:
        df_countries = df_countries[df_countries["Country Code"].isin(countries)]
    
    dimension_list = set([x for x in indicator_list if x in DIMENSIONS])
    indicator_list = set([x for x in indicator_list if x not in DIMENSIONS])

    df_list = []
    
    for indicator in indicator_list: 

        try:
            df =  pyjstat.Dataset.read(url_wdidata.format(language, indicator, year_begin, year_end)).write('dataframe')
        except Exception as e:
            print(e)
            continue

        df.drop(columns=["Series"], inplace=True)
        df["indicator"] = indicator       
        df = df.merge(df_countries, how="inner", left_on="Country", right_on="Country Name")
        df["Year"] = df["Year"].astype(int)
        df.drop(columns=["Country"], inplace=True) 
        df_list.append(df)
        
    if len(df_list) == 0:
        df = pd.DataFrame()
    else:
        if len(df_list) > 1:
            df = pd.concat(df_list) 
        else:
            df = df_list[0]
            

    if df.empty == True:
        df_list = []
    else:
        df_list = [df]
        year_begin = df["Year"].min()
        year_end = df["Year"].max() 
            
    for dim in dimension_list:
        df = pd.read_csv(url_cultures, usecols=["Country Code", dim])
        for year in range(year_begin, year_end + 1):
            df[str(year)] = df[dim]       
        df.drop(columns=[dim], inplace=True)
        df = pd.melt(df, id_vars=["Country Code"], 
                     var_name = "Year", 
                     value_name = "value", 
                     value_vars=[str(year) for year in range(year_begin, year_end + 1)])

        df['indicator'] = dim 
        df = df.merge(df_countries, how="inner", on="Country Code")  
        df_list.append(df)

    if len(df_list) == 0:
        df = pd.DataFrame()
    else:
        if len(df_list) > 1:
            df = pd.concat(df_list) 
        else:
            df = df_list[0]
               
    if df.empty == True:
        return pd.DataFrame()
    else:
        return df.dropna()
    
    
if __name__ == "__main__":
    
    
#    df =  pyjstat.Dataset.read(url_wdidata.format("en", "NY.GDP.PCAP.PP.CD", 2015, 2015)).write('dataframe')
#    print(df.head())
#    print(get_topic_options("en"))

#    print(get_topic_options("en"))
#   print(get_indicator_options("en",8))

#    print(get_language_options())
    
    indicator_list = ["NY.GDP.PCAP.PP.CD", "SP.DYN.LE00.IN", "PDI","SP.POP.TOTL", "IDV"]
#   indicator_list = ["PDI", "IDV"]
    lang = "en"
    

                                     
#    print(get_indicator_labels(indicator_list))
#    indicator_options = get_indicator_options(language,  8)
#    print(indicator_options)

#    df_countries, _, _, _, _ = get_countries(lang, [], [], [])
#    print(df_countries.head())
#    countries = df_countries["Country Name"].tolist()
#    print(countries)
    
    df_wdi = get_data(lang, indicator_list, [], 2010, 2020)
    print(df_wdi.shape)
    print(df_wdi.columns)