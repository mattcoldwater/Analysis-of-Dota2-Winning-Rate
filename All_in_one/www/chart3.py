import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

import pandas as pd
import pymysql
from config import *
import time
import numpy as np
import sys
import json
from chart3_train import MYCNN

class MyTransformer():
    def __init__(self):
        self.transform_gold = lambda x: (x - -120.77453220660516) / 5591.068864620627
        self.anti_gold = lambda x: x * 5591.068864620627 + -120.77453220660516
        self.transform_xp = lambda x: (x - -361.1073401336045) / 6297.316406573604
        self.anti_xp = lambda x: x * 6297.316406573604 + -361.1073401336045
        # data = np.apply_along_axis(self.transform_gold, 0, data)
        # target = np.apply_along_axis(self.transform_xp, 0, target)
        # data, target = data.reshape(1,-1), target.reshape(1,-1)
        # return data, target

def intersect_list(a_list, b_list):
    inter = list((set(a_list).union(set(b_list)))^(set(a_list)^set(b_list)))
    return inter

def get_matches(hero_ids):
    db = pymysql.connect(ip, user, password, db_name)
    cursor = db.cursor()
    sql_1 = "M.duration >= " + str(time_len*60) + " "
    sql_2 = " (PM.hero_id = {} OR PM.hero_id = {} OR PM.hero_id = {} OR PM.hero_id = {} OR PM.hero_id = {} )".format(hero_ids[0], hero_ids[1], hero_ids[2], hero_ids[3], hero_ids[4])
    sql = """select M.match_id as match_id
            from player_match PM, matches M
            where M.match_id = PM.match_id AND """ + sql_1 + "AND" + sql_2
    # print(sql)
    cursor.execute(sql)
    df = pd.read_sql_query(sql, db)
    ids = df["match_id"].tolist()
    return ids

def main_get_chart(hero_ids):
    assert len(hero_ids) == 10
    radiant_matches = get_matches(hero_ids[:5])
    dire_matches = get_matches(hero_ids[5:])
    matches = intersect_list(radiant_matches, dire_matches)
    
    data = pd.read_csv("chart3_dataset.csv")
    data = data[data["match_id"].isin(matches)]
    data.reset_index(drop=True, inplace=True)
    gold_list = data["radiant_gold_adv"].apply(lambda x:eval(x)[:time_len])
    gold_arr = np.array(gold_list.tolist())
    # gold = gold_arr.mean(axis=0)
    gold = gold_arr[-1]

    model = MYCNN()
    checkpoint = torch.load("./checkpoints/2.pth")
    model.load_state_dict(checkpoint['state_dict'])

    my_transformer = MyTransformer()
    gold_trans = np.apply_along_axis(my_transformer.transform_gold, 0, gold)
    gold_tensor = torch.from_numpy(gold_trans.reshape(1, 1, -1)) 
    xp_pred_trans = model(Variable(gold_tensor.float()))
    xp_pred_trans = xp_pred_trans.detach().numpy().flatten()
    xp_pred = np.apply_along_axis(my_transformer.anti_xp, 0, xp_pred_trans)

    data_dict = {
        "gold_predict": gold.tolist(),
        "xp_predict": xp_pred.tolist()
    }
    data_dict = json.dumps(data_dict)
    print(data_dict)

    # from matplotlib import pyplot as plt
    # plt.plot(gold, label="gold_predict")
    # plt.plot(xp_pred, label="xp_predict")
    # plt.legend()
    # plt.show()

def main():
    hero_string = sys.argv[1]
    test_hero_ids = hero_string.split(",")
    test_hero_ids = [eval(x) for x in test_hero_ids]
    test_hero_ids = test_hero_ids[:10]
    main_get_chart(hero_ids=test_hero_ids)

if __name__ == '__main__':
    main()