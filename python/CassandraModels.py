import time
import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model


class users(Model):
    user_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    username = columns.Text(required=True, index=True)
    password = columns.Text(required=True)
    public_key = columns.Text(required=True)
    logged_in = columns.Text(required=False, index=True)
    login_time = columns.Double(required=False)
    api_key = columns.Text(required=False)


class api_keys(Model):
    key_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    creation_epoch = columns.Double(required=True, default=time.time)
