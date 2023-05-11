import asyncio
import base64
import os
import re
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
from .pokeconfg import *
from .pokemon import *
from .PokeCounter import *
from .until import *

sv = Service('pokemon', enable_on_default=True)

@sv.on_fullmatch(['精灵帮助','宝可梦帮助'])
async def pokemon_help(bot, ev: CQEvent):
    msg='''  
             宝可梦帮助
1、初始精灵列表(查询可以领取的初始精灵)
2、领取初始精灵[精灵名](领取初始精灵[精灵名])
3、精灵状态[精灵名](查询[精灵名]的属性信息)
4、我的精灵列表(查询我拥有的等级前20的精灵)
5、宝可梦重开(删除我所有的精灵信息)
6、放生精灵[精灵名](放生名为[精灵名]的精灵)
7、学习精灵技能[精灵名] [技能名](让精灵学习技能[非学习机技能])
8、遗忘精灵技能[精灵名] [技能名](让精灵遗忘技能)
注:
同一类型的精灵只能拥有一只(进化型为不同类型)
后续功能在写了在写了(新建文件夹)
 '''
    await bot.send(ev, msg)

@sv.on_prefix(['技能伤害测试'])
async def get_jn_poke_info(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)<3:
        await bot.finish(ev, '请输入 技能伤害测试+我方宝可梦名称+敌方宝可梦名称+技能名称 中间用空格隔开。', at_sender=True)
    mypokename = args[0]
    dipokename = args[1]
    bianhao1 = get_poke_bianhao(mypokename)
    bianhao2 = get_poke_bianhao(dipokename)
    if bianhao1 == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    if bianhao2 == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    jineng1 = args[2]
    jineng2 = args[3]
    
    tianqi = args[4]
    
    if len(args)>=7:
        zhuangtai1 = args[5]
        zhuangtai2 = args[6]
    else:
        zhuangtai1 = "无"
        zhuangtai2 = "无"
    
    try:
        gid = ev.group_id
        uid = ev.user_id
        jinenginfo1 = JINENG_LIST[jineng1]
        if jinenginfo1[6] == '':
            await bot.finish(ev, f'{jineng1}的技能效果在写了在写了(新建文件夹)。', at_sender=True)
            
        jinenginfo2 = JINENG_LIST[jineng2]
        if jinenginfo2[6] == '':
            await bot.finish(ev, f'{jineng2}的技能效果在写了在写了(新建文件夹)。', at_sender=True)
        
        mypokemon_info = get_pokeon_info_sj(gid,uid,bianhao1)
        dipokemon_info = get_pokeon_info_sj(gid,uid,bianhao2)
        myinfo = []
        diinfo = []
        
        #名称
        myinfo.append(POKEMON_LIST[bianhao1][0])
        diinfo.append(POKEMON_LIST[bianhao2][0])
        #属性
        myinfo.append(POKEMON_LIST[bianhao1][7])
        diinfo.append(POKEMON_LIST[bianhao2][7])
        #等级
        myinfo.append(mypokemon_info[0])
        diinfo.append(dipokemon_info[0])
        
        myshux = []
        dishux = []
        myshux = get_pokemon_shuxing(gid,uid,bianhao1,mypokemon_info)
        dishux = get_pokemon_shuxing(gid,uid,bianhao2,dipokemon_info)
        
        #属性值HP,ATK,DEF,SP.ATK,SP.DEF,SPD
        for shuzhimy in myshux:
            myinfo.append(shuzhimy)
        
        for shuzhidi in dishux:
            diinfo.append(shuzhidi)
        
        #状态等级 攻击等级,防御等级,特攻等级,特防等级,速度等级,要害等级,闪避等级,命中等级
        for num in range(1,9):
            myinfo.append(0)
            diinfo.append(0)
        
        #剩余血量
        myinfo.append(myshux[0])
        diinfo.append(dishux[0])
        
        mes = f'生成测试精灵成功\n我方\n{POKEMON_LIST[bianhao1][0]}\nLV:{mypokemon_info[0]}\n属性:{POKEMON_LIST[bianhao1][7]}\n性格:{mypokemon_info[13]}\nHP:{myshux[0]}({mypokemon_info[1]})\n物攻:{myshux[1]}({mypokemon_info[2]})\n物防:{myshux[2]}({mypokemon_info[3]})\n特攻:{myshux[3]}({mypokemon_info[4]})\n特防:{myshux[4]}({mypokemon_info[5]})\n速度:{myshux[5]}({mypokemon_info[6]})\n努力值:{mypokemon_info[7]},{mypokemon_info[8]},{mypokemon_info[9]},{mypokemon_info[10]},{mypokemon_info[11]},{mypokemon_info[12]}\n'
        mes = mes + f'敌方\n{POKEMON_LIST[bianhao2][0]}\nLV:{dipokemon_info[0]}\n属性:{POKEMON_LIST[bianhao2][7]}\n性格:{dipokemon_info[13]}\nHP:{dishux[0]}({dipokemon_info[1]})\n物攻:{dishux[1]}({dipokemon_info[2]})\n物防:{dishux[2]}({dipokemon_info[3]})\n特攻:{dishux[3]}({dipokemon_info[4]})\n特防:{dishux[4]}({dipokemon_info[5]})\n速度:{dishux[5]}({dipokemon_info[6]})\n努力值:{dipokemon_info[7]},{dipokemon_info[8]},{dipokemon_info[9]},{dipokemon_info[10]},{dipokemon_info[11]},{dipokemon_info[12]}\n'
        await bot.send(ev, mes, at_sender=True)
        mes = ''
        changdi = [[tianqi, 3],['', 0]]
        myzhuangtai = [[zhuangtai1, 3],['无', 0]]
        dizhuangtai = [[zhuangtai2, 3],['无', 0]]
        shul = 1
        jieshu = 0
        while jieshu == 0:
            await bot.send(ev, f"回合：{shul}", at_sender=True)
            shul = shul + 1
            mysd = get_nowshuxing(myinfo[8], myinfo[13])
            if myzhuangtai[0][0] == '麻痹' and int(myzhuangtai[0][1])>0:
                mysd = int(mysd*0.5)
            disd = get_nowshuxing(diinfo[8], diinfo[13])
            if dizhuangtai[0][0] == '麻痹' and int(dizhuangtai[0][1])>0:
                disd = int(mysd*0.5)
            
            #先手判断
            myxianshou = 1
            if jineng1 in xianzhi or jineng2 in xianzhi:
                if jineng1 in xianzhi and jineng2 in xianzhi:
                    if mysd < disd:
                        myxianshou = 0
                else:
                    if jineng1 in xianzhi:
                        myxianshou = 1
                    if jineng2 in xianzhi:
                        myxianshou = 0
            elif jineng1 in youxian or jineng2 in youxian:
                if jineng1 in youxian and jineng2 in youxian:
                    if mysd < disd:
                        myxianshou = 0
                else:
                    if jineng1 in youxian:
                        myxianshou = 1
                    if jineng2 in youxian:
                        myxianshou = 0
            else:
                if mysd < disd:
                    myxianshou = 0
            
            #判断我方能否发动攻击
            mychushou = 1
            if myzhuangtai[0][0] in tingzhilist and int(myzhuangtai[0][1]) > 0:
                mychushou = 0
            if myzhuangtai[0][0] in chushoulist and int(myzhuangtai[0][1]) > 0:
                if myzhuangtai[0][0] == '麻痹':
                    shuzhi = 25
                if myzhuangtai[0][0] == '混乱':
                    shuzhi = 33
                suiji = int(math.floor(random.uniform(0,100)))
                if suiji <= shuzhi:
                    mychushou = 0
            
            #判断敌方能否发动攻击
            dichushou = 1
            if dizhuangtai[0][0] in tingzhilist and int(dizhuangtai[0][1]) > 0:
                dichushou = 0
            if dizhuangtai[0][0] in chushoulist and int(dizhuangtai[0][1]) > 0:
                if dizhuangtai[0][0] == '麻痹':
                    shuzhi = 25
                if dizhuangtai[0][0] == '混乱':
                    shuzhi = 33
                suiji = int(math.floor(random.uniform(0,100)))
                if suiji <= shuzhi:
                    dichushou = 0
            
            #双方出手
            if myxianshou == 1:
                if mychushou == 1:
                    #我方攻击
                    canshu1 = {'jineng':jineng1,'myinfo':myinfo,'diinfo':diinfo,'myzhuangtai':myzhuangtai,'dizhuangtai':dizhuangtai,'changdi':changdi}
                    exec(f'ret = {jinenginfo1[6]}', globals(), canshu1)
                    mes,myinfo,diinfo,myzhuangtai,dizhuangtai,changdi = canshu1['ret']
                    await bot.send(ev, mes, at_sender=True)
                else:
                    if myzhuangtai[0][0] == '混乱' and int(myzhuangtai[0][1]) > 0:
                        mes,myinfo,diinfo,myzhuangtai,dizhuangtai,changdi = get_hunluan_sh(myinfo,diinfo,myzhuangtai,dizhuangtai,changdi)
                        await bot.send(ev, mes, at_sender=True)
                        
                    else:
                        mes = f"{myinfo[0]}{myzhuangtai[0][0]}中，技能发动失败"
                        await bot.send(ev, mes, at_sender=True)
                if myinfo[17] == 0 or diinfo[17] == 0:
                    jieshu = 1
                    break
                
                if dichushou == 1:
                    #敌方攻击
                    canshu2 = {'jineng':jineng2,'myinfo':diinfo,'diinfo':myinfo,'myzhuangtai':dizhuangtai,'dizhuangtai':myzhuangtai,'changdi':changdi}
                    exec(f'ret = {jinenginfo2[6]}', globals(), canshu2)
                    mes,diinfo,myinfo,dizhuangtai,myzhuangtai,changdi = canshu2['ret']
                    await bot.send(ev, mes, at_sender=True)
                else:
                    if dizhuangtai[0][0] == '混乱' and int(dizhuangtai[0][1]) > 0:
                        mes,diinfo,myinfo,dizhuangtai,myzhuangtai,changdi = get_hunluan_sh(diinfo,myinfo,dizhuangtai,myzhuangtai,changdi)
                        await bot.send(ev, mes, at_sender=True)
                    else:
                        mes = f"{diinfo[0]}{dizhuangtai[0][0]}中，技能发动失败"
                        await bot.send(ev, mes, at_sender=True)
                if myinfo[17] == 0 or diinfo[17] == 0:
                    jieshu = 1
                    break
            
            else:
                if dichushou == 1:
                    #敌方攻击
                    canshu2 = {'jineng':jineng2,'myinfo':diinfo,'diinfo':myinfo,'myzhuangtai':dizhuangtai,'dizhuangtai':myzhuangtai,'changdi':changdi}
                    exec(f'ret = {jinenginfo2[6]}', globals(), canshu2)
                    mes,diinfo,myinfo,dizhuangtai,myzhuangtai,changdi = canshu2['ret']
                    await bot.send(ev, mes, at_sender=True)
                else:
                    if dizhuangtai[0][0] == '混乱' and int(dizhuangtai[0][1]) > 0:
                        mes,diinfo,myinfo,dizhuangtai,myzhuangtai,changdi = get_hunluan_sh(diinfo,myinfo,dizhuangtai,myzhuangtai,changdi)
                        await bot.send(ev, mes, at_sender=True)
                    else:
                        mes = f"{diinfo[0]}{dizhuangtai[0][0]}中，技能发动失败"
                        await bot.send(ev, mes, at_sender=True)
                if myinfo[17] == 0 or diinfo[17] == 0:
                    jieshu = 1
                    break
                
                if mychushou == 1:
                    #我方攻击
                    canshu1 = {'jineng':jineng1,'myinfo':myinfo,'diinfo':diinfo,'myzhuangtai':myzhuangtai,'dizhuangtai':dizhuangtai,'changdi':changdi}
                    exec(f'ret = {jinenginfo1[6]}', globals(), canshu1)
                    mes,myinfo,diinfo,myzhuangtai,dizhuangtai,changdi = canshu1['ret']
                    await bot.send(ev, mes, at_sender=True)
                else:
                    if myzhuangtai[0][0] == '混乱' and int(myzhuangtai[0][1]) > 0:
                        mes,myinfo,diinfo,myzhuangtai,dizhuangtai,changdi = get_hunluan_sh(myinfo,diinfo,myzhuangtai,dizhuangtai,changdi)
                        await bot.send(ev, mes, at_sender=True)
                    else:
                        mes = f"{myinfo[0]}{myzhuangtai[0][0]}中，技能发动失败"
                        await bot.send(ev, mes, at_sender=True)
                if myinfo[17] == 0 or diinfo[17] == 0:
                    jieshu = 1
                    break
            
            #回合结束天气与状态伤害计算
            if myzhuangtai[0][0] in kouxuelist and int(myzhuangtai[0][1]) > 0:
                mes,myinfo,diinfo,myzhuangtai,dizhuangtai,changdi = get_zhuangtai_sh(myinfo,diinfo,myzhuangtai,dizhuangtai,changdi)
                await bot.send(ev, mes, at_sender=True)
            if myinfo[17] == 0 or diinfo[17] == 0:
                jieshu = 1
                break
            
            if dizhuangtai[0][0] in kouxuelist and int(dizhuangtai[0][1]) > 0:
                mes,diinfo,myinfo,dizhuangtai,myzhuangtai,changdi = get_zhuangtai_sh(diinfo,myinfo,dizhuangtai,myzhuangtai,changdi)
                await bot.send(ev, mes, at_sender=True)
            if myinfo[17] == 0 or diinfo[17] == 0:
                jieshu = 1
                break
            
            if changdi[0][0] in tq_kouxuelist and int(changdi[0][1]) > 0:
                mes,myinfo,diinfo,myzhuangtai,dizhuangtai,changdi = get_tianqi_sh(myinfo,diinfo,myzhuangtai,dizhuangtai,changdi)
                await bot.send(ev, mes, at_sender=True)
            if myinfo[17] == 0 or diinfo[17] == 0:
                jieshu = 1
                break
            
            if myzhuangtai[0][0] in hh_yichanglist and int(myzhuangtai[0][1]) > 0:
                myshengyuyc = int(myzhuangtai[0][1]) - 1
                if myshengyuyc == 0:
                    await bot.send(ev, f"{myinfo[0]}的{myzhuangtai[0][0]}状态解除了", at_sender=True)
                    myzhuangtai[0][0] = '无'
                    myzhuangtai[0][1] = 0
                else:
                    myzhuangtai[0][1] = myshengyuyc
                    
            if dizhuangtai[0][0] in hh_yichanglist and int(dizhuangtai[0][1]) > 0:
                dishengyuyc = int(dizhuangtai[0][1]) - 1
                if dishengyuyc == 0:
                    await bot.send(ev, f"{diinfo[0]}的{dizhuangtai[0][0]}状态解除了", at_sender=True)
                    dizhuangtai[0][0] = '无'
                    dizhuangtai[0][1] = 0
                else:
                    dizhuangtai[0][1] = dishengyuyc
            
            if myzhuangtai[0][0] in jiechulist and int(myzhuangtai[0][1]) > 0:
                suiji = int(math.floor(random.uniform(0,100)))
                if suiji <= 20:
                    await bot.send(ev, f"{myinfo[0]}的{myzhuangtai[0][0]}状态解除了", at_sender=True)
                    myzhuangtai[0][0] = '无'
                    myzhuangtai[0][1] = 0

            if dizhuangtai[0][0] in jiechulist and int(dizhuangtai[0][1]) > 0:
                suiji = int(math.floor(random.uniform(0,100)))
                if suiji <= 20:
                    await bot.send(ev, f"{diinfo[0]}的{dizhuangtai[0][0]}状态解除了", at_sender=True)
                    dizhuangtai[0][0] = '无'
                    dizhuangtai[0][1] = 0
            
            if int(changdi[0][1]) > 0 and changdi[0][0] != '无天气':
                shengyutianqi = int(changdi[0][1]) - 1
                if shengyutianqi == 0:
                    await bot.send(ev, f"{changdi[0][0]}停止了，天气影响消失了", at_sender=True)
                    changdi[0][0] = '无天气'
                    changdi[0][1] = 99
                else:
                    changdi[0][1] = shengyutianqi
                    await bot.send(ev, f"{changdi[0][0]}持续中", at_sender=True)
            
    except:
        await bot.finish(ev, '无法找到该技能，请输入正确的技能名称。', at_sender=True)
    

