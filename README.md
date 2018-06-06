# raining.py

raining.py is a simple Python script I wrote in Python 2.7.14. It runs as a service that responds to HTTP GET requests by locating the user based on IP and then using an open weather API to determine whether it is raining at the user's location or not. It then responds with a simple HTTP message that lets the user know if it is raining.

I wrote raining.py because:

1. I wanted to work with low-level networking interfaces

2. I wanted to learn more about the nuts and bolts of HTTP

3. I needed to test some basic networking functions on a lab network

## Dependencies

raining.py uses the netaddr library for comparing IP addresses.

## Requirements

You will need a working internet connection. You will also need an API key for the Open Weather API, which is free for limited access. The script assumes a user from a public IP address, and it will return a default location to localhost or private network addresses.

## Launching the Service

$ python raining.py <port>

Be sure to specify a port that is not already in use, or the script will return an error. Terminate by KeyboardInterrupt to close the port and ensure a graceful exit. The service will run indefinitely. It will log requests and processing information to stdout. The script ignores browser requests for favicon.ico.

## Use Cases

Use raining.py to test internet connectivity. It can also be used to test security policies. Because the messages are unencrypted, it is easy to identify and inspect raining.py traffic in a packet capture. 

## Warnings

This script is not intended to be robust or secure. Nothing is encrypted, so do not use it to send anything important. It will not be able to handle a large amount of requests at one time.
