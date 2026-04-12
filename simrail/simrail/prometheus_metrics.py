from prometheus_client import Gauge
import logging

logger = logging.getLogger(__name__)

time_offset = Gauge("simrail_time_offset",
                    "Server time offset",
                    ["server"])

trains = Gauge("simrail_trains",
               "Number of trains",
               ["server"])

drivers = Gauge("simrail_drivers",
                "Number of drivers",
                ["server"])

stations = Gauge("simrail_stations",
                 "Number of stations",
                 ["server"])

dispatchers = Gauge("simrail_dispatchers",
                    "Number of dispatchers",
                    ["server"])


def update(results):
    logger.info("Updating metrics")
    for i in results:
        server = i["server"]
        time_offset.labels(server=server).set(i["time_offset"])
        trains.labels(server=server).set(i["trains"])
        drivers.labels(server=server).set(i["drivers"])
        stations.labels(server=server).set(i["stations"])
        dispatchers.labels(server=server).set(i["dispatchers"])
