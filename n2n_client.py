import os
import sys
import json
import yaml
import shlex
import ctypes
import asyncio
import aiohttp
import zipfile
import requests
from nicegui import ui, native, app

version = "2.0.4"
app.storage.general.indent = True
app.storage.general['update_server'] = "https://qn.nya-wsl.cn/"
app.storage.general['updateCheckUrl'] = "n2n/n2n_config.html"
app.storage.general['zipUrl'] = "n2n/n2n_update_win.zip"

def check_permission():
    admin_permission = False
    if not ctypes.windll.shell32.IsUserAnAdmin(): # 判断是否使用管理员权限执行
        with ui.dialog() as admin_dialog, ui.card(align_items="center"):
            ui.label(NotAdmin).classes("text-red")
            with ui.row():
                ui.button('ok', on_click=lambda: admin_dialog.close())
                ui.button('quit', on_click=lambda: app.shutdown())
        if not global_lang["dev_mode"]:
            admin_dialog.open()
        else:
            admin_permission = True
    else:
        admin_permission = True
    return admin_permission

def check_update():
    if os.path.exists("update.bat"):
        os.remove("update.bat")

    async def download(url, save_path):
        async def close_session():
            await session.close()
            cancelButton.on_click(dialog.close)
        updateButton.set_enabled(False)
        percent_dialog.set_text(DownloadStart)
        if not os.path.exists("cache"):
            os.mkdir("cache")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                cancelButton.on_click(lambda: close_session())
                with open(save_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        f.write(chunk)
                        percent_dialog.set_text(DownloadProgress + "%.2f%%" % (f.tell() / response.content_length * 100))
                        if not chunk:
                            break
        # percent_dialog.set_text(DownloadProgress + "100%")
        # updateButton.delete()
        # cancelButton.delete()
        percent_dialog.set_text(DownloadFinish)
        Unzip = zipfile.ZipFile("cache\\n2n_update_win.zip", mode='r')
        for names in Unzip.namelist():
            Unzip.extract(names, os.getcwd())
        Unzip.close()
        with open("update.bat", "w") as f:
            f.write(f"""
cd /d {os.getcwd()}
taskkill /f /im N2N-Client-NG.exe
timeout /t 3 /nobreak
move /y update\\* ./
rmdir /s /q update
rmdir /s /q cache
N2N-Client-NG.exe
""")
        os.system("update.bat")
        app.shutdown()

    response = requests.get(app.storage.general['update_server'] + app.storage.general['updateCheckUrl'])

    if response.text.replace("\n", "") != version:
        with ui.dialog() as dialog, ui.card():
            percent_dialog = ui.label(UpdateLabelLang)
            with ui.row(align_items="center"):
                updateButton = ui.button('Update', on_click=lambda: download(app.storage.general['update_server'] + app.storage.general['zipUrl'], "cache\\n2n_update_win.zip"))
                cancelButton = ui.button('Cancel', on_click=dialog.close)
        dialog.open()
    else:
        ui.notify(UpdateNotNeed, type="info")

def check_port():
    if not os.path.exists(".nicegui/storage-general.json"):
        portSetting.set_value("")
    if portSetting.value == "" or int(portSetting.value) < 1 or int(portSetting.value) > 65525:
        print("Port is error! Will search for available port!")
        port = native.find_open_port(65001, 65525)
        portSetting.set_value(port)
    else:
        port = portSetting.value
    return int(port)

def stop_command():
    process.kill()
    connButton.set_text(connButtonLang)
    connButton.on_click(run_command())

async def run_command() -> None:
    global process

    command = ""
    result.content = ""

    if not check_permission():
        return

    if ipInputSwitch.value:
        command = f"{n2n} -c {groupNameInput.value} -l {ServerSelect.value}"
    else:
        command = f"{n2n} -c {groupNameInput.value} -a {ipInput.value} -l {ServerSelect.value}"

    if connButton.text == DisconnButton:
        stop_command()
    else:
        if groupNameInput.value == "" or ServerSelect.value == "null":
            if ipInputSwitch.value == False:
                if ipInput.value == "":
                    ui.notify(ParameterError, type="negative")
            else:
                ui.notify(ParameterError, type="negative")
        else:
            if ipInputSwitch.value == False:
                if ipInput.value == "":
                    ui.notify(ParameterError, type="negative")
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
                        connButton.set_text(DisconnButton)
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
                    connButton.set_text(DisconnButton)

def GetLocalServer():
    if not CheckServerListSwitch.value:
        try:
            if not localListSelect.value in localListSelect.options:
                ui.notify(LocalServerGetError, type="negative")
            elif localListSelect.value == "json":
                with open("local_list.json", "r", encoding="utf-8") as f:
                    ServerSelect.set_options(options=json.load(f))
            elif localListSelect.value == "yml":
                with open("local_list.yml", "r", encoding="utf-8") as f:
                    ServerSelect.set_options(options=yaml.load(f, Loader=yaml.FullLoader))
        except:
            ui.notify(LocalServerGetError, type="negative")
            ServerSelect.set_options([f"{LocalServerGetError}"])
    else:
        GetServer(True)

def GetServer(status = False):
    try:
        response = requests.get(serverUrl.value + ListUrl.value)
        if not status:
            return response.json()
        else:
            ServerSelect.set_options(options=response.json())
    except:
        ui.notify(ServerGetError, type="negative")
        ServerSelect.set_options([f"{ServerGetError}"])

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
    "disconnButton": "Disconnect",
    "GlobalSettings": "Global Settings",
    "ServerSettings": "Server Settings",
    "LocalSettings": "Local Settings",
    "LangSelect": "Language",
    "DefaultLanguageSelect": "Default Language",
    "ServerUrl": "Asset Server",
    "AutoUpdate": "Auto Update",
    "CheckServerList": "Get Server List",
    "CheckUpdateButton": "Check Update",
    "LocalListFile": "Local server list file type",
    "LocalListPath": "Local Server Path",
    "NativePort": "GUI Run Port",
    "ParameterError": "Parameter error, please check!",
    "LocalServerGetError": "Get local server list is error, please check!",
    "ServerGetError": "Get server list is error, please check!",
    "UpdateLabel": "The new version is available, do you want to update it?",
    "CheckUpdateError": "Check update failed!",
    "UpdateNotNeed": "The current version is already the latest version!",
    "UpdateError": "Update failed!",
    "DownloadStart": "Download update started！",
    "DownloadError": "Download update error！",
    "DownloadProgress": "Download progress: ",
    "DownloadFinish": "Download update finished! The update will be installed!",
    "NotAdmin": "Please run as administrator!"
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
DisconnButton = lang["disconnButton"]
GlobalSettings = lang["GlobalSettings"]
ServerSettings = lang["ServerSettings"]
LocalSettings = lang["LocalSettings"]
LangSelect = lang["LangSelect"]
DefaultLanguageSelectLang = lang["DefaultLanguageSelect"]
ServerUrl = lang["ServerUrl"]
AutoUpdate = lang["AutoUpdate"]
CheckServerList = lang["CheckServerList"]
CheckUpdateButtonLang = lang["CheckUpdateButton"]
ListPath = lang["ListPath"]
LocalListFile = lang["LocalListFile"]
NativePort = lang["NativePort"]
ParameterError = lang["ParameterError"]
LocalServerGetError = lang["LocalServerGetError"]
ServerGetError = lang["ServerGetError"]
UpdateLabelLang = lang["UpdateLabel"]
CheckUpdateError = lang["CheckUpdateError"]
UpdateError = lang["UpdateError"]
DownloadStart = lang["DownloadStart"]
DownloadError = lang["DownloadError"]
DownloadProgress = lang["DownloadProgress"]
DownloadFinish = lang["DownloadFinish"]
UpdateNotNeed = lang["UpdateNotNeed"]
NotAdmin = lang["NotAdmin"]

check_permission()

with ui.tabs().classes('w-full') as tabs:
    ui.tab('home', TabHomeName, icon='home')
    ui.tab('settings', TabSettingsName, icon='settings')
with ui.tab_panels(tabs, value='home').classes('w-full'):
    with ui.tab_panel('settings'):
        with ui.row():
            with ui.column(align_items="center"):
                AutoUpdateSwitch = ui.switch(text=AutoUpdate, value=True).bind_value(app.storage.general, "auto_update")
                CheckServerListSwitch = ui.switch(text=CheckServerList, value=True, on_change=lambda: GetLocalServer()).bind_value(app.storage.general, "check_server_list")
                checkUpdateButton = ui.button(text=CheckUpdateButtonLang, on_click=lambda: check_update())
            with ui.column():
                ui.badge(GlobalSettings, outline=True)
                LanguageSelect = ui.select(label=LangSelect, options=global_lang["lang"], value="auto").style("width: 140px").bind_value(app.storage.general, "language")
                DefaultLanguageSelect = ui.select(label=DefaultLanguageSelectLang, options=global_lang["default_lang"], value="en_us").style("width: 140px").bind_value(app.storage.general, "default_lang")
                portSetting = ui.input(label=NativePort, value=lambda: int(check_port()), placeholder="1-65525").style("width: 140px").bind_value(app.storage.general, "native_port")
            with ui.column():
                ui.badge(ServerSettings, outline=True)
                serverUrl = ui.input(label=ServerUrl, value="https://nya-wsl.com/").style("width: 140px").bind_value(app.storage.general, "server")
                ListUrl = ui.input(label=ListPath, value="files/ServerList.json").bind_value(app.storage.general, "listUrl")

            with ui.column():
                ui.badge(LocalSettings, outline=True)
                # csvPath = ui.input(label=csvPathLang, value="ServerList.csv").bind_value(app.storage.general, "csvPath")
                localListSelect = ui.select(label=LocalListFile, options=["json", "yml"]).style("width: 160px").bind_value(app.storage.general, "localListSelect")

    with ui.tab_panel('home'):
        with ui.row().classes("w-full"):
            with ui.card(align_items="center").classes("w-full"):
                ipInputSwitch = ui.switch(text=ipInputSwitchLang, value=True, on_change=lambda: ShowIpInput())
                with ui.row():
                    ServerSelect = ui.select(label=ServerSelectLang, options=GetServer()).style("width: 200px").bind_value(app.storage.general, "N2N_Server")
                    groupNameInput = ui.input(label=GroupNameInputLang).bind_value(app.storage.general, "GroupName")
                    ipInput = ui.input(ipInputLang).style("width: 120px").bind_value(app.storage.general, "LAN_IP")
                    ipInput.set_enabled(False)
                connButton = ui.button(connButtonLang, on_click=lambda: run_command())
        with ui.card().classes('w-full'):
            with ui.scroll_area().classes('w-full') as area:
                result = ui.markdown()

if AutoUpdateSwitch.value:
    check_update()
ui.run(
port=int(check_port()),
title=f"N2N Client | Nya-WSL | v{version}",
native=True,
reload=False,
window_size=[740, 700]
)