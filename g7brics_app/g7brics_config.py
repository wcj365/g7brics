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

FOUNDERS = [
    "BRA",
    "RUS",
    "IND",
    "CHN",
    "ZAF"
]

ADDITIONS = [
    "EGY",
    "ETH",
    "IRN",
    "SAU"
]

PARTNERS = [
    "DZA",
    "BLR",
    "BOL",
    "CUB",
    "IDN",
    "KAZ",
    "MYS",
    "NGA",
    "THA",
    "TUR",
    "UGA",
    "UZB",
    "VNM"
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
    "SH.STA.SUIC.P5",
    "MS.MIL.XPND.CD",
    "MS.MIL.XPND.GD.ZS",
    "NY.GDP.MKTP.CD",
    "NY.GDP.PCAP.CD"
]

COLUMNS = [
    "Population ($Millions)",
    "GDP PPP ($Billions)",
    "GDP Per Capita PPP ($)",
    "Life Expectancy at Birth (Years)",
    "Suicide Mortality Rate (Per 100K People)",
    "Military Expenditure ($Millions)",
    "Military Expenditure (% of GDP)",
    "GDP ($Billions)",
    "GDP Per Capita ($)"
]

TOPICS = [
    "Geography", 
    "Population", 
    "Economy", 
    "Defense",
    "Wealth", 
    "Health", 
    "Data"
]

GDP_MEASURE = [
    "Norminal Dollar", 
    "Purching Power Parity (PPP)"
]

TAB_OPTIONS = [
    ":sunny: Historic Trend", 
    ":sunny: By Year/Group",
    ":sunny: By Year/Country"
]