@sv.on_prefix(['属性测试'])
async def get_aj_poke_info(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)!=1:
        await bot.finish(ev, '请输入 属性测试+宝可梦名称 中间用空格隔开。', at_sender=True)
    pokename = args[0]
    gid = ev.group_id
    uid = ev.user_id
    bianhao = get_poke_bianhao(pokename)
    if bianhao == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    pokemon_info = get_pokeon_info_sj(gid,uid,bianhao)
    HP,W_atk,W_def,M_atk,M_def,speed = get_pokemon_shuxing(gid,uid,bianhao,pokemon_info)
    picfile = os.path.join(FILE_PATH, 'icon', f'{POKEMON_LIST[bianhao][0]}.png')
    mes = f"[CQ:image,file=file:///{os.path.abspath(picfile)}]\n"
    mes = mes + f'{POKEMON_LIST[bianhao][0]}\nLV:{pokemon_info[0]}\n属性:{POKEMON_LIST[bianhao][7]}\n性格:{pokemon_info[13]}\n属性值[种族值](个体值)\nHP:{HP}[{POKEMON_LIST[bianhao][1]}]({pokemon_info[1]})\n物攻:{W_atk}[{POKEMON_LIST[bianhao][2]}]({pokemon_info[2]})\n物防:{W_def}[{POKEMON_LIST[bianhao][3]}]({pokemon_info[3]})\n特攻:{M_atk}[{POKEMON_LIST[bianhao][4]}]({pokemon_info[4]})\n特防:{M_def}[{POKEMON_LIST[bianhao][5]}]({pokemon_info[5]})\n速度:{speed}[{POKEMON_LIST[bianhao][6]}]({pokemon_info[6]})\n努力值:{pokemon_info[7]},{pokemon_info[8]},{pokemon_info[9]},{pokemon_info[10]},{pokemon_info[11]},{pokemon_info[12]}\n'
    mes = mes + f'可用技能\n{pokemon_info[14]}'
    jinenglist = get_level_jineng(pokemon_info[0],bianhao)
    mes = mes + '\n当前等级可学习的技能为：\n'
    for jn_name in jinenglist:
        mes = mes + f'{jn_name},'
    await bot.send(ev, mes, at_sender=True)

