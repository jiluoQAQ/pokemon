import asyncio
import base64
import os
import random
import sqlite3
import math
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
import copy
import json
from .pokemon import *
from .PokeCounter import *

FILE_PATH = os.path.dirname(__file__)

def get_poke_bianhao(name):
    for bianhao in CHARA_NAME:
        if str(name) in CHARA_NAME[bianhao]:
            return bianhao
    return 0
#造成伤害天气
tq_kouxuelist = ['沙暴','冰雹']
#损失血量异常状态
kouxuelist = ['灼烧','中毒']
#可自动解除状态异常
jiechulist = ['冰冻','混乱','睡眠']
#无法出手异常
tingzhilist = ['冰冻','睡眠']
#概率无法出手异常
chushoulist = ['混乱','麻痹']
#有回合限制的异常状态
hh_yichanglist = ['混乱','睡眠']
#强制先手技能
xianzhi = ['守住','看穿','极巨防壁','拦堵']
#先手技能
youxian = ['电光一闪','音速拳','神速','真空波','子弹拳','冰砾','影子偷袭','水流喷射','飞水手里剑','圆瞳','电电加速']
#性格列表
list_xingge = ['实干','孤僻','勇敢','固执','调皮','大胆','坦率','悠闲','淘气','无虑','胆小','急躁','认真','天真','保守','稳重','冷静','害羞','马虎','沉着','温顺','狂妄','慎重','浮躁']
#初始精灵列表
chushi_list = [1,4,7,152,155,158,252,255,258,387,390,393,495,498,501,650,653,656,810,813,816]
#生成精灵初始技能
def add_new_pokemon_jineng(level,bianhao):
    jinenglist = get_level_jineng(level,bianhao)
    if len(jinenglist) <= 4:
        jinengzu = jinenglist
    else:
        jinengzu = random.sample(jinenglist,4)
    return jinengzu

#获取当期等级可以学习的技能
def get_level_jineng(level,bianhao):
    jinenglist = LEVEL_JINENG_LIST[bianhao]
    kexuelist = []
    #print(jinenglist)
    for item in jinenglist:
        #print(item[0])
        if int(level) >= int(item[0]):
            kexuelist.append(item[1])
    return kexuelist

#添加宝可梦，随机生成个体值
def add_pokemon(gid,uid,bianhao):
    POKE = PokeCounter()
    pokemon_info = []
    level = 5
    pokemon_info.append(level)
    for num in range(1,7):
        gt_num = int(math.floor(random.uniform(1,32)))
        pokemon_info.append(gt_num)
    for num in range(1,7):
        pokemon_info.append(0)
    xingge = random.sample(list_xingge,1)
    pokemon_info.append(xingge[0])
    jinengzu = add_new_pokemon_jineng(level,bianhao)
    jineng = ''
    shul = 0
    for jinengname in jinengzu:
        if shul>0:
            jineng = jineng + ','
        jineng = jineng + jinengname
        shul = shul + 1
    pokemon_info.append(jineng)
    POKE._add_pokemon_info(gid,uid,bianhao,pokemon_info)
    return pokemon_info

#获取宝可梦，随机个体，随机努力，测试用
def get_pokeon_info_sj(gid,uid,bianhao):
    pokemon_info = []
    level = 100
    pokemon_info.append(level)
    gt_hp = int(math.floor(random.uniform(1,32)))
    
    for num in range(1,7):
        gt_num = int(math.floor(random.uniform(1,32)))
        pokemon_info.append(gt_num)
    
    nuli = 510
    for num in range(1,6):
        MAXNULI = nuli
        if nuli > 255:
            MAXNULI = 255
        MAXNULI = MAXNULI + 1
        nulinum = int(math.floor(random.uniform(0,MAXNULI)))
        nuli = nuli - nulinum
        pokemon_info.append(nulinum)
    if nuli > 0:
        if nuli < 255:
            pokemon_info.append(nuli)
        else:
            nulinum = int(math.floor(random.uniform(1,256)))
            pokemon_info.append(nuli)
    else:
        pokemon_info.append(0)
    xingge = random.sample(list_xingge,1)
    pokemon_info.append(xingge[0])
    jinengzu = add_new_pokemon_jineng(level,bianhao)
    jineng = ''
    shul = 0
    for jinengname in jinengzu:
        if shul>0:
            jineng = jineng + ','
        jineng = jineng + jinengname
        shul = shul + 1
    pokemon_info.append(jineng)
    return pokemon_info

#获取宝可梦信息
def get_pokeon_info(gid,uid,bianhao):
    POKE = PokeCounter()
    pokemon_info = POKE._get_pokemon_info(gid,uid,bianhao)
    return pokemon_info

#计算宝可梦属性
def get_pokemon_shuxing(gid,uid,bianhao,pokemon_info):
    zhongzu_info = POKEMON_LIST[bianhao]
    xingge_info = XINGGE_LIST[pokemon_info[13]]
    #print(xingge_info)
    name = zhongzu_info[0]
    HP = math.ceil((((int(zhongzu_info[1])*2) + int(pokemon_info[1]) + (int(pokemon_info[7])/4)) * int(pokemon_info[0]))/100 + 10 + int(pokemon_info[0]))
    W_atk = math.ceil(((((int(zhongzu_info[2])*2) + int(pokemon_info[2]) + int((int(pokemon_info[8])/4))) * int(pokemon_info[0]))/100 + 5)*float(xingge_info[0]))
    W_def = math.ceil(((((int(zhongzu_info[3])*2) + int(pokemon_info[3]) + int((int(pokemon_info[9])/4))) * int(pokemon_info[0]))/100 + 5)*float(xingge_info[1]))
    M_atk = math.ceil(((((int(zhongzu_info[4])*2) + int(pokemon_info[4]) + int((int(pokemon_info[10])/4))) * int(pokemon_info[0]))/100 + 5)*float(xingge_info[2]))
    M_def = math.ceil(((((int(zhongzu_info[5])*2) + int(pokemon_info[5]) + int((int(pokemon_info[11])/4))) * int(pokemon_info[0]))/100 + 5)*float(xingge_info[3]))
    speed = math.ceil(((((int(zhongzu_info[6])*2) + int(pokemon_info[6]) + int((int(pokemon_info[12])/4))) * int(pokemon_info[0]))/100 + 5)*float(xingge_info[4]))
    return HP,W_atk,W_def,M_atk,M_def,speed
    
#重开，清除宝可梦列表个人信息
def chongkai(gid,uid):
    POKE = PokeCounter()
    POKE._delete_poke_info(gid,uid)

#放生
def fangshen(gid,uid,bianhao):
    POKE = PokeCounter()
    POKE._delete_poke_bianhao(gid,uid,bianhao)