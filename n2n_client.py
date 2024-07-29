import os
import csv
import sys
import shlex
import ctypes
import asyncio
import platform
import datetime
import requests
import subprocess
from urllib import request
from nicegui import ui, native, app

version = "2.0.0" # 版本号

def stop_command():
    process.kill()
    connButton.set_text("连接")
    connButton.on_click(run_command(cmd))

async def run_command(command: str) -> None:
    global process
    result.content = ""
    if connButton.text == "断开连接":
        stop_command()
    else:
        if ipInput.value == "" or groupNameInput.value == "" or ServerSelect.value == "null":
            ui.notify("参数错误！请检查！", type="negative")
        else:
            command = command.replace('python3', sys.executable)  # NOTE replace with machine-independent Python path (#1240)
            process = await asyncio.create_subprocess_exec(
                *shlex.split(command, posix='win' not in sys.platform.lower()),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            # NOTE we need to read the output in chunks, otherwise the process will block
            output = []
            while True:
                new = await process.stdout.readline()
                output.append(f"{new}")
                output_str = str(output).replace("\\n", "\n").replace("[\"b\'", "").replace("\r\n", "\n").replace("\\r\\", "").replace("\"]", "").replace("""\
    '", "b'""", "").replace("\''\, \"b'", "")
                if not new:
                    break
                result.content = f'```\n{output_str}\n+{new}\n```'
                area.scroll_to(percent=1.0)
                connButton.set_text("断开连接")

def GetServer():
    ServerDict = {"127.0.0.1:7776" : "NWC | 上海", "125.197.99.92:7777" : "NWC | 东京", "127.0.0.1:7777" : "NWC | 首尔"}
    return ServerDict

def ShowIpInput():
    if ipInputSwitch.value:
        ipInput.set_visibility(False)
    else:
        ipInput.set_visibility(True)

app.storage.general.indent = True
# 检测系统类型
osInfo = sys.platform
if osInfo == "win32": # 系统类型
    n2nEXE = "edge.exe" # windows的n2n二进制文件

elif osInfo == "linux": # 系统类型
    n2nEXE = "./edge" # linux的n2n二进制文件

# CheckServerList = config["check_server_list"]
# AutoUpdate = config["auto_update"]

# language = config["language"] #读取语言文件的字典
# if language == "auto":
#     dll_h = ctypes.windll.kernel32
#     SysLang = hex(dll_h.GetSystemDefaultUILanguage())
#     if SysLang == "0x804":
#         language = "zh_cn"
#     elif SysLang == "0x409":
#         language = "en_us"
#     else:
#         language = config["default_lang"]
# else:
#     language = config["language"]
# if not os.path.exists(f"lang/{language}.json"):
#     ui.notify(f"{language}.json is not exists!", type="error")

# with open(f"lang/{language}.json", encoding="utf-8") as l: # 读取语言文件
#     LangText = l.read()
#     lang = json.loads(LangText)

# StartText = lang["StartText"]
# AssignTextAuto = lang["AssignTextAuto"]
# AssignTextManual = lang["AssignTextManual"]
# CheckVersion = lang["CheckVersion"]
# LocalVersion = lang["LocalVersion"]
# ServerVersion = lang["ServerVersion"]
# UpdateText = lang["UpdateText"]
# LatestVersion = lang["LatestVersion"]
# HistoryChoose = lang["HistoryChoose"]
# HistoryChoose1 = lang["HistoryChoose1"]
# HistoryChoose2 = lang["HistoryChoose2"]
# HistoryChoose3 = lang["HistoryChoose3"]
# SecondCheck = lang["SecondCheck"]
# SearchServer = lang["SearchServer"]
# InputGroupName = lang["InputGroupName"]
# ServerNumber = lang["ServerNumber"]
# ServerName = lang["ServerName"]
# ServerIP = lang["ServerIP"]
# AssignText = lang["AssignText"]
# ConfirmText = lang["ConfirmText"]
# AutoUpdateText = lang["AutoUpdateText"]
# AutoUpdateConfigError = lang["AutoUpdateConfigError"]
# CheckServerListError = lang["CheckServerListError"]

# ConServerUrl = config["server"] # 读取服务器配置
with ui.tabs().classes('w-full') as tabs:
    ui.tab('home', '首页', icon='home')
    ui.tab('settings', '设置', icon='settings')
with ui.tab_panels(tabs, value='home').classes('w-full'):
    with ui.tab_panel('settings'):
        with ui.row():
            with ui.column():
                with ui.row():
                    LanguageSelect = ui.select(label="Language", options={"auto":"Auto", "zh_CN":"简体中文", "en_US":"English"}, value="auto").style("width: 100px").bind_value(app.storage.general, "language")
                    DefaultLanguageSelect = ui.select(label="Default Language", options={"zh_CN":"简体中文", "en_US":"English"}, value="en_US").style("width: 140px").bind_value(app.storage.general, "default_lang")
                CheckServerListSwitch = ui.switch(text="联网获取节点", value=True).bind_value(app.storage.general, "check_server_list")
                AutoUpdateSwitch = ui.switch(text="自动更新", value=True).bind_value(app.storage.general, "auto_update")
                serverUrl = ui.input(label="Server URL").bind_value(app.storage.general, "server")
                checkUpdateButton = ui.button(text="Check Update")
            with ui.column():
                csvUrl = ui.input(label="CSV URL", value="files/ServerList.csv").bind_value(app.storage.general, "csvUrl")
                updateCheckUrl = ui.input(label="Update Check URL", value="files/n2n_config.html").bind_value(app.storage.general, "conUrl")
                zipUrl = ui.input(label="Zip URL", value="files/n2n_update_win.zip").bind_value(app.storage.general, "zipUrl")
                updateUrl = ui.input(label="Update URL", value="files/update.exe").bind_value(app.storage.general, "updateUrl")
                historyUrl = ui.input(label="History URL", value="files/history.json").bind_value(app.storage.general, "historyUrl")
            with ui.column():
                csvPath = ui.input(label="CSV File Path", value="./ServerList.csv").bind_value(app.storage.general, "csvPath")
                csvFile = ui.input(label="CSV File Name", value="ServerList.csv").bind_value(app.storage.general, "csvFile")
                localListPath = ui.input(label="Local List Path", value="./local_list.csv").bind_value(app.storage.general, "local_list")
                updateFile = ui.input(label="Update Program Name", value="update.exe").bind_value(app.storage.general, "updateFile")
                historyFile = ui.input(label="History File Name", value="history.txt").bind_value(app.storage.general, "historyFile")
    with ui.tab_panel('home'):
        with ui.row().classes('w-full'):
            with ui.card().classes('w-full'):
                ipInputSwitch = ui.switch("自动分配IP", value=True, on_change=ShowIpInput)
                with ui.row():
                    ServerSelect = ui.select(label="选择服务器", options=GetServer()).style("width: 120px").bind_value(app.storage.general, "N2N_Server")
                    groupNameInput = ui.input(label="组名称").bind_value(app.storage.general, "GroupName")
                    ipInput = ui.input("IP地址").style("width: 120px").bind_value(app.storage.general, "LAN_IP")
                    ipInput.set_visibility(False)
                cmd = ""
                if ipInputSwitch.value:
                    cmd = f"edge.exe -c {groupNameInput.value} -l {ServerSelect.value}"
                else:
                    cmd = f"edge.exe -c {groupNameInput.value} -a {ipInput.value} -l {ServerSelect.value}"
                connButton = ui.button("连接", on_click=lambda: run_command(cmd)).classes("w-full")
            with ui.card().classes('w-full'):
                with ui.scroll_area().classes('w-full') as area:
                    result = ui.markdown()

port_label = ui.label(native.find_open_port()).bind_text_to(app.storage.general, "native_port")
port_label.set_visibility(False)
ui.run(host="0.0.0.0", port=int(port_label.text), title=f"N2N Client | Nya-WSL v{version}", native=True, reload=False, window_size=[705, 700])