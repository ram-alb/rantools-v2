import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


def acquire_lock(lock_key: str, timeout: int) -> bool:
    """Acquire a lock with a given key and timeout."""
    return redis_client.set(lock_key, 'locked', ex=timeout, nx=True)


def release_lock(lock_key: str) -> None:
    """Release the lock with the given key."""
    redis_client.delete(lock_key)


def is_locked(lock_key: str) -> bool:
    """Check if a lock with the given key exists."""
    return redis_client.exists(lock_key)