@sv.on_fullmatch(['我的精灵列表'])
async def my_pokemon_list(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    POKE = PokeCounter()
    mypokelist = POKE._get_pokemon_list(gid,uid)
    if mypokelist == 0:
        await bot.finish(ev, '您还没有精灵，请输入 初始精灵列表 开局。', at_sender=True)
    mes = '您的精灵信息为(只显示等级最高的前20只):\n'
    for pokemoninfo in mypokelist:
        mes = mes + f'{POKEMON_LIST[pokemoninfo[0]][0]}({pokemoninfo[1]}),'
    await bot.send(ev, mes, at_sender=True)

@sv.on_prefix(['精灵状态'])
async def get_my_poke_info(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)!=1:
        await bot.finish(ev, '请输入 我的精灵+宝可梦名称 中间用空格隔开。', at_sender=True)
    pokename = args[0]
    gid = ev.group_id
    uid = ev.user_id
    bianhao = get_poke_bianhao(pokename)
    if bianhao == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    pokemon_info = get_pokeon_info(gid,uid,bianhao)
    if pokemon_info == 0:
        await bot.finish(ev, f'您还没有{POKEMON_LIST[bianhao][0]}。', at_sender=True)
    HP,W_atk,W_def,M_atk,M_def,speed = get_pokemon_shuxing(gid,uid,bianhao,pokemon_info)
    picfile = os.path.join(FILE_PATH, 'icon', f'{POKEMON_LIST[bianhao][0]}.png')
    mes = f"[CQ:image,file=file:///{os.path.abspath(picfile)}]\n"
    mes = mes + f'{POKEMON_LIST[bianhao][0]}\nLV:{pokemon_info[0]}\n属性:{POKEMON_LIST[bianhao][7]}\n性格:{pokemon_info[13]}\n属性值[种族值](个体值)\nHP:{HP}[{POKEMON_LIST[bianhao][1]}]({pokemon_info[1]})\n物攻:{W_atk}[{POKEMON_LIST[bianhao][2]}]({pokemon_info[2]})\n物防:{W_def}[{POKEMON_LIST[bianhao][3]}]({pokemon_info[3]})\n特攻:{M_atk}[{POKEMON_LIST[bianhao][4]}]({pokemon_info[4]})\n特防:{M_def}[{POKEMON_LIST[bianhao][5]}]({pokemon_info[5]})\n速度:{speed}[{POKEMON_LIST[bianhao][6]}]({pokemon_info[6]})\n努力值:{pokemon_info[7]},{pokemon_info[8]},{pokemon_info[9]},{pokemon_info[10]},{pokemon_info[11]},{pokemon_info[12]}\n'
    mes = mes + f'可用技能\n{pokemon_info[14]}'
    jinenglist = get_level_jineng(pokemon_info[0],bianhao)
    mes = mes + '\n当前等级可学习的技能为：\n'
    for jn_name in jinenglist:
        mes = mes + f'{jn_name},'
    await bot.send(ev, mes, at_sender=True)
    
@sv.on_fullmatch(['初始精灵列表'])
async def get_chushi_list(bot, ev: CQEvent):
    tas_list = []
    for bianhao in chushi_list:
        mes = ''
        picfile = os.path.join(FILE_PATH, 'icon', f'{POKEMON_LIST[bianhao][0]}.png')
        mes = mes + f"[CQ:image,file=file:///{os.path.abspath(picfile)}]\n"
        mes = mes + f"{POKEMON_LIST[bianhao][0]}\n属性:{POKEMON_LIST[bianhao][7]}"
        data = {
            "type": "node",
            "data": {
                "name": "ご主人様",
                "uin": "1587640710",
                "content":mes
                    }
                }
        tas_list.append(data)
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=tas_list)

