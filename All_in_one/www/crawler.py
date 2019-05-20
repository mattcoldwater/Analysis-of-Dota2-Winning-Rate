import requests
from urllib import parse
import pandas as pd
from datetime import datetime
import pymysql
import mysql.connector #mysql-connector-python
from sqlalchemy import create_engine
from retrying import retry
import time
import datetime
from config import *

@retry(wait_fixed=5000)
def crawl(file_name, limit="200", day="2000-12-25"):
    with open(file_name, "r") as f:
        raw_sql = f.readlines()
        raw_sql = [s if s!="LIMIT 200" else "LIMIT "+limit for s in raw_sql]
        day0 = "AND matches.start_time >= extract(epoch from timestamp '2000-12-25T00:00:00.000Z')\n"
        day_now = day0.replace("2000-12-25", day)
        raw_sql = [s if s!=day0 else day_now for s in raw_sql]
        raw_sql = "".join(raw_sql)

    quote_sql = parse.quote(raw_sql)
    # print(quote_sql)
    url = "https://api.opendota.com/api/explorer?sql="+quote_sql
    info = requests.get(url)
    print(info)
    info = info.json()

    df = pd.DataFrame(info["rows"])
    if file_name in ["matches", "player_match"]:
        df["match_id"] = df["match_id"].astype("str")
    print(len(df))
    return df

class Win_database():
    def __init__(self):
        pass
    
    @staticmethod
    def create_table(name):
        if name == "heroes":
            sql = r"""CREATE TABLE heroes
                (hero_id INT NOT NULL,
                name VARCHAR(50) NOT NULL,
                localized_name VARCHAR(30) NOT NULL,
                attack_type BOOLEAN NOT NULL,
                primary_attr VARCHAR(30) NOT NULL,
                legs INT NOT NULL,
                PRIMARY KEY (hero_id) )"""
        elif name == "item":
            sql = r"""CREATE TABLE item
                (item_id INT NOT NULL,
                name VARCHAR(60) NOT NULL,
                cost INT NOT NULL,
                side_shop INT NOT NULL,
                secret_shop INT NOT NULL,
                recipe INT NOT NULL,
                PRIMARY KEY (item_id) )"""            
        elif name == "suitable_item":
            sql = r"""CREATE TABLE suitable_item
                (hero_id INT NOT NULL,
                item_id INT NOT NULL,
                PRIMARY KEY (hero_id, item_id),
                FOREIGN KEY (hero_id) REFERENCES heroes(hero_id),
                FOREIGN KEY (item_id) REFERENCES item(item_id) )"""            
        elif name == "player":
            sql = r"""CREATE TABLE player
                (account_id INT NOT NULL,
                cheese INT NOT NULL,
                PRIMARY KEY (account_id) )"""          
        elif name == "leagues":
            sql = r"""CREATE TABLE leagues
                (leagueid INT NOT NULL,
                tier VARCHAR(20),
                PRIMARY KEY (leagueid) )"""            
        elif name == "matches":
            sql = r"""CREATE TABLE matches
                (match_id  VARCHAR(10) NOT NULL,
                start_time  CHAR(11) NOT NULL,
                radiant_win BOOLEAN NOT NULL,
                duration INT NOT NULL,
                radiant_score INT NOT NULL,
                dire_score INT NOT NULL,
                leagueid INT,
                PRIMARY KEY (match_id),
                FOREIGN KEY (leagueid) REFERENCES leagues(leagueid) )"""                   
        elif name == "player_match":
            sql = r"""CREATE TABLE player_match
                (match_id  VARCHAR(10) NOT NULL,
                slot INT NOT NULL,
                account_id INT NOT NULL,
                hero_id INT NOT NULL,
                kills INT NOT NULL,
                deaths INT NOT NULL,
                hero_damage INT,
                tower_damage INT,
                hero_healing INT,
                gold_per_min INT NOT NULL,
                xp_per_min INT NOT NULL,
                level INT NOT NULL,
                PRIMARY KEY (match_id, slot),
                FOREIGN KEY (hero_id) REFERENCES heroes(hero_id),
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (account_id) REFERENCES player(account_id) )"""
        elif name == "public_match":
            sql = r"""CREATE TABLE public_match
                (pmatch_id VARCHAR(10) NOT NULL,
                match_seq_num VARCHAR(10) NOT NULL,
                game_mode VARCHAR(10) NOT NULL,
                lobby_mode VARCHAR(4) NOT NULL,
                num_mmr INT,
                avg_mmr INT,
                start_time VARCHAR(10) NOT NULL,
                pradiant_win BOOL NOT NULL,
                match_id VARCHAR(10),
                PRIMARY KEY (pmatch_id),
                FOREIGN KEY (match_id) REFERENCES matches(match_id) )"""            
        elif name == "ban_pick":
            sql = r"""CREATE TABLE ban_pick
                (match_id  VARCHAR(10) NOT NULL,
                ord INT NOT NULL,
                hero_id INT NOT NULL,
                team INT NOT NULL,
                ban_or_pick BOOL NOT NULL,
                PRIMARY KEY (match_id, ord),
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (hero_id) REFERENCES heroes(hero_id) )"""   
        return sql
       
def main_crawl(): 
    limit = "200000000"
    win = Win_database()

    # mysql
    db = pymysql.connect(ip, user, password, db_name)
    cursor = db.cursor()
    print("db connection ok")

    # create table
    if if_exists == "replace":
        # drop
        for i in range(len(table_names)):
            table_name = table_names[-i-1]
            sql = "DROP TABLE IF EXISTS "+table_name
            print(sql)
            cursor.execute(sql)

        for table_name in table_names:
            sql = win.create_table(table_name)
            print(sql)
            cursor.execute(sql)

    db.close()    

    #engine
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:3306/{}".format(user, password, ip, db_name), encoding='utf-8')
    con = engine.connect()# 建立连接
    print("engine connection ok")
    # insert
    for table_name in table_names:
        print(table_name, "----", end="")
        df = crawl("./txt_files/"+table_name+".txt", limit, "1998-12-10")  
        print("writing----", end="")
        df.to_sql(name=table_name, con=con, if_exists="append", index=False, chunksize=100)
        print("ok")

def main():
    main_crawl()

if __name__ == '__main__':
    main()