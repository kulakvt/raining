#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 18:45:29 2018

This is a simple weather app for network testing. While running, the script
uses two APIs to check and see if it is raining at a user's location, and then
the app returns the results using HTML over HTTP. You will need to provide an
API key and set the default location if the user cannot be located using
a public IP address.

@author: Andrew Kulak
"""

# Libraries
import socket
import requests
import json
from netaddr import IPSet
import sys

# Takes a command line argument for port number to run on
if (len(sys.argv) != 2 or not sys.argv[1].isdigit()):
    print 'Usage: python raining.py <port>'
    exit()

# Setting variables and network connections
p = int(sys.argv[1])
l = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', p))
s.listen(1)
print '[+] raining.py service listening on port ' + str(p)

# Main loop
try:
    while 1:
        (c, a) = s.accept()
        l.append(c)
        info = '\n[+] %d: Connection from %s' % (len(l), a)
        print info
        if c.recv(1024).split('\n')[0].strip() == 'GET / HTTP/1.1':
            print '[+] Responding to HTTP GET request...'
            try:
                ip_addr = a[0]
                location = requests.get('https://ipinfo.io/' + ip_addr)
                print '[+] IP address detected as: ' + ip_addr
                # Compare IP address to private network ranges
                if ip_addr not in IPSet(['10.0.0.0/8', '172.16.0.0/12', '192.0.2.0/24', '192.168.0.0/16', '239.192.0.0/14', '127.0.0.0/8']):
                    location_json = json.loads(location.content)
                    location_info = location_json['loc']
                    location_lat = location_info.split(',')[0]
                    location_lon = location_info.split(',')[1]
                    location_city = location_json['city']
                    print '[+] User located in ' + location_city + ' at lat ' + location_lat + ' and lon ' + location_lon
                else:
                    print '[-] Private address detected...'
                    raise Exception
            except Exception as e:
                print '[-] Could not locate user, using default location'
                location_lat = '' # Set to a default latitude of your choice
                location_lon = '' # Set to a default longitude of your choice
                location_city = '' # Set to a default city of your choide
                pass
            try:
                conds = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + location_lat + '&lon=' + location_lon + '&APPID=YOUR_APP_ID')
                conds_content = conds.content
                conds_json = json.loads(conds_content)
                conds_current = conds_json['weather'][0]
                print '[+] Currently ' + str(conds_current['description']) + ' at user location'
                if conds_current['id'] <= 531:
                    print '[+] Reporting as rain in ' +location_city
                    HTTP_payload = '<!DOCTYPE html><html lang="en"><head><title>Is it raining?</title></head><body><p>It is raining in ' + location_city + '...</p></body></html>'
                    HTTP_header = 'HTTP/1.1 200 OK\n'
                    HTTP_server= 'Server: Python (custom)\n'
                    HTTP_length = 'Content-Length: ' + str(len(HTTP_payload.encode('utf-8'))) + '\n'
                    HTTP_connection = 'Connection: Closed\n'
                    HTTP_content = 'Content-Type: text/html\n\n'
                    c.send(HTTP_header + HTTP_server + HTTP_length + HTTP_connection + HTTP_content + HTTP_payload)
                    c.close()
                else:
                    print '[+] Reporting as not rain in ' + location_city
                    HTTP_payload = '<!DOCTYPE html><html lang="en"><head><title>Is it raining?</title></head><body><p>It is not raining in ' + location_city + '...</p></body></html>'
                    HTTP_header = 'HTTP/1.1 200 OK\n'
                    HTTP_server= 'Server: Python (custom)\n'
                    HTTP_length = 'Content-Length: ' + str(len(HTTP_payload.encode('utf-8'))) + '\n'
                    HTTP_connection = 'Connection: Closed\n'
                    HTTP_content = 'Content-Type: text/html\n\n'
                    c.send(HTTP_header + HTTP_server + HTTP_length + HTTP_connection + HTTP_content + HTTP_payload)
                    c.close()
            except Exception as e:
                try:
                    print '[-] Could not determine conditions'
                    print '[-]' + str(e)
                    HTTP_payload = '<!DOCTYPE html><html lang="en"><head><title>Is it raining?</title></head><body><p>Please try again</p></body></html>'
                    HTTP_header = 'HTTP/1.1 200 OK\n'
                    HTTP_server= 'Server: Python (custom)\n'
                    HTTP_length = 'Content-Length: ' + str(len(HTTP_payload.encode('utf-8'))) + '\n'
                    HTTP_connection = 'Connection: Closed\n'
                    HTTP_content = 'Content-Type: text/html\n\n'
                    c.send(HTTP_header + HTTP_server + HTTP_length + HTTP_connection + HTTP_content + HTTP_payload)
                    c.close()
                except Exception as e:
                    print '[-] Could not send response'
                    print '[-]' + str(e)
                    pass
                pass
        else:
            try:
                print '[-] Unsupported request...'
                HTTP_payload = ''
                HTTP_header = 'HTTP/1.1 404 Not Found\n'
                HTTP_server= 'Server: Python (custom)\n'
                HTTP_length = 'Content-Length: ' + str(len(HTTP_payload.encode('utf-8'))) + '\n'
                HTTP_connection = 'Connection: Closed\n'
                HTTP_content = 'Content-Type: text/html\n\n'
                c.send(HTTP_header + HTTP_server + HTTP_length + HTTP_connection + HTTP_content + HTTP_payload)
                c.close()
            except Exception as e:
                print '[-] Could not send response'
                print '[-]' + str(e)
                pass

# Will run forever, this terminates gracefully on keyboard interrupt
except KeyboardInterrupt:
    print '[+] Exiting...'
    try:
            sys.exit(0)
            c.close()
            s.close()
    except:
            pass
