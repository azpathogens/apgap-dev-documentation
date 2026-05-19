"""Distributed Redis lock helpers for Celery tasks."""


# Compare-and-delete: if the task's TTL expired and another worker has since
# re-acquired the key, a naive DEL would delete the successor's valid lock.


def release_lock_if_owner(
    redis_client: redis.Redis,
    lock_key: str,
    request_id: str,
) -> None:
    """Atomically release ``lock_key`` only if its value equals ``request_id``.

    Errors are logged and swallowed; the lock will self-heal via TTL.
    """
