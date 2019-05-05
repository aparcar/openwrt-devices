import re
import os
import yaml

with open("dts_files", "r") as dts_file:
    dts_paths = dts_file.readlines()
    for dts in dts_paths:
        content = ""

        with open(dts.replace("\n", ""), "r") as dts_file:
            content = dts_file.read()

        device = re.findall('compatible = "(.*?)",', content, re.MULTILINE)
        if not device:
            continue

        device = device[0].replace(",", "_")

        if os.path.exists("_data/devices/" + device + ".yml"):
            print("bingo", device)

            layout = (re.findall("""\
.*?label = "(.*?)";
.*?reg = <(.*?)>;""", content, re.MULTILINE))

            if layout:
                with open("_data/devices/" + device + ".yml", "r") as device_file:
                    device_info = yaml.full_load(device_file)

                device_info["flash_layout"] = {}

                for label, reg in layout:
                    device_info["flash_layout"][label] = reg.replace(" ", "-")

                with open("_data/devices/" + device + ".yml", "w") as device_file:
                    yaml.dump(device_info, device_file)