@sv.on_prefix(['领取初始精灵'])
async def get_chushi_pokemon(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)!=1:
        await bot.finish(ev, '请输入 领取初始精灵+宝可梦名称 中间用空格隔开。', at_sender=True)
    pokename = args[0]
    gid = ev.group_id
    uid = ev.user_id
    
    POKE = PokeCounter()
    mypokelist = POKE._get_pokemon_list(gid,uid)
    if mypokelist != 0:
        await bot.finish(ev, '您已经有精灵了，无法领取初始精灵。', at_sender=True)
    
    bianhao = get_poke_bianhao(pokename)
    if bianhao == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    if bianhao not in chushi_list:
        await bot.finish(ev, f'{POKEMON_LIST[bianhao][0]}不属于初始精灵，无法领取。', at_sender=True)
    pokemon_info = add_pokemon(gid,uid,bianhao)
    HP,W_atk,W_def,M_atk,M_def,speed = get_pokemon_shuxing(gid,uid,bianhao,pokemon_info)
    picfile = os.path.join(FILE_PATH, 'icon', f'{POKEMON_LIST[bianhao][0]}.png')
    mes = f"恭喜！您领取到了初始精灵\n"
    mes = mes + f"[CQ:image,file=file:///{os.path.abspath(picfile)}]\n"
    mes = mes + f'{POKEMON_LIST[bianhao][0]}\nLV:{pokemon_info[0]}\n属性:{POKEMON_LIST[bianhao][7]}\n性格:{pokemon_info[13]}\nHP:{HP}({pokemon_info[1]})\n物攻:{W_atk}({pokemon_info[2]})\n物防:{W_def}({pokemon_info[3]})\n特攻:{M_atk}({pokemon_info[4]})\n特防:{M_def}({pokemon_info[5]})\n速度:{speed}({pokemon_info[6]})\n'
    mes = mes + f'可用技能\n{pokemon_info[14]}'
    await bot.send(ev, mes, at_sender=True)
    
