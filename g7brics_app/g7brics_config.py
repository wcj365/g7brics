#/usr/local/env python

LANGUAGES = {
    "English" : "en",
    "中文"    : "zh"
}


G7 = [
    "USA",
    "CAN",
    "GBR",
    "DEU",
    "FRA",
    "ITA",
    "JPN"
]


BRICS= [
    "BRA",
    "RUS",
    "IND",
    "CHN",
    "ZAF",
    "EGY",
    "ETH",
    "IRN",
    "SAU"
]


COLOR_MAP = {
    "REST OF WORLD" : "lightgreen",
    "BRICS" : "orangered",  
    "G7" : "MediumSlateBlue" 
}


INDICATORS = [
    "SP.POP.TOTL",
    "NY.GDP.MKTP.PP.CD",
    "NY.GDP.PCAP.PP.CD",
    "SP.DYN.LE00.IN",
    "SH.STA.SUIC.P5"
]

COLUMNS = [
    "Population (Millions)",
    "GDP PPP ($Billions)",
    "GDP Per Capita PPP ($)",
    "Life Expectancy at Birth (Years)",
    "Suicide Mortality Rate (Per 100K People)"
]

TOPICS = ["Geography", "Population", "Economy", "Wealth", "Health", "Data"]

TAB_OPTIONS = [
    ":sunny: Historic Trend", 
    ":sunny: By Year/Group",
    ":sunny: By Year/Country"
]