from cloudspace.settings import MAX_THREAD_WORKERS
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS)


def background(func):
    def decorator(*args, **kwargs):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                print("Worker thread exception: %s", str(e))
        executor.submit(wrapper, *args, **kwargs)
    return decorator
