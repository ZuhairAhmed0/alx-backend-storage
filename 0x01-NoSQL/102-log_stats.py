#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient


def log_stats():
    """
    provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient("mongodb://127.0.0.1:27017")
    logs = client.logs.nginx

    totoal = logs.count_documents({})
    get = logs.count_documents({"method": "GET"})
    post = logs.count_documents({"method": "POST"})
    put = logs.count_documents({"method": "PUT"})
    patch = logs.count_documents({"method": "PATCH"})
    delete = logs.count_documents({"method": "DELETE"})
    path = logs.count_documents({"method": "GET", "path": "/status"})

    print("{} logs".format(totoal))
    print("Methods:")
    print("\tmethod GET: {}".format(get))
    print("\tmethod POST: {}".format(post))
    print("\tmethod PUT: {}".format(put))
    print("\tmethod PATCH: {}".format(patch))
    print("\tmethod DELETE: {}".format(delete))
    print("{} status check".format(path))
    print("IPs:")
    sorted_ips = logs.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    i = 0
    for s in sorted_ips:
        if i == 10:
            break
        print("\t{}: {}".format(s.get('_id'), s.get('count')))
        i += 1


if __name__ == "__main__":
    log_stats()
