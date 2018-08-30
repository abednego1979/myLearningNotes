# -*- coding: utf-8 -*-

#Python 3.5.x

#V0.01

import os
import re
import datetime

import sympy
import xlrd
import xlutils.copy

EXCEL_NAME="21-模型基础参数.xlsx"


__metaclass__ = type

class BaseEleMent():
    #name=""                 #英文名字
    #name_cn=""              #中文名
    #index=0                #索引
    #value=0.0               #如果是参数，这里是参数值，如果是过程量，这里是依赖的过程量算法

    def __init__(self, name="", name_cn="", index=0, pos="", value=0.0):
        self.name=name
        self.name_cn=name_cn
        self.index=index
        self.value=value
        self.pos=pos
        
all_factor=[\
    BaseEleMent(pos="D06", index="L01", name="FaDianLiang", name_cn="发电量", value=2850000.0),\
    BaseEleMent(pos="D07", index="L02", name="FaDianChangYongDianLiang", name_cn="发电厂用电量", value="(L01)*(L08)/100.0"),\
    BaseEleMent(pos="D08", index="L03", name="GongReChangYongDianLiang", name_cn="供热厂用电量", value="(L07)*(L09)/1000.0"),\
    BaseEleMent(pos="D09", index="L04", name="GongDianLiang", name_cn="供电量", value="(L01)-(L02)"),\
    BaseEleMent(pos="D10", index="L05", name="XianSunLiang", name_cn="线损量", value="(L04)-(L06)"),\
    BaseEleMent(pos="D11", index="L06", name="ShangWangDianLiang", name_cn="上网电量", value="(L01)*(1-(L10)/100.0)"),\
    BaseEleMent(pos="D12", index="L07", name="GongReLiang", name_cn="供热量", value=5000000.0),\
    BaseEleMent(pos="D13", index="L08", name="FaDianChangYongDianLv", name_cn="发电厂用电率", value=6.0),\
    BaseEleMent(pos="D14", index="L09", name="GongReChangYongDianLv", name_cn="供热厂用电率", value=9.7),\
    BaseEleMent(pos="D15", index="L10", name="ZhongHeChangYongDianLv", name_cn="综合厂用电率", value=8.23),\
    BaseEleMent(pos="D16", index="L11", name="FaDianMeiHao", name_cn="发电煤耗", value="(L13)*(L04)/(L01)"),\
    BaseEleMent(pos="D17", index="L12", name="ShangWangMeiHao", name_cn="上网煤耗", value="(L13)*(L04)/(L06)"),\
    BaseEleMent(pos="D18", index="L13", name="GongDianMeiHao", name_cn="供电煤耗", value=288.0),\
    BaseEleMent(pos="D19", index="L14", name="GongReMeiHao", name_cn="供热煤耗", value=40.0),\
    BaseEleMent(pos="D20", index="L15", name="FaDianGongReBiaoMeiLiang", name_cn="发电供热标煤量", value="(L16)+(L17)"),\
    BaseEleMent(pos="D21", index="L16", name="FaDiaBiaoMeiLiangn", name_cn="发电标煤量", value="(L11)*(L01)/1000.0"),\
    BaseEleMent(pos="D22", index="L17", name="GongReBiaoMeiLiang", name_cn="供热标煤量", value="(L14)*(L07)/1000.0"),\
    BaseEleMent(pos="D23", index="L18", name="GongReYongDianFenTanMeiLiang", name_cn="供热厂用电分摊煤量", value="(L03)*(L13)/1000.0"),\
    BaseEleMent(pos="D24", index="L19", name="GongReChangYongDianFenTanRanLiaoFei", name_cn="供热厂用电分摊燃料费", value="(L07)*(L09)*(L13)*(L23)/10000000000.0"),\
    BaseEleMent(pos="D25", index="L20", name="LiYongXiaoShi", name_cn="利用小时", value="(L01)/(L21)"),\
    BaseEleMent(pos="D26", index="L21", name="JiZhuRongLiang", name_cn="机组容量", value=600.0),\
    BaseEleMent(pos="D27", index="L22", name="FaDianBianJiLiRun", name_cn="发电边际利润", value="(L25)/1.16-(L52)"),\
    BaseEleMent(pos="D28", index="L23", name="ZhongHeBiaoMeiDanJia", name_cn="综合标煤单价", value=588.93),\
    BaseEleMent(pos="D30", index="L24", name="DianLiShouRu", name_cn="电力收入", value="(L28)+(L31)+(L34)+(L37)"),\
    BaseEleMent(pos="D31", index="L25", name="PingJunShangWangDianJia_HanShui", name_cn="平均上网电价（含税）", value="(L24)*1.16/(L06)*10000"),\
    BaseEleMent(pos="D32", index="L26", name="ShangWangDianLiang1_JiShuDIanLiang", name_cn="上网电量1（基数电量）", value=940775.5665),\
    BaseEleMent(pos="D33", index="L27", name="ShangWangDianJia1_HanShui", name_cn="上网电价1（含税）", value=374.9),\
    BaseEleMent(pos="D34", index="L28", name="ShangWangDianJia1ShouRu", name_cn="上网电价1收入", value="(L26)*(L27)/1.16/10000"),\
    BaseEleMent(pos="D35", index="L29", name="ShangWangDianLiang2_KuaQuDianLiang", name_cn="上网电量2(跨区电量）", value=115079.58),\
    BaseEleMent(pos="D36", index="L30", name="ShangWangDianJia2_HanShui", name_cn="上网电价2（含税）", value=305.62),\
    BaseEleMent(pos="D37", index="L31", name="ShangWangDianJia2ShouRu", name_cn="上网电价2收入", value="(L29)*(L30)/1.16/10000"),\
    BaseEleMent(pos="D38", index="L32", name="ShangWangDianLiang3_TiDaiDianLiang", name_cn="上网电量3(替代电量）", value=313591.8555),\
    BaseEleMent(pos="D39", index="L33", name="ShangWangDianJia3_HanShui", name_cn="上网电价3（含税）", value=320.0),\
    BaseEleMent(pos="D40", index="L34", name="ShangWangDianJia3ShouRu", name_cn="上网电价3收入", value="(L32)*(L33)/1.16/10000"),\
    BaseEleMent(pos="D41", index="L35", name="ShangWangDianLiang4_DaYongHuDianLiang", name_cn="上网电量4(大用户电量）", value=1245997.998),\
    BaseEleMent(pos="D42", index="L36", name="ShangWangDianJia4_HanShui", name_cn="上网电价4（含税）", value=355.0),\
    BaseEleMent(pos="D43", index="L37", name="ShangWangDianJia4ShouRu", name_cn="上网电价4收入", value="(L35)*(L36)/1.16/10000"),\
    BaseEleMent(pos="D44", index="L38", name="ReLiShouRu", name_cn="热力收入", value="(L39)*(L40)/11000"),\
    BaseEleMent(pos="D45", index="L39", name="PingJunReJia", name_cn="平均热价（含税）", value=30.0),\
    BaseEleMent(pos="D46", index="L40", name="DuiWaiGongReLiang", name_cn="对外供热量", value="(L07)"),\
    BaseEleMent(pos="D48", index="L41", name="YingYeShouRu", name_cn="营业收入", value="(L42)+(L46)"),\
    BaseEleMent(pos="D49", index="L42", name="ZhuYingYeWuShouRu", name_cn="主营业务收入", value="(L43)+(L44)+(L45)"),\
    BaseEleMent(pos="D50", index="L43", name="DianLi_ZhuYingYeWuShouRu", name_cn="电力", value="(L24)"),\
    BaseEleMent(pos="D51", index="L44", name="ReLi_ZhuYingYeWuShouRu", name_cn="热力", value="(L38)"),\
    BaseEleMent(pos="D52", index="L45", name="QiTa_ZhuYingYeWuShouRu", name_cn="其他", value=700.0),\
    BaseEleMent(pos="D53", index="L46", name="QiTaYeWuShouRu", name_cn="其他业务收入", value=1495.73),\
    BaseEleMent(pos="D54", index="L47", name="YingYeChengBen", name_cn="营业成本", value="(L48)+(L62)"),\
    BaseEleMent(pos="D55", index="L48", name="ZhuYingYeWuChengBen", name_cn="主营业务成本", value="(L49)+(L54)+(L55)+(L56)+(L57)+(L58)+(L59)+(L60)+(L61)"),\
    BaseEleMent(pos="D56", index="L49", name="RanLiao_ZhuYingYeWuChengBen", name_cn="燃料", value="(L50)+(L51)"),\
    BaseEleMent(pos="D57", index="L50", name="DianLi_RanLiao_ZhuYingYeWuChengBen", name_cn="电力", value="((L01)-((L01)*(L08)/100.0))*(L13)/1000.0*(L23)/10000.0-(L07)*(L09)*(L13)*(L23)/10000000000.0"),\
    BaseEleMent(pos="D58", index="L51", name="RenLi_RanLiao_ZhuYingYeWuChengBen", name_cn="热力", value="(L07)*(L14)/1000.0*(L23)/10000.0+(L07)*(L09)*(L13)*(L23)/10000000000"),\
    BaseEleMent(pos="D59", index="L52", name="FaDianDanWeiRanLiaoChengBen", name_cn="发电单位燃料成本", value="(L50)*10000/(L06)"),\
    BaseEleMent(pos="D60", index="L53", name="GongReDanWeiRanLiaoChengBen", name_cn="供热单位燃料成本", value="(L51)*10000/(L07)"),\
    BaseEleMent(pos="D61", index="L54", name="HuanBaoFei", name_cn="环保费", value=1107.0),\
    BaseEleMent(pos="D62", index="L55", name="GouRuDianLiFei", name_cn="购入电力费", value=0.0),\
    BaseEleMent(pos="D63", index="L56", name="ShuiFeiJiShuiZiYuanFei", name_cn="水费及水资源费", value=1019.02938506921),\
    BaseEleMent(pos="D64", index="L57", name="CaiLiaoFei", name_cn="材料费", value=1388.4),\
    BaseEleMent(pos="D65", index="L58", name="ZhiGongXinChou", name_cn="职工薪酬", value=8884.0),\
    BaseEleMent(pos="D66", index="L59", name="ZeJiu", name_cn="折旧", value=18126.63),\
    BaseEleMent(pos="D67", index="L60", name="XiuLiFei", name_cn="修理费", value=2178.0),\
    BaseEleMent(pos="D68", index="L61", name="QiTaFeiYong", name_cn="其他费用", value=1196.694),\
    BaseEleMent(pos="D69", index="L62", name="QiTaYeWuChengBen", name_cn="其他业务成本", value=408.98),\
    BaseEleMent(pos="D70", index="L63", name="YingYeShuiJinJiFuJia", name_cn="营业税金及附加", value=1784.84),\
    BaseEleMent(pos="D71", index="L64", name="XiaoShouFeiYong", name_cn="销售费用", value=0.0),\
    BaseEleMent(pos="D72", index="L65", name="GuanLiFeiYong", name_cn="管理费用", value=0.0),\
    BaseEleMent(pos="D73", index="L66", name="CaiWuFeiYong", name_cn="财务费用", value=7655.69),\
    BaseEleMent(pos="D74", index="L67", name="ZiChanJianZhiShunSi", name_cn="资产减值损失", value=0.0),\
    BaseEleMent(pos="D75", index="L68", name="TouZiShouYi", name_cn="投资收益", value=0.0),\
    BaseEleMent(pos="D76", index="L69", name="YingYeLiRun", name_cn="营业利润", value="(L41)-(L47)-(L63)-(L64)-(L65)-(L66)-(L67)+(L68)"),\
    BaseEleMent(pos="D77", index="L70", name="YingYeWaiShouRu", name_cn="营业外收入", value=150.0),\
    BaseEleMent(pos="D78", index="L71", name="YingYeWaiZiChu", name_cn="营业外支出", value=0.0),\
    BaseEleMent(pos="D79", index="L72", name="LiRunZongE", name_cn="利润总额", value="(L69)+(L70)-(L71)"),\
]

