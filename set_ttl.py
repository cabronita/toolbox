import os

from ionos import Ionos

ionos = Ionos(api_key_public_prefix=os.getenv("api_key_public_prefix"),
              api_key_secret=os.getenv("api_key_secret"))


def update(record, ttl):
    print(record.name)
    print(record.ttl)
    if record.ttl != ttl:
        record.ttl = ttl
        ionos.update_record(record)
    print(record.ttl)


if __name__ == "__main__":
    ttl = 3600
    for cname_record in ionos.cname_records:
        update(cname_record, ttl)
    for a_record in ionos.a_records:
        update(a_record, ttl)
