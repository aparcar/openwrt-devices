from bs4 import BeautifulSoup
import urllib3
import os
import yaml
import json

base_url = "https://openwrt.org"

deviceinfo = """\
---
title: Info about {device}
folder: info
layout: deviceinfo
permalink: /devices/{device}/
device: {device}
---
"""

def parse_raw_devices():
    for device in os.listdir("raw/"):
        with open("raw/" + device, "r") as device_file:
            soup = BeautifulSoup(device_file.read(), "html.parser")
            techdata = soup.find("div", "techdata")
            device_info = {}
            device_info["device_id"] = device

            for dd in techdata.find_all("dd"):
                value = str(dd.string) or ""
                if (
                    value.lower() == "none"
                    or value == "-"
                    or value == ""
                    or value == "¿"
                ):
                    continue
                if value == "Yes":
                    value = True
                if value == "No":
                    value = False
                device_info[dd["class"][0]] = value


            with open("_data/devices/" + device + ".yml", "w") as outfile:
                yaml.dump(device_info, outfile, default_flow_style=False)

            with open("pages/info/" + device + ".md", "w") as outfile:
                outfile.write(deviceinfo.format(**{"device":device}))

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
