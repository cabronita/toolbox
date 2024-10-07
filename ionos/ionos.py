from pprint import pprint
import os
import socket

import requests

api_key_public_prefix = os.getenv("api_key_public_prefix")
api_key_secret = os.getenv("api_key_secret")


class Ionos:
    class Record:
        def __init__(self, d):
            self.changeDate = None
            self.content = None
            self.disabled = None
            self.id = None
            self.name = None
            self.prio = None
            self.rootName = None
            self.ttl = None
            self.type = None
            self.__dict__ = d
            if self.type == "A":
                self.ip = socket.inet_aton(self.content)

        def __str__(self):
            return self.name

    def __init__(self, api_key_public_prefix, api_key_secret):
        self.__api_key = f"{api_key_public_prefix}.{api_key_secret}"
        self.__base_url = "https://api.hosting.ionos.com/dns"
        self.__headers = {"accept": "application/json", "X-API-Key": self.__api_key}
        self.zone = self.get_zone()
        self.records = self.get_records()
        self.a_records = self.get_a_records()
        self.cname_records = self.get_cname_records()

    def get_data(self, endpoint):
        print(f"Getting data from {endpoint}")
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
            if i.type == "CNAME":
                cname_records.append(i)
        return cname_records

    def set_ttl(self, item):
        print(f"Resetting ttl for {item}")
        json_data = {"ttl": 3600}
        headers = self.__headers
        headers["Content-Type"] = "application/json"
        response = requests.put(url=f"{self.__base_url}/v1/zones/{self.zone}/records/{item.id}", headers=headers,
                                json=json_data)
        print(response.json())


if __name__ == "__main__":
    dns = Ionos(api_key_public_prefix, api_key_secret)

    for record in sorted(dns.a_records, key=lambda i: i.ip):
        print(f"{record.type} {record.content} {record.name}")

    for record in sorted(dns.cname_records, key=lambda i: i.name):
        print(f"{record.type} {record.name} {record.content}")

    for record in dns.a_records + dns.cname_records:
        if record.ttl != 3600:
            print(f"{record.type} {record.content} {record.name} {record.ttl}")
            dns.set_ttl(record)
