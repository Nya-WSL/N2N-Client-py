import os
import csv
import sys
import json
import shlex
import ctypes
import asyncio
import datetime
import requests
import subprocess
from urllib import request
from nicegui import ui, native, app

version = "2.0.0"
app.storage.general.indent = True
# env_cmd = r"setx NICEGUI_STORAGE_PATH %s /m"%"config"
# os.system(env_cmd)

def check_port():
    if portSetting.value == "" or int(portSetting.value) < 1 or int(portSetting.value) > 65525:
        print("Port is error! Will search for available IP!")
        port = native.find_open_port(65001, 65525)
        portSetting.set_value(port)
    else:
        port = portSetting.value
    return int(port)

def stop_command():
    process.kill()
    connButton.set_text("连接")
    connButton.on_click(run_command())

async def run_command() -> None:
    global process

    command = ""
    result.content = ""

    if ipInputSwitch.value:
        command = f"{n2n} -c {groupNameInput.value} -l {ServerSelect.value}"
    else:
        command = f"{n2n} -c {groupNameInput.value} -a {ipInput.value} -l {ServerSelect.value}"

    if connButton.text == "断开连接":
        stop_command()
    else:
        if groupNameInput.value == "" or ServerSelect.value == "null":
            if ipInputSwitch.value == False:
                if ipInput.value == "":
                    ui.notify("参数错误！请检查！", type="negative")
            else:
                ui.notify("参数错误！请检查！", type="negative")
        else:
            if ipInputSwitch.value == False:
                if ipInput.value == "":
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
    ServerDict = {"125.197.99.92:7777" : "NWC | 东京"}
    return ServerDict

def ShowIpInput():
    if ipInputSwitch.value:
        ipInput.set_enabled(False)
    else:
        ipInput.set_enabled(True)

n2n = ""
language = ""
osInfo = sys.platform

if osInfo == "win32": # 系统类型
    n2n = "edge.exe" # windows的n2n二进制文件
elif osInfo == "linux": # 系统类型
    n2n = "./edge" # linux的n2n二进制文件

with open("lang/global.json", "r", encoding="utf-8") as f:
    global_lang = json.load(f)

if os.path.exists(".nicegui/storage-general.json"):
    language = app.storage.general["language"] #读取语言文件的字典
else:
    language = "auto"

if language == "auto":
    # dll_h = ctypes.windll.kernel32
    SysLang = hex(ctypes.windll.kernel32.GetSystemDefaultUILanguage())
    if SysLang == "0x804":
        language = "zh_cn"
    elif SysLang == "0x409":
        language = "en_us"
    elif SysLang == "0x411":
        language = "ja_jp"
    else:
        if os.path.exists(".nicegui/storage-general.json"):
            language = app.storage.general["default_lang"]
        else:
            language = "en_us"
else:
    language = app.storage.general["language"]

lang = {
    "TabHomeName": "Home",
    "TabSettingsName": "Settings",
    "ipInputSwitch": "Auto Assign IP",
    "ServerSelect": "Select Server",
    "GroupNameInput": "Group Name",
    "ipInput": "LAN IP",
    "connButton": "connect",
    "GlobalSettings": "Global Settings",
    "ServerSettings": "Server Settings",
    "LocalSettings": "Local Settings",
    "LangSelect": "Language",
    "DefaultLanguageSelect": "Default Language",
    "ServerUrl": "Asset Server",
    "AutoUpdate": "Auto Update",
    "CheckServerList": "Get Server List",
    "CheckUpdateButton": "Check Update",
    "csvUrl": "CSV File Path",
    "VersionCheckUrl": "Version File Path",
    "ZipUrl": "Update File Path",
    "UpdateProgramUrl": "Update Program Path",
    "csvPath": "CSV File Name",
    "LocalListPath": "Local Server Path",
    "UpdateProgramName": "Update Program Name",
    "NativePort": "GUI Run Port"
}

if not os.path.exists(f"lang/{language}.json"): # 检查语言文件是否存在
    ui.notify(f"{language}.json is not exists!", type="error")
    print(f"{language}.json is not exists!")
else:
    with open(f"lang/{language}.json", encoding="utf-8") as l: # 读取语言文件
        LangText = l.read()
        lang = json.loads(LangText)