@sv.on_fullmatch(['宝可梦重开'])
async def chongkai_pokemon(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    chongkai(gid,uid)
    await bot.send(ev, '重开成功，请重新领取初始精灵开局', at_sender=True)
    
@sv.on_prefix(['放生精灵'])
async def fangsheng_pokemon(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)!=1:
        await bot.finish(ev, '请输入 放生精灵+宝可梦名称 中间用空格隔开。', at_sender=True)
    pokename = args[0]
    gid = ev.group_id
    uid = ev.user_id
    bianhao = get_poke_bianhao(pokename)
    if bianhao == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    pokemon_info = get_pokeon_info(gid,uid,bianhao)
    if pokemon_info == 0:
        await bot.finish(ev, f'您还没有{POKEMON_LIST[bianhao][0]}。', at_sender=True)
    fangshen(gid,uid,bianhao)
    await bot.send(ev, f'放生成功，{POKEMON_LIST[bianhao][0]}离你而去了', at_sender=True)
    
@sv.on_prefix(['学习精灵技能'])
async def add_pokemon_jineng(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)!=2:
        await bot.finish(ev, '请输入 学习精灵技能+宝可梦名称+技能名称 中间用空格隔开。', at_sender=True)
    pokename = args[0]
    gid = ev.group_id
    uid = ev.user_id
    bianhao = get_poke_bianhao(pokename)
    if bianhao == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    pokemon_info = get_pokeon_info(gid,uid,bianhao)
    if pokemon_info == 0:
        await bot.finish(ev, f'您还没有{POKEMON_LIST[bianhao][0]}。', at_sender=True)
    jinengname = args[1]
    if str(jinengname) in str(pokemon_info[14]):
        await bot.finish(ev, f'学习失败，您的精灵{POKEMON_LIST[bianhao][0]}已学会{jinengname}。', at_sender=True)
    jinenglist = re.split(',',pokemon_info[14])
    if len(jinenglist) >= 4:
        await bot.finish(ev, f'学习失败，您的精灵{POKEMON_LIST[bianhao][0]}已学会4个技能，请先遗忘一个技能后再学习。', at_sender=True)
    jinengzu = get_level_jineng(pokemon_info[0],bianhao)
    if jinengname not in jinengzu:
        await bot.finish(ev, f'学习失败，不存在该技能或该技能无法在当前等级学习(学习机技能请使用技能学习机进行教学)。', at_sender=True)
    jineng = pokemon_info[14] + ',' + jinengname
    POKE = PokeCounter()
    POKE._add_pokemon_jineng(gid, uid, bianhao, jineng)
    await bot.send(ev, f'恭喜，您的精灵{POKEMON_LIST[bianhao][0]}学会了技能{jinengname}', at_sender=True)
    
@sv.on_prefix(['遗忘精灵技能'])
async def del_pokemon_jineng(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)!=2:
        await bot.finish(ev, '请输入 学习精灵技能+宝可梦名称+技能名称 中间用空格隔开。', at_sender=True)
    pokename = args[0]
    gid = ev.group_id
    uid = ev.user_id
    bianhao = get_poke_bianhao(pokename)
    if bianhao == 0:
        await bot.finish(ev, '请输入正确的宝可梦名称。', at_sender=True)
    pokemon_info = get_pokeon_info(gid,uid,bianhao)
    if pokemon_info == 0:
        await bot.finish(ev, f'您还没有{POKEMON_LIST[bianhao][0]}。', at_sender=True)
    jinengname = args[1]
    if str(jinengname) not in str(pokemon_info[14]):
        await bot.finish(ev, f'遗忘失败，您的精灵{POKEMON_LIST[bianhao][0]}未学习{jinengname}。', at_sender=True)
    jinenglist = re.split(',',pokemon_info[14])
    jinenglist.remove(jinengname)
    jineng = ''
    shul = 0
    for name in jinenglist:
        if shul>0:
            jineng = jineng + ','
        jineng = jineng + name
        shul = shul + 1
    POKE = PokeCounter()
    POKE._add_pokemon_jineng(gid, uid, bianhao, jineng)
    await bot.send(ev, f'成功，您的精灵{POKEMON_LIST[bianhao][0]}遗忘了技能{jinengname}', at_sender=True)
    
@sv.on_prefix(['精灵技能信息'])
async def get_jineng_info(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args)!=1:
        await bot.finish(ev, '请输入 精灵技能信息+技能名称 中间用空格隔开。', at_sender=True)
    jineng = args[0]
    try:
        jinenginfo = JINENG_LIST[jineng]
        mes = f'名称：{jineng}\n属性：{jinenginfo[0]}\n类型：{jinenginfo[1]}\n威力：{jinenginfo[2]}\n命中：{jinenginfo[3]}\nPP值：{jinenginfo[4]}\n描述：{jinenginfo[5]}'
        await bot.send(ev, mes)
    except:
        await bot.finish(ev, '无法找到该技能，请输入正确的技能名称。', at_sender=True)