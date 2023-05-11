import asyncio
import random
import os
import sqlite3
import math
import json
DB_PATH = os.path.expanduser("~/.hoshino/pokemon.db")
# 记录贵族相关数据

class PokeCounter:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_table()
    
    def _connect(self):
        return sqlite3.connect(DB_PATH)
    
    def _create_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_TABLE
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           BIANHAO         INT    NOT NULL,
                           LEVEL           INT    NOT NULL,
                           EXP             INT    NOT NULL,
                           GT_HP           INT   NOT NULL,
                           GT_ATK          INT   NOT NULL,
                           GT_DEF          INT   NOT NULL,
                           GT_STK          INT   NOT NULL,
                           GT_SEF          INT   NOT NULL,
                           GT_SPD          INT   NOT NULL,
                           NL_HP           INT   NOT NULL,
                           NL_ATK          INT   NOT NULL,
                           NL_DEF          INT   NOT NULL,
                           NL_STK          INT   NOT NULL,
                           NL_SEF          INT   NOT NULL,
                           NL_SPD          INT   NOT NULL,
                           XINGGE          TEXT   NOT NULL,
                           JINENG          TEXT   NOT NULL,
                           PRIMARY KEY(GID,UID,BIANHAO));''')
        except:
            raise Exception('创建表发生错误')
    
    def _add_pokemon_info(self, gid, uid, bianhao, pokemon_info):
        level, gt_hp, gt_atk, gt_def, gt_stk, gt_sdf, gt_spd, nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd, xingge, jineng = pokemon_info
        #print(pokemon_info)
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_TABLE (GID,UID,BIANHAO,LEVEL,EXP,GT_HP,GT_ATK,GT_DEF,GT_STK,GT_SEF,GT_SPD,NL_HP,NL_ATK,NL_DEF,NL_STK,NL_SEF,NL_SPD,XINGGE,JINENG) \
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (gid, uid, bianhao, level, 0, gt_hp, gt_atk, gt_def, gt_stk, gt_sdf, gt_spd, nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd, xingge, jineng)
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _add_pokemon_level(self, gid, uid, bianhao, level):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_TABLE (GID,UID,BIANHAO,LEVEL) \
                                VALUES (?,?,?,?)", (gid, uid, bianhao, level)
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _add_pokemon_nuli(self, gid, uid, bianhao, nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_TABLE (GID,UID,BIANHAO,NL_HP,NL_ATK,NL_DEF,NL_STK,NL_SEF,NL_SPD) \
                                VALUES (?,?,?,?,?,?,?,?,?)", (gid, uid, bianhao, nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd)
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _add_pokemon_jineng(self, gid, uid, bianhao, jineng):
        try:
            with self._connect() as conn:
                conn.execute(
                    "UPDATE POKEMON_TABLE SET JINENG = ? WHERE GID=? AND UID=? AND BIANHAO=?",
                    (jineng, gid, uid, bianhao),
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _get_pokemon_info(self, gid, uid, bianhao):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT LEVEL,GT_HP,GT_ATK,GT_DEF,GT_STK,GT_SEF,GT_SPD,NL_HP,NL_ATK,NL_DEF,NL_STK,NL_SEF,NL_SPD,XINGGE,JINENG FROM POKEMON_TABLE WHERE GID={gid} AND UID={uid} AND BIANHAO={bianhao}").fetchall()
                if r:
                    return r[0]
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
            
    def _get_pokemon_list(self, gid, uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT BIANHAO,LEVEL FROM POKEMON_TABLE WHERE GID={gid} AND UID={uid} ORDER BY LEVEL desc LIMIT 20").fetchall()
                if r:
                    return r
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
            
    def _delete_poke_info(self, gid, uid):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM POKEMON_TABLE  WHERE GID=? AND UID=?",
                (gid, uid),
            )
            
    def _delete_poke_bianhao(self, gid, uid, bianhao):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM POKEMON_TABLE  WHERE GID=? AND UID=? AND BIANHAO=?",
                (gid, uid, bianhao),
            )