import pandas as pd
import pymysql
from config import *
import time
import sys
import json

def main_get_chart(hero_ids):
    assert len(hero_ids) == 10
    db = pymysql.connect(ip, user, password, db_name)
    cursor = db.cursor()
    # print("db connection ok")
    cursor.execute("DROP VIEW IF EXISTS chart2_data")
    sql1 = """CREATE VIEW chart2_data AS
                select M.match_id as match_id,
                ((PM.slot <128) = M.radiant_win) as win, 
                PM.hero_id as hero_id,
                PM.kills as kills,
                PM.deaths as deaths,
                PM.hero_damage as hero_damage,
                PM.tower_damage as tower_damage,
                PM.gold_per_min as gold_per_min,
                PM.xp_per_min as xp_per_min,
                M.radiant_score as radiant_score,
                M.dire_score as dire_score,
                M.duration as duration
            from player_match PM, matches M
            where M.match_id = PM.match_id AND 
                  M.radiant_score <> 0 AND M.dire_score <> 0"""
    # print(sql1)
    cursor.execute(sql1)

    data_dict = {}
    for attr in ['avg_xp_per_min', 'avg_dire_score', 'avg_duration', 'avg_hero_damage', 'avg_deaths', 'avg_tower_damage', 'avg_win', 'avg_gold_per_min', 'avg_kills', 'avg_radiant_score']:
        data_dict[attr] = []
    for k in range(len(hero_ids)):
        hero_id = hero_ids[k]
        sql_2 = """ select AVG(win) avg_win, 
                        AVG(kills) avg_kills, 
                        AVG(deaths) avg_deaths, 
                        AVG(hero_damage) avg_hero_damage, 
                        AVG(tower_damage) avg_tower_damage,
                        AVG(gold_per_min) avg_gold_per_min,
                        AVG(xp_per_min) avg_xp_per_min,
                        AVG(radiant_score) avg_radiant_score,
                        AVG(dire_score) avg_dire_score,
                        AVG(duration) avg_duration
                    from chart2_data
                    where hero_id = """+str(hero_id)
        cursor.execute(sql_2)
        df = pd.read_sql_query(sql_2, db)
        hero_dict = df.to_dict(orient='dict')
        for attr in ['avg_xp_per_min', 'avg_dire_score', 'avg_duration', 'avg_hero_damage', 'avg_deaths', 'avg_tower_damage', 'avg_win', 'avg_gold_per_min', 'avg_kills', 'avg_radiant_score']:
            data_dict[attr].append(hero_dict[attr][0])
    cursor.execute("drop view chart2_data")
    db.close() 

    data_dict = json.dumps(data_dict)
    print(data_dict)

def main():
    hero_string = sys.argv[1]
    test_hero_ids = hero_string.split(",")
    test_hero_ids = [eval(x) for x in test_hero_ids]
    test_hero_ids = test_hero_ids[:10]
    main_get_chart(hero_ids=test_hero_ids)

if __name__ == '__main__':
    main()