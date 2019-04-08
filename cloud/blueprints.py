from flask import Blueprint, request
from google.cloud import datastore
import pprint
import json
import os

raspberry = Blueprint('raspberry', __name__)


@raspberry.route("/")
def raspberry_home():
    return "This application receives data from a Raspberry Pi!"

'''
@raspberry.route("/proximityget")
def raspberry_proximityget():
    datastore_client = datastore.Client()
    kind = 'Logs'
    key = datastore_client.key(kind)

    x = datastore_client.allocate_ids(key, 1)
    return json.dumps(x[0].id)
'''

@raspberry.route("/proximityget")
def raspberry_proximityget():
    datastore_client = datastore.Client()
    kind = 'Proximity_Logs'

    #key = datastore_client.key(kind)
    #x = datastore_client.get_multi([key])

    query = datastore_client.query(kind=kind)
    x = query.fetch()

    #return pprint.pformat(x, indent=10)





    return json.dumps(list(x))


@raspberry.route("/proximity/<string:datetime>/<int:distance>")
def raspberry_proximity(datetime, distance):
    datastore_client = datastore.Client()
    kind = 'Proximity_Logs'

    key = datastore_client.key(kind)
    ids = datastore_client.allocate_ids(key, 1)
    id = ids[0].id
    key = datastore_client.key(kind, id)

    # Prepares the new entity
    entity = datastore.Entity(key=key)
    entity['datetime'] = datetime
    entity['distance'] = distance

    # Saves the entity
    datastore_client.put(entity)

    return('Saved {}: {}'.format(entity.key.id, entity['datetime']))