TabHomeName = lang["TabHomeName"]
TabSettingsName = lang["TabSettingsName"]
ipInputSwitchLang = lang["ipInputSwitch"]
ServerSelectLang = lang["ServerSelect"]
GroupNameInputLang = lang["GroupNameInput"]
ipInputLang = lang["ipInput"]
connButtonLang = lang["connButton"]
GlobalSettings = lang["GlobalSettings"]
ServerSettings = lang["ServerSettings"]
LocalSettings = lang["LocalSettings"]
LangSelect = lang["LangSelect"]
DefaultLanguageSelectLang = lang["DefaultLanguageSelect"]
ServerUrl = lang["ServerUrl"]
AutoUpdate = lang["AutoUpdate"]
CheckServerList = lang["CheckServerList"]
CheckUpdateButtonLang = lang["CheckUpdateButton"]
csvUrlLang = lang["csvUrl"]
VersionCheckUrl = lang["VersionCheckUrl"]
ZipUrlLang = lang["ZipUrl"]
UpdateProgramUrl = lang["UpdateProgramUrl"]
csvPathLang = lang["csvPath"]
LocalListPathLang = lang["LocalListPath"]
UpdateProgramName = lang["UpdateProgramName"]
NativePort = lang["NativePort"]


# ConServerUrl = config["server"] # 读取服务器配置
with ui.tabs().classes('w-full') as tabs:
    ui.tab('home', TabHomeName, icon='home')
    ui.tab('settings', TabSettingsName, icon='settings')
with ui.tab_panels(tabs, value='home').classes('w-full'):
    with ui.tab_panel('settings'):
        with ui.row():
            with ui.column():
                AutoUpdateSwitch = ui.switch(text=AutoUpdate, value=True).bind_value(app.storage.general, "auto_update")
                CheckServerListSwitch = ui.switch(text=CheckServerList, value=True).bind_value(app.storage.general, "check_server_list")
                checkUpdateButton = ui.button(text=CheckUpdateButtonLang)
            with ui.column():
                ui.badge(GlobalSettings, outline=True)
                LanguageSelect = ui.select(label=LangSelect, options=global_lang["lang"], value="auto").style("width: 140px").bind_value(app.storage.general, "language")
                DefaultLanguageSelect = ui.select(label=DefaultLanguageSelectLang, options=global_lang["default_lang"], value="en_us").style("width: 140px").bind_value(app.storage.general, "default_lang")
                serverUrl = ui.input(label=ServerUrl, value="https://qn.nya-wsl.cn/").style("width: 140px").bind_value(app.storage.general, "server")
                portSetting = ui.input(label=NativePort, value=lambda: int(check_port()), placeholder="1-65525").style("width: 140px").bind_value(app.storage.general, "native_port")

            with ui.column():
                ui.badge(ServerSettings, outline=True)
                csvUrl = ui.input(label=csvUrlLang, value="files/ServerList.csv").bind_value(app.storage.general, "csvUrl")
                updateCheckUrl = ui.input(label=VersionCheckUrl, value="files/n2n_config.html").bind_value(app.storage.general, "conUrl")
                zipUrl = ui.input(label=ZipUrlLang, value="files/n2n_update_win.zip").bind_value(app.storage.general, "zipUrl")
                updateUrl = ui.input(label=UpdateProgramUrl, value="files/update.exe").bind_value(app.storage.general, "updateUrl")

            with ui.column():
                ui.badge(LocalSettings, outline=True)
                csvPath = ui.input(label=csvPathLang, value="ServerList.csv").bind_value(app.storage.general, "csvPath")
                localListPath = ui.input(label=LocalListPathLang, value="local_list.csv").bind_value(app.storage.general, "local_list")
                updateFile = ui.input(label=UpdateProgramName, value="update.exe").bind_value(app.storage.general, "updateFile")

    with ui.tab_panel('home'):
        with ui.row().classes("w-full"):
            with ui.card(align_items="center").classes("w-full"):
                ipInputSwitch = ui.switch(text=ipInputSwitchLang, value=True, on_change=lambda: ShowIpInput())
                with ui.row():
                    ServerSelect = ui.select(label=ServerSelectLang, options=GetServer()).style("width: 120px").bind_value(app.storage.general, "N2N_Server")
                    groupNameInput = ui.input(label=GroupNameInputLang).bind_value(app.storage.general, "GroupName")
                    ipInput = ui.input(ipInputLang).style("width: 120px").bind_value(app.storage.general, "LAN_IP")
                    ipInput.set_enabled(False)
                connButton = ui.button(connButtonLang, on_click=lambda: run_command())
        with ui.card().classes('w-full'):
            with ui.scroll_area().classes('w-full') as area:
                result = ui.markdown()

ui.run(
port=int(check_port()),
title=f"N2N Client | Nya-WSL v{version}",
native=True,
reload=False,
window_size=[740, 700]
)