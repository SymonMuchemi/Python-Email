import redis

# create redis client
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = 'shopsmart:mail'
GROUP_NAME = 'shopsmart:mail_group'
CONSUMER_NAME = 'alpha'

# Create consumer group
try:
    redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, id='0', mkstream=True)
except Exception as e:
    print(f'Error creating consumer group: {e.message}')
    pass
