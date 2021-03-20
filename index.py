#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd

from env import *

def sanitizeMac(mac):
    return mac.replace('-', '').replace(':', '')

# Vianet RaiseCom Router
def loginMain():
    url = "http://192.168.1.1/boaform/admin/formLogin"
    payload = f"username={mainUsername}&psd={mainPassword}&loginSelinit=1"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    return False


def getTableFromMainRouter(retries=0):
    try:
        url = "http://192.168.1.1/status_wlan_info_11n.asp"
        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'Cookie': cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.findAll('table', attrs={'class': 'flat'})[2]
        return pd.read_html(table.prettify())[0]
    except:
        if(retries <= 2):
            print(retries)
            retries += 1
            loginMain()
            return getTableFromMainRouter(retries)

# Tradelink router
def loginSecondary():
    url = "http://192.168.100.1/login.cgi"
    payload = f"username={secondaryUsername}&password={secondaryPassword}&submit.htm%3Flogin.htm=Send"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    return False

def getTableFromSecondaryRouter(retries=0):
    try:
        url = "http://192.168.100.1/dhcptbl.htm"
        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'Cookie': cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find(id='IdWlanClientTbl').find(id='body_header').findAll(
            'table', attrs={'class': 'formlisting'})[0]
        return pd.read_html(table.prettify())[0]
    except:
        if(retries <= 2):
            print(retries)
            retries += 1
            loginSecondary()
            return getTableFromMainRouter(retries)


macAddresses = {}
for key in macDeviceDict:
    macAddresses[sanitizeMac(key)] = macDeviceDict[key]

tableMain = getTableFromMainRouter()
if not (tableMain is None or tableMain.empty):
    macListMain = [['Mac', 'Device Name']]
    for index, row in tableMain[0].iteritems():
        if row != 'MAC':
            cleanMac = sanitizeMac(row)
            deviceName = macAddresses[cleanMac] if cleanMac in macAddresses else 'Unknown Device'
            macListMain.append([row, deviceName])
    mainList = pd.DataFrame(macListMain)

    print('Connected to main router')
    print(mainList)


tableSecondary = getTableFromSecondaryRouter()
if not (tableSecondary is None or tableSecondary.empty):
    macListSecondary = [['Mac', 'Device Name']]
    for index, row in tableSecondary[2].iteritems():
        if row != 'MAC Address':
            cleanMac = sanitizeMac(row)
            deviceName = macAddresses[cleanMac] if cleanMac in macAddresses else 'Unknown Device'
            macListSecondary.append([row, deviceName])
    scondaryList = pd.DataFrame(macListSecondary)

    print('\n')
    print('Connected to secondary router')
    print(scondaryList)
