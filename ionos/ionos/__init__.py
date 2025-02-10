import logging
import os
import socket

import requests

logger = logging.getLogger(__name__)

api_key_public_prefix = os.getenv("api_key_public_prefix")
api_key_secret = os.getenv("api_key_secret")


class Ionos:
    class Record:
        def __init__(self, d):
            self.changeDate = None
            self.content: str = None
            self.disabled = None
            self.id = None
            self.name: str = None
            self.prio = None
            self.rootName = None
            self.ttl = None
            self.type = None
            self.__dict__ = d
            if self.type == "A":
                self.inet_aton = socket.inet_aton(self.content)

        def __str__(self):
            return self.name

        def __eq__(self, other):
            if isinstance(other, Ionos.Record):
                return self.name == other.name
            return False

    def __init__(self, api_key_public_prefix, api_key_secret):
        self.__api_key = f"{api_key_public_prefix}.{api_key_secret}"
        self.__base_url = "https://api.hosting.ionos.com/dns"
        self.__headers = {"accept": "application/json", "X-API-Key": self.__api_key}
        self.zone = self.get_zone()
        self.records = self.get_records()
        self.a_records = self.get_a_records()
        self.cname_records = self.get_cname_records()

    def get_data(self, endpoint):
        logger.info(f"Getting data from {endpoint}")
        url = f"{self.__base_url}{endpoint}"
        headers = self.__headers
        return requests.get(url=url, headers=headers)

    def get_zone(self):
        response = self.get_data("/v1/zones")
        return response.json()[0]["id"]

    def get_records(self):
        records = []
        response = self.get_data(f"/v1/zones/{self.zone}")
        for item in response.json()["records"]:
            records.append(self.Record(item))
        return records

    def get_a_records(self):
        a_records = []
        for i in self.records:
            if i.type == "A":
                a_records.append(i)
        return a_records

    def get_cname_records(self):
        cname_records = []
        for i in self.records:
            if i.type == "CNAME" and i.content.endswith(".cabronita.com"):
                cname_records.append(i)
        return cname_records

    def set_ttl(self, item, ttl):
        logger.info(f"Resetting ttl for {item}")
        json_data = {"ttl": ttl}
        headers = self.__headers
        headers["Content-Type"] = "application/json"
        response = requests.put(url=f"{self.__base_url}/v1/zones/{self.zone}/records/{item.id}", headers=headers,
                                json=json_data)
        logger.info(response.json())

    def create_records(self, records):
        """
        Push list of records
        :param records:
        :return: status code
        """
        json_records = []
        for rec in records:
            json_records.append({"content": rec.content,
                                 "name": rec.name,
                                 "ttl": 3600,
                                 "type": "A"})

        logger.info(f"Creating records {json_records}")
        json_data = json_records
        headers = self.__headers
        headers["Content-Type"] = "application/json"
        response = requests.post(url=f"{self.__base_url}/v1/zones/{self.zone}/records", headers=headers, json=json_data)
        logger.info(response.json())
        return response.status_code

    def delete_record(self, record):
        """
        Remove single record
        :param record: Ionos.Record
        :return: status code
        """
        logger.info(f"Removing {record.name}")
        headers = self.__headers
        headers["Content-Type"] = "*/*"
        response = requests.delete(url=f"{self.__base_url}/v1/zones/{self.zone}/records/{record.id}", headers=headers)
        logger.info(response.status_code)
        return response.status_code

    def update_record(self, record):
        """
        Update single record
        :param record: Ionos.Record
        :return: status code
        """
        logger.info(f"Updating {record.name}")
        print(vars(record))
        json_data = {"content": record.content}
        headers = self.__headers
        headers["Content-Type"] = "application/json"
        response = requests.put(url=f"{self.__base_url}/v1/zones/{self.zone}/records/{record.id}", headers=headers,
                                json=json_data)
        logger.info(response.status_code)
        return response.status_code
