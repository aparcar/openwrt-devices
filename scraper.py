from bs4 import BeautifulSoup
import re
import urllib3
import urllib.request
import os
import yaml
import json

dev = False

base_url = "https://openwrt.org"

deviceinfo = """\
---
title: Info about {device}
folder: info
layout: deviceinfo
permalink: /devices/{device}/
device: {device}
---
{{% include templates/device_info.md %}}
"""

int_values = [
    "cpu_cores",
    "cpu_mhz",
    "ethernet_100m_ports",
    "ethernet_gbit_ports",
    "flash_mb",
    "ram_mb",
]


def download_images():
    for device_raw in os.listdir("raw/"):
        device = device_raw.replace(".", "-")
        with open("raw/" + device_raw, "r") as device_file:
            soup = BeautifulSoup(device_file.read(), "html.parser")
            techdata = soup.find("div", "techdata")
            if not techdata:
                continue

            dd = techdata.find_all("dd", "picture")

            if not dd:
                print("no picture defined", device)
                continue

            href = dd[0].a["href"]
            if href != "/_media/media/example/genericrouter1.png?cache=":
                url = base_url + href
                suffix = url.split("?")[0].split(".")[-1]
                image = device + "." + suffix

                try:
                    with urllib.request.urlopen(url) as response, open(
                        "images/devices/" + image, "wb"
                    ) as out_file:
                        data = response.read()  # a `bytes` object
                        out_file.write(data)

                    yaml_path = "_data/devices/" + device + ".yml"
                    if os.path.exists(yaml_path):
                        with open(yaml_path, "r") as yaml_file:
                            device_info = yaml.full_load(yaml_file.read())
                        device_info["image"] = image
                        with open(yaml_path, "w") as yaml_file:
                            yaml.dump(device_info, yaml_file, default_flow_style=False)
                        print("stored and added", device)
                    else:
                        print("just stored", device)
                except:
                    print("404ed", device)
            else:
                print("generic", device)


def parse_raw_devices():
    i = 0
    for device_raw in os.listdir("raw/"):
        device = device_raw.replace(".", "-")
        if dev == True and i > 100:
            break
        i += 1

        yaml_path = "_data/devices/" + device + ".yml"
        if os.path.exists(yaml_path):
            with open(yaml_path, "r") as yaml_file:
                device_info = yaml.full_load(yaml_file.read())
            device_info["vendor"] = device_info["brand"]
            if "brand" in device_info: device_info.pop("brand", None)

        else:
            with open("raw/" + device_raw, "r") as device_file:
                soup = BeautifulSoup(device_file.read(), "html.parser")
                techdata = soup.find("div", "techdata")
                if not techdata:
                    continue
                device_info = {}
                device_info["device_id"] = device
                device_info["malformed"] = {}

                for dd in techdata.find_all("dd"):
                    if not dd.string:
                        continue
                    value = str(dd.string)
                    if (
                        not value
                        or value.lower() == "none"
                        or value == "-"
                        or value == ""
                        or value == "¿"
                    ):
                        continue
                    if value == "Yes":
                        value = True
                    if value == "No":
                        value = False
                    for int_value in int_values:
                        if int_value in device_info:
                            try:
                                device_info[int_value] = int(device_info[int_value])
                            except:
                                device_info["malformed"][int_value] = device_info[
                                    int_value
                                ]
                    device_info[dd["class"][0]] = value

        with open(yaml_path, "w") as yaml_file:
            yaml.dump(device_info, yaml_file, default_flow_style=False)

        with open("pages/info/" + device + ".md", "w") as outfile:
            outfile.write(deviceinfo.format(**{"device": device}))

        #            with open("json/" + device + ".json", "w") as outfile:
        #                json.dump(device_info, outfile, indent=4)

        print("stored", device)


def download_raw_devices():
    content = open("toh_fwdownload").read()
    soup = BeautifulSoup(content, "html.parser")
    http = urllib3.PoolManager()
    for tr in soup.find_all("tr"):
        for td in tr.find_all("td", "device_techdata"):
            device_url = base_url + td.a["href"]
            device_path = "raw/" + device_url.split("/")[-1]
            req = http.request("GET", device_url)
            with open(device_path, "w") as device_file:
                device_file.write(req.data.decode("utf-8"))

            print("stored", device_path, "from", device_url)


# download_raw_devices()
parse_raw_devices()
#download_images()
