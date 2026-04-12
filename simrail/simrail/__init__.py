import logging

from pymongo import MongoClient
from requests_cache import CachedSession, MongoCache

from . import prometheus_metrics

logger = logging.getLogger(__name__)

mongo_client = MongoClient("mongodb://mongo1.cabronita.com:27017,"
                           "mongo2.cabronita.com:27017,"
                           "mongo3.cabronita.com:27017"
                           "/?replicaSet=rs0")
cache_backend = MongoCache(connection=mongo_client)
session = CachedSession(backend=cache_backend, expire_after=60)

server_times_url = 'https://api1.aws.simrail.eu:8082/api/getTimeZone?serverCode='
servers_url = 'https://panel.simrail.eu:8084/servers-open'
stations_url = 'https://panel.simrail.eu:8084/stations-open?serverCode='
trains_url = 'https://panel.simrail.eu:8084/trains-open?serverCode='


class Station:
    """
    Example of source data:
    {'AdditionalImage1URL': 'https://api1.aws.simrail.eu:8083/Thumbnails/Stations/sl2.jpg',
     'AdditionalImage2URL': 'https://api1.aws.simrail.eu:8083/Thumbnails/Stations/sl3.jpg',
     'DifficultyLevel': 3,
     'DispatchedBy': [],
     'Latititude': 50.29477240684154,
     'Longitude': 19.37502719820521,
     'MainImageURL': 'https://api1.aws.simrail.eu:8083/Thumbnails/Stations/sl1m.jpg',
     'Name': 'Sławków',
     'Prefix': 'Sl',
     'id': '654b7d25b694ecf3f05ba098'}
    """

    def __init__(self, dict):
        self.dispatcher_id = dict['DispatchedBy'][0]['SteamId'] if dict['DispatchedBy'] else None
        self.name = dict['Name']


class Train:
    """
    Example of source data:
    {'EndStation': 'Wrocław Główny',
     'ServerCode': 'pl2',
     'StartStation': 'Warszawa Grochów',
     'TrainData': {'ControlledBySteamID': '76561198053288376',
                   'DistanceToSignalInFront': 708.52294921875,
                   'InBorderStationArea': False,
                   'Latititute': 52.11979675292969,
                   'Longitute': 20.65149688720703,
                   'SignalInFront': 'Gr_D@9280,67778,4',
                   'SignalInFrontSpeed': 32767,
                   'VDDelayedTimetableIndex': 11,
                   'Velocity': 68.7264404296875},
     'TrainName': 'EIJ - EIP',
     'TrainNoLocal': '1621',
     'Type': 'user',
     'Vehicles': ['Pendolino/ED250-018 Variant'],
     'id': '65635a10572ed21c875f8ac1'}
    """

    def __init__(self, dict):
        velocity = dict['TrainData']['Velocity']
        self.number = int(dict['TrainNoLocal'])
        self.station_start = dict['StartStation']
        self.station_end = dict['EndStation']
        self.type = dict['Type']
        self.engine = dict['Vehicles'][0]
        self.units = len(dict['Vehicles'])
        self.speed = int(dict['TrainData']['Velocity']) if velocity else 0
        self.name = dict['TrainName']
        self.signal_in_front = dict['TrainData']['SignalInFront']
        self.user = dict['TrainData']['ControlledBySteamID']


def get_servers(all=False):
    """
    Return list of server codes
    :param all: Include Xbox servers
    """
    servers = []
    logger.info(f"Getting servers")
    for item in session.get(servers_url).json()['data']:
        if item['IsActive']:
            if all:
                servers.append(item['ServerCode'])
            else:
                if not item['ServerCode'].startswith('xbx'):
                    servers.append(item['ServerCode'])
    return servers


def get_server_time_offset(server):
    """
    Return server time offset
    """
    try:
        logger.info(f"Getting offset for {server}")
        offset = session.get(server_times_url + server).json()
        return int(offset)
    except Exception:
        logger.warning(f"Failed to get data from {server_times_url + server}")
        raise


def get_stations(server):
    logger.info(f"Getting stations for {server}")
    stations = []
    for dict in session.get(stations_url + server).json()['data']:
        stations.append(Station(dict))
    return stations


def get_trains(server, all=False):
    """
    Return list of trains
    :param all: Include trains without signal in front
    """
    logger.info(f"Getting trains for {server}")
    trains = []
    for dict in session.get(trains_url + server).json()['data']:
        if dict['TrainData']['SignalInFront'] or all:
            trains.append(Train(dict))
    return trains
