from pymemcache.client.base import Client

# TODO, insert a static ip for the cluster
CLUSTER_ENDPOINT = "testmemcached.nryvye.cfg.euc1.cache.amazonaws.com"
CLUSTER_PORT = 11211


# method used to query into the sitributed cache and see if the
# itinerary (identified with itinKey) has already been computed.
# This method will return a string in json format of the itinerary
# or None if it is not present into memcached.
def searchInMemcached(itinKey):

    try:
        client = Client((CLUSTER_ENDPOINT, CLUSTER_PORT))
        itinJson = client.get(itinKey)
    except:
        itinJson = None

    return itinJson

# Method that return true if the insertion in cache was successful
# False otherwise
def insertInMemcached(itinKey, itinJsonString):

    try:
        client = Client((CLUSTER_ENDPOINT, CLUSTER_PORT))
        response = client.set(itinKey, itinJsonString)
    except:
        response = False

    return response