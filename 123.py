# import requests
# import json
# import openpyxl as op
# import pandas as pd
# from matplotlib import pyplot as plt
# import configparser
# import os
#
# iii = 1
# print(iii)
#
#
# # ------------------------------获取配置文件参数------------------------------
# def getconfig():
#     # 配置文件路径
#     curpath = os.path.dirname(os.path.realpath(__file__))
#     cfgpath = os.path.join(curpath, "config.ini")
#     # 创建对象
#     conf = configparser.ConfigParser()
#     # 读取ini文件
#     conf.read(cfgpath, encoding="utf-8")
#     # 获取所有的section
#     sections = conf.sections()
#     # 将section中config作为数组内容分传递到items
#     items = conf.items('config')
#     # 所需参数数值获取
#     projectId = items[0][1]
#     variAble = items[1][1]
#     deviceId = items[2][1]
#     APIKey = items[3][1]
#     startId = items[4][1]
#     excelId = items[5][1]
#     sheetId = items[6][1]
#     streamHttp = items[7][1]
#     pointHttp = items[8][1]
#
#     return [projectId, variAble, deviceId, APIKey, startId, excelId, sheetId, streamHttp, pointHttp]
#
#
# # ------------------------------获取onenet设备数据------------------------------
# def setconfig(did, api, startid, streamHttp, pointHttp):
#     # pid:项目名称,vae:变量名称,did:设备ID,point:数据信息,tit:设备名称,eid:excel名称及路径,sid:sheet名(形参下同)
#     # url配置参数
#     # payload = {'start': startid, 'limit': 6000}
#     # http: // api.heclouds.com / devices / 8029377 / datapoints?datastream_id = ds & start = 2017 - 01 - 01
#     # T00: 00:00 & limit = 100
#     # HTTP / 1.1
#     headers = {'api-key': api}
#
#     # 设备详情API
#     url_stream = streamHttp + did
#     # 从设备详情信息中取出设备号数据(title)
#     Title = requests.get(url_stream, headers=headers)
#     temp = str(Title.text)
#     Jtemp = json.loads(temp)
#     data = Jtemp['data']
#     keys = data['keys']
#     for index, values in enumerate(keys):
#         title = values.get('title', '')
#     # 设备历史数据API
#     url_point = pointHttp + did + "/datapoints"
#     Point = requests.get(url_point, headers=headers, params=payload)
#     # 从设备历史数据中取出数据流中数据信息
#     temp = str(Point.text)
#     Jtemp = json.loads(temp)
#     data = Jtemp['data']
#     datastreams = data['datastreams']
#     for index, values in enumerate(datastreams):
#         point = values.get('datapoints', '')
#     return [title, point]
#
#
# # ------------------------------数据导入excel------------------------------
# def writeExcel(pid, vae, did, point, tit, eid, sid):
#     # 创建excel表
#     ws = op.Workbook()
#     # 创建sheet表单
#     wb = ws.create_sheet(sid)
#     # 表头信息
#     # wb.cell(row=1, column=1, value='项目名称')
#     # wb.cell(row=1, column=2, value='设备名称')
#     # wb.cell(row=1, column=3, value='设备ID')
#     # wb.cell(row=1, column=4, value='变量名称')
#     wb.cell(row=1, column=1, value='时间')
#     wb.cell(row=1, column=2, value='最新数据')
#
#     # 计数器，代表行数
#     count = 1
#     # 循环数据信息，每次循环一个字典，计数+1
#     for index, values in enumerate(point):
#         count += 1
#         # time代表数据信息对应时间'at'，temp代表数据信息'value'
#         time = str(values.get('at', ''))
#         temp = str(values.get('value', ''))
#         # 随循环递增exlce表内容，row代表行，column代表列，value代表要添加的信息
#         # wb.cell(row=count, column=1, value='项目' + pid)
#         # wb.cell(row=count, column=2, value='设备' + tit)
#         # wb.cell(row=count, column=3, value=did)
#         # wb.cell(row=count, column=4, value=vae)
#         wb.cell(row=count, column=1, value=time)
#         wb.cell(row=count, column=2, value=temp)
#         # 保存表格
#         ws.save(eid)
#     ws.close()
#
#
# # ------------------------------数据导入折线图------------------------------
# def drawPicture(pid, vae, did, point, tit):
#     # 解决数据输出时列名不对齐的问题
#     pd.set_option('display.unicode.east_asian_width', True)
#     # list_x存储时间信息，list_y存储数据信息
#     list_x = []
#     list_y = []
#     plt.ion()
#     for index, values in enumerate(point / 100):  # 我修改过
#         x_time = str(values.get('at', ''))
#         y_temperature = float((values.get('value', '')))
#         # 每次循环所获数值，添加到对应列表中
#         list_x.append(x_time)
#         list_y.append(y_temperature)
#         # 清楚figure坐标轴
#         plt.clf()
#         # 防止中文乱码
#         plt.rcParams['font.sans-serif'] = ['SimHei']
#         # 防止负号不显示
#         plt.rcParams['axes.unicode_minus'] = False
#         # 传递x和y轴数据，后续参数为格式控制
#         plt.plot(list_x, list_y, color="r", marker="o", linestyle="-", alpha=0.5, mfc="c")
#         # 设置x和y轴名称
#         plt.xlabel("时间")
#         plt.ylabel("温度")
#         # x轴赋值
#         dfdate_x = ['%s 时' % i for i in list_x]
#         plt.xticks(list_x, dfdate_x, rotation=320)
#         # 设置网格线
#         plt.grid(color="g", linestyle=":", alpha=0.5)
#         # 设置图例
#         plt.legend(("项目:" + pid + ", 设备:" + did + "-" + tit + vae,))
#         # 设置标题
#         plt.title("温度传感器", fontdict={'fontsize': 15, 'fontweight': 20, 'va': 'center'}, loc="center")
#         # 延时
#         plt.pause(0.5)
#         plt.ioff()
#     plt.show()
#
#
# # ------------------------------窗口输出信息------------------------------
# def configprint(pid, vae, did, point, tit):
#     # 计数循环，窗口递增输出数据流信息
#     count = 1
#     print('项目名称' + '\t\t\t' + '设备名称' + '\t\t\t\t' + '设备ID' + '\t\t\t\t\t' + '变量名称'
#           + '\t\t\t' + '最新数据' + '\t\t\t\t' + '时间')
#     for index, values in enumerate(point):
#         count += 1
#         time = str(values.get('at', ''))
#         temperature = str(values.get('value', ''))
#         print(pid + '\t\t\t\t' + tit + '\t\t\t\t' + did + '\t\t\t\t' + vae + '\t\t\t\t' + temperature
#               + '\t\t\t\t' + time)
#
#
# # ------------------------------main()------------------------------
# if __name__ == "__main__":
#     # 调用configGet获取配置文件参数
#     configGet = getconfig()
#     projectId = configGet[0]  # 项目名称
#     variAble = configGet[1]  # 变量名称
#     deviceId = configGet[2]  # 设备ID
#     APIKey = configGet[3]  # API配置参数
#     startId_i = configGet[4]  # 数据流开始时间
#     excelId = configGet[5]  # excle名称及路径
#     sheetId = configGet[6]  # sheet名称
#     streamHttp = configGet[7]  # 对应url使用参数
#     pointHttp = configGet[8]  # 对应url使用参数
#
#     # startId_e = [2021-09-24T16:19:44]    # 数据流开始时间
#
#     # 调用configSet设置参数
#     configSet = setconfig(deviceId, APIKey, startId_i, streamHttp, pointHttp)
#
#     title = configSet[0]  # 设备名称
#     point = configSet[1]  # 数据流中数据信息
#     for index, values in enumerate(point):
#         time = str(values.get('at', ''))
#         temperature = float((values.get('value', '')))
#         if (time != ""):
#             # 数据对应时间不为空，即可执行窗口输出，写入excel，构画折线图
#             configprint(projectId, variAble, deviceId, point, title)
#             writeExcel(projectId, variAble, deviceId, point, title, excelId, sheetId)
#             drawPicture(projectId, variAble, deviceId, point, title)
#             break
#         else:
#             print("error:NO POINT!")
#         break

for i in range(30):
    aa = 1
    bb = 1+i
    dd = 'd'
    cc = str(aa)+str(bb)+dd
    print(cc)
