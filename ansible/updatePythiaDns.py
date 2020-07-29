import sys
import requests

def updateDns(ip, num):

    f = open("freednspass", "r")
    passwd = f.read()
    f.close()

    if int(num) == 1:
        url = "http://xultra:%s@sync.afraid.org/u/?h=pythia1-resvag.crabdance.com&ip=%s"
    else:
        url = "http://xultra:%s@sync.afraid.org/u/?h=pythia2-resvag.crabdance.com&ip=%s"

    URL = url % (passwd, ip)
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    r = requests.get(URL, headers=ua)

    response = r.text
    if response.__contains__("Updated"):
        print("DNS updated, response: {}".format(response))
    else:
        print("WARNING, DNS NOT UPDATED, response: {}".format(response))


if __name__ == "__main__":
    updateDns(sys.argv[1], sys.argv[2])
