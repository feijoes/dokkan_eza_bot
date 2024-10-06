from datetime import datetime
from functools import wraps
import time

def log_error(message):
    """Log an error message with a timestamp."""
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

def delete_last_line():
    print("\033[A                             \033[A")


def retry(retries=5, wait=2):
    """Decorator to retry a method call with specified retries and wait time."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal retries, wait
            attempts = retries
            while attempts > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log_error(f"Error during {func.__name__}: {str(e)}")
                    time.sleep(wait)
                    attempts -= 1
            return False

        return wrapper

    return decorator
