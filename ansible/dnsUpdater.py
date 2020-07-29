import sys
import requests
import subprocess

def updateDns(system, domain):

    f = open("noippass", "r")
    passwd = f.read()
    f.close()
    cmd = "dig +short %s @resolver1.opendns.com" % domain
    newIp = subprocess.check_output(cmd, shell=True).decode("utf-8").split("\n")[0]

    if system == "memcached":
        url = "http://alterramulti@yahoo.it:%s@dynupdate.no-ip.com/nic/update?hostname=memcached-resvag.ddns.net&myip=%s"
    else:
        url = "http://alterramulti@yahoo.it:%s@dynupdate.no-ip.com/nic/update?hostname=ulixes-resvag.ddns.net&myip=%s"

    URL = url % (passwd, newIp)
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    r = requests.get(URL, headers=ua)

    response = r.text
    if response.__contains__("good") or response.__contains__("nochg"):
        print("DNS updated, response: {}".format(response))
    else:
        print("WARNING, DNS NOT UPDATED, response: {}".format(response))


if __name__ == "__main__":
    updateDns(sys.argv[1], sys.argv[2])
