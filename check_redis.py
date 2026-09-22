import redis

redis_client = redis.Redis.from_url("redis://localhost:6379", decode_responses=True)

# Get queue size
queue_size = redis_client.llen("job_queue")
print(f"Queue size: {queue_size}")

# Get all jobs
jobs = redis_client.lrange("job_queue", 0, -1)
print(f"Jobs in queue:")
for job in jobs:
    print(f"  - {job}")