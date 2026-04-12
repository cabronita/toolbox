#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
from prometheus_client import start_http_server
from time import asctime, sleep

import simrail

parser = ArgumentParser()
parser.add_argument('-v', '--verbosity', action='count', default=0, help='increase output verbosity (-vv for debug)')
args = parser.parse_args()

verbosity = args.verbosity

logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
logging.basicConfig(level=logging_levels[verbosity],
                    format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    start_http_server(8000)
    while True:
        results = []
        for server in simrail.get_servers():
            try:
                time_offset = simrail.get_server_time_offset(server)
            except Exception:
                time_offset = 0
            trains = simrail.get_trains(server)
            drivers_num = len([t for t in trains if t.type == 'user'])
            stations = simrail.get_stations(server)
            dispatchers_num = len([s for s in stations if s.dispatcher_id])
            results.append({"server": server,
                            "time_offset": time_offset,
                            "trains": len(trains),
                            "drivers": drivers_num,
                            "stations": len(stations),
                            "dispatchers": dispatchers_num})
        simrail.prometheus_metrics.update(results)
        print(f"Cycle completed on {asctime()}")
        sleep(60)


if __name__ == "__main__":
    logging.info("Starting...")
    print("Starting...")
    try:
        main()
    except KeyboardInterrupt as eki:
        logging.info("Stopping...")
        print("Stopping...")
