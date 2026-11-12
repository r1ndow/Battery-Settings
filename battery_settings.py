import psutil
import time
import win32api
import win32con
import subprocess

def set_refresh_rate(hz):
    settings = win32api.EnumDisplaySettings(
        None, 
        win32con.ENUM_CURRENT_SETTINGS
    )

    settings.DisplayFrequency = hz

    result = win32api.ChangeDisplaySettings(settings, win32con.CDS_TEST)

    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        result = win32api.ChangeDisplaySettings(settings, 0)
        print("Result:", result)
        return result == win32con.DISP_CHANGE_SUCCESSFUL
    else:
        print("Check rate is failed, Code:", result)
        return False

subprocess.run(
    [
        "powercfg",
        "/setdcvalueindex",
        "SCHEME_CURRENT",
        "SUB_ENERGYSAVER",
        "ESBATTTHRESHOLD",
        "100"
    ],
    check=True
)

subprocess.run(
    [   "powercfg",
        "/setactive",
        "SCHEME_CURRENT"
    ],
    check=True
)

previous_state = None

while True:
    battery = psutil.sensors_battery()

    if battery.power_plugged != previous_state:
        if battery.power_plugged:
            print("Power plugged")
            success = set_refresh_rate(165)
        else:
            print("Power not plugged")
            success = set_refresh_rate(60)

        if success:
            previous_state = battery.power_plugged

    time.sleep(0.2)