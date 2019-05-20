import pandas as pd
import pymysql
from config import *
import time
import requests
from retrying import retry
from urllib import parse
import mysql.connector #mysql-connector-python
from sqlalchemy import create_engine

@retry(wait_fixed=5000)
def get_raw_data(file_name):
    with open(file_name, "r") as f:
        raw_sql = f.readlines()
        raw_sql = "".join(raw_sql)

    quote_sql = parse.quote(raw_sql)
    # print(quote_sql)
    url = "https://api.opendota.com/api/explorer?sql="+quote_sql
    info = requests.get(url)
    info = info.json()

    raw_data = pd.DataFrame(info["rows"])
    raw_data.dropna(how="any", inplace=True)
    raw_data = raw_data[(raw_data["radiant_gold_adv"].apply(lambda x:len(x))>2)]
    raw_data = raw_data[(raw_data["radiant_xp_adv"].apply(lambda x:len(x))>2)]
    raw_data.reset_index(drop=True, inplace=True)
    raw_data.to_csv("chart3_raw_data.csv", index=False)
    print(len(raw_data))
    return raw_data

def get_data():
    try:
        raw_data = pd.read_csv("chart3_raw_data.csv")
    except:
        raw_data = get_raw_data("./txt_files/points.txt")
    
    data = raw_data.copy()
    data["gold"] = data["radiant_gold_adv"].apply(lambda x:len(eval(x)))
    data["xp"] = data["radiant_xp_adv"].apply(lambda x:len(eval(x)))
    data = data[data["gold"]>=time_len]
    data = data[data["xp"]>=time_len]
    data.reset_index(drop=True, inplace=True)
    data[["match_id", "radiant_gold_adv", "radiant_xp_adv"]].to_csv("chart3_dataset.csv", index=False)
    print(len(data))

def main():
    get_data()

if __name__ == '__main__':
    main()