import sys

import requests


def updateDns(system, newIp):

    f = open("noippass", "r")
    passwd = f.read()
    f.close()

    if (system == "pythia"):
        url = "http://alterramulti@yahoo.it:%s@dynupdate.no-ip.com/nic/update?hostname=pythia-resvag.ddns.net&myip=%s"
    elif system == "memcached":
        url = "http://alterramulti@yahoo.it:%s@dynupdate.no-ip.com/nic/update?hostname=memcached-resvag.ddns.net&myip=%s"
    else:
        url = "http://alterramulti@yahoo.it:%s@dynupdate.no-ip.com/nic/update?hostname=ulixes-resvag.ddns.net&myip=%s"

    URL = url % (passwd, newIp)
    ua = {"User-Agent": "Mozilla"}
    r = requests.get(URL, headers=ua)
    response = r.text
    if response.__contains__("good") or response.__contains__("nochg"):
        print("DNS updated, response: {}".format(response))
    else:
        print("WARNING, DNS NOT UPDATED, response: {}".format(response))


if __name__ == "__main__":
    updateDns(sys.argv[1], sys.argv[2])
