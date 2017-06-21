# coding=utf-8
# sqlite database to redis

import uuid
import sqlite3
from config import SQLITE3_DB_PATH, SQLITE3_DB_SIZE
from base_cache import rds


def sqlite2redis():
    con = sqlite3.connect(SQLITE3_DB_PATH + "ft.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM ft;')
    datas = cur.fetchall()
    for row in datas:
        ft_id = str(row[0])
        ft_value = str(row[1])
        ft_url = str(row[2])
        ft_token = str(uuid.uuid4())
        
        rds.set(ft_id, (ft_token, ft_value, ft_url), 2*60*60)


def get_token_value(token):
    for i in range(1, SQLITE3_DB_SIZE + 1):
        ft_data = rds.get(str(i))
        if ft_data is not None:
            if ft_data[0] == token:
                return ft_data[1]
    return None