#设置变量参数，自动跳过非参数
def setPara(index, value=None):
    global all_factor
    
    if type(index)==int(1):
        pass
    else:
        index=[item.index for item in all_factor].index(obj)
    
    if type(all_factor[index].value)==type(1.0):
        if type(value)!=type(1.0):
            a=input(all_factor[i].name_cn+"<"+str(float(all_factor[i].value))+">=")
            if a:
                all_factor[i].value=float(a)
        else:
            all_factor[i].value=float(value)
    else:
        pass
    
    return

#所有参数都设置好的情况下计算某个表达式对应的值
def getValue(index):
    global all_factor
    
    if type(index)==type(1):
        pass
    else:
        index=[item.index for item in all_factor].index(index)
    
    temp_expression = all_factor[index].value
    
    if type(temp_expression)==type(1.0):
        return temp_expression
    else:
        while True:
            #找到temp_expression中的Lxx，替换为进一步的表达式，直到不能继续替换
            s=re.search(r'''L[0-9][0-9]''', temp_expression)
            if s:
                temp_Lxx=s.group(0)
                temp_expression=temp_expression.replace(temp_Lxx, str([item.value for item in all_factor if item.index == temp_Lxx][0]))
            else:
                break
    
    return eval(temp_expression)

#当有一个变量var的时候，得到表达方程式
#obj:要得到obj对应的表达式，Lxx格式
#var:变量，Lxx格式
def getExpression(obj, var):
    global all_factor
    
    index=[item.index for item in all_factor].index(obj)
    temp_expression = all_factor[index].value
    
    if all_factor[index].index==var:
        return "x"
    elif type(temp_expression)==type(1.0):
        return str(temp_expression)
    else:
        while True:
            #找到new_temp_expression中的Lxx，替换为进一步的表达式，直到不能继续替换
            s=re.search(r'''L[0-9][0-9]''', temp_expression)
            if s:
                temp_Lxx=s.group(0)     #找到一个Lxx
                if temp_Lxx==var:       #找到的是变量
                    temp_expression=temp_expression.replace(temp_Lxx, "x")
                else:
                    temp_expression=temp_expression.replace(temp_Lxx, str([item.value for item in all_factor if item.index == temp_Lxx][0]))
            else:
                break
    return temp_expression

#解方程的方式，求结果固定时的参数值
#obj：目标值索引，Lxx格式
#objValue：目标值的数值
#var:变量，Lxx格式
def inversionFunc(obj, objValue, var):
    global all_factor
    
    tempExp = getExpression(obj, var)       #得到obj=func(var)形式的表达式
    tempExp = tempExp+" - "+str(float(objValue))        #得到func(var)-objValue=0格式的表达式
    
    x = sympy.Symbol('x')
    res=sympy.solve(tempExp, x)         #求解
    
    #=========
    return res


#==验证公式==
#for i in range(len(all_factor)):
    #setPara(i)
#for i in range(len(all_factor)):
    ##print (all_factor[i].name_cn+"=%f" % (getValue(i)))
    #print ("%f" % (getValue(i)))
#==OVER==


#==验证反推求参数的功能==
#print (inversionFunc("L02", 171000, "L01"))
#==OVER==


print ("Start...")

#从Excel表格读取信息
def readTableSetData():
    global all_factor
    global EXCEL_NAME

    r=xlrd.open_workbook(EXCEL_NAME)
    rs=r.sheets()[0]
    
    var_list=[]
    obj_list=[]

    for i in range(len(all_factor)):
        temp_pos=all_factor[i].pos
        colx=ord(re.search(r'''[A-Z]''', temp_pos).group(0))-ord("A")
        rowx=int(re.search(r'''[0-9][0-9]''', temp_pos).group(0))-1
        if type(all_factor[i].value)==type(1.0):
            #读数据
            temp_data=rs.cell_value(rowx,colx)
            
            if temp_data:
                all_factor[i].value = float(temp_data)
            else:
                all_factor[i].value = float(0.0)
                
            temp_data=rs.cell_value(rowx,colx+2)
            if temp_data=='var':
                var_list.append(all_factor[i].index)
        else:
            temp_data=rs.cell_value(rowx,colx+2)
            if temp_data:
                obj_list.append((all_factor[i].index, float(temp_data)))

    assert len(var_list)==len(obj_list)==1
    return obj_list[0][0],obj_list[0][1],var_list[0]

#软件的要求是希望得到某个目标值的情况下，反推它依赖的某个参数的值应该是多少

#读取数据
obj, objValue, var=readTableSetData()
#obj="L02"
#objValue=172000
#var="L01"

#反推
res=inversionFunc(obj, objValue, var)
assert len(res)==1

#修改内存保存的新var值
index=[item.index for item in all_factor].index(var)
all_factor[index].value=float(res[0])

#重新计算所有的数值
for i in range(len(all_factor)):
    print (all_factor[i].name_cn+"=%f" % (getValue(i)))
    #print ("%f" % (getValue(i)))
    
#把所有的数据写回excel，固定量和变量要用不同颜色或字体凸显
rb = xlrd.open_workbook(EXCEL_NAME)
#创建一个可写入的副本
wb = xlutils.copy.copy(rb)

ws = wb.get_sheet(0)

for item in all_factor:
    temp_pos=item.pos
    colx=ord(re.search(r'''[A-Z]''', temp_pos).group(0))-ord("A")
    rowx=int(re.search(r'''[0-9][0-9]''', temp_pos).group(0))-1
    
    ws.write(rowx, colx, getValue(item.index))
wb.save("Data"+datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')+".xls")  