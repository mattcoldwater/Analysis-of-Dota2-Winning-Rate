password = "CUHKSZ"
# ["heroes", "item", "suitable_item", "player", "leagues","matches", "player_match",] "123456" #
table_names = ["heroes", "item", "suitable_item", "player", "leagues","matches", "player_match", "public_match", "ban_pick"]
#table_names = ["heroes", "player", "leagues","matches", "player_match"]
ip = "localhost"
user = "root"
db_name = "win" #"win"
if_exists = "replace"

batch_size = 16
num_epoch = 1000
time_len = 34

test_hero_ids = [59, 98, 99, 100, 101, 23, 2, 12, 45, 43]

"""
pip install requests
pip install pymysql
pip install pandas
pip install mysql-connector-python
pip install sqlalchemy
pip install retrying
conda install pytorch-cpu torchvision-cpu -c pytorch
"""