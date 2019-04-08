from flask import Blueprint, request
from google.cloud import datastore
import json

raspberry = Blueprint('raspberry', __name__)


@raspberry.route("/")
def raspberry_home():
    return "This application receives data from a Raspberry Pi!"


@raspberry.route("/proximity_records")
def raspberry_proximityget():
    datastore_client = datastore.Client()
    kind = 'Proximity_Logs'

    query = datastore_client.query(kind=kind)
    x = query.fetch()
    return json.dumps(list(x))


@raspberry.route("/proximity/<string:datetime>/<float:distance>")
def raspberry_proximity(datetime, distance):
    datastore_client = datastore.Client()
    kind = 'Proximity_Logs'

    # Gets an usable ID
    key = datastore_client.key(kind)
    ids = datastore_client.allocate_ids(key, 1)
    id = ids[0].id

    # Prepares the new entity
    key = datastore_client.key(kind, id)
    entity = datastore.Entity(key=key)
    entity['datetime'] = datetime
    entity['distance'] = distance

    # Saves the entity
    datastore_client.put(entity)

    return('Saved {}: {}'.format(entity.key.id, entity['datetime']))
