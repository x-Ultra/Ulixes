class BootstrapRequest:

    def __init__(self, reqType, ip, lat, lon, numFogNodes, beatPort):
        self.lat = lat
        self.lon = lon
        self.ip = ip
        self.reqtype = reqType
        self.beatPort = beatPort
        self.numFogNodes = numFogNodes


