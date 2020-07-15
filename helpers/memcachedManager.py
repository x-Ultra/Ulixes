from pymemcache.client.base import Client
from time import sleep
# TODO, insert a static ip for the cluster
CLUSTER_ENDPOINT = "testmemcached.nryvye.cfg.euc1.cache.amazonaws.com"
CLUSTER_PORT = 11211
WAIT_ON_SEARCH = "INSERTING"
POOL_SEC = 1


# method used to query into the sitributed cache and see if the
# itinerary (identified with itinKey) has already been computed.
# This method will return a string in json format of the itinerary
# or None if it is not present into memcached.
def searchInMemcached(lat, lon, t, transp):

    itinKey = str(lat)+str(lon)+str(t)+str(transp)

    try:
        client = Client((CLUSTER_ENDPOINT, CLUSTER_PORT))
        while True:
            itinJson = client.get(itinKey)
            if itinJson != None and itinJson == WAIT_ON_SEARCH:
                # some other server is evaluating the same itinerary,
                # just wait and pool fot the result
                sleep(POOL_SEC)
            else:
                break
    except:
        itinJson = None

    return itinJson


# Method that return true if the insertion in cache was successful
# False otherwise
def insertInMemcached(lat, lon, t, transp, itinJsonString):
    itinKey = str(lat) + str(lon) + str(t) + str(transp)
    try:
        client = Client((CLUSTER_ENDPOINT, CLUSTER_PORT))
        response = client.set(itinKey, itinJsonString)
    except:
        response = False

    return response


# method that marks a given itinerary as 'isterting'
def insertingInProgress(lat, lon, t, transp):

    itinKey = str(lat) + str(lon) + str(t) + str(transp)
    try:
        client = Client((CLUSTER_ENDPOINT, CLUSTER_PORT))
        response = client.set(itinKey, WAIT_ON_SEARCH)
    except:
        response = False

    return response