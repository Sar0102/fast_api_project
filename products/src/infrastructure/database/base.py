import aioredis

redis_client = aioredis.StrictRedis(host='product_redis', port=6379, db=0)