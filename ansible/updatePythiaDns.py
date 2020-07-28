import sys
import requests

def updateDns(ip):

    f = open("freednspass", "r")
    passwd = f.read()
    f.close()

    url = "	http://xultra:%s@sync.afraid.org/nic/update?hostname=pythia-resvag.crabdance.com&myip=%s"
    URL = url % (passwd, ip)

    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    r = requests.get(URL, headers=ua)

    response = r.text
    if response.__contains__("Updated"):
        print("DNS updated, response: {}".format(response))
    else:
        print("WARNING, DNS NOT UPDATED, response: {}".format(response))


if __name__ == "__main__":
    updateDns(sys.argv[1])
