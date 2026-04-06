#!/usr/bin/env python3

from time import sleep
from prometheus_client import start_http_server, Gauge
from temperusb.temper import TemperHandler

if __name__ == "__main__":
    print("Starting...")
    start_http_server(8000)
    g = Gauge("temperature_office", "Office temperature")
    th = TemperHandler()
    dev = th.get_devices()[0]

    while True:
        g.set(round(dev.get_temperature(), 1))
        sleep(60)
