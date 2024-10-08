from time import sleep
from functools import wraps


def retry(retries=3, retry_delay=2, exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    A decorator that retries a function if specific exceptions are raised during its execution.

    Args:
        retries (int): Maximum number of attempts. Default is 3.
        retry_delay (int): Time in seconds between attempts. Default is 2.
        exceptions (tuple): Exceptions that trigger a retry. Default is (Exception,).
        error_message (str): Error message if the maximum retries are exceeded.

    Raises:
        Exception: If the number of retries is exceeded.

    Returns:
        any: The result of the decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Attempt {attempt + 1} of {retries}")
                    print(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
            raise Exception(error_message)
        return wrapper
    return decorator


def silent_retry_with_default(retries=3, retry_delay=2, default_return_value=None,
                              exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    A decorator that silently retries a function and returns a default value if it fails.

    Args:
        retries (int): Maximum number of attempts. Default is 3.
        retry_delay (int): Time in seconds between attempts. Default is 2.
        default_return_value (any): Value to return if the maximum retries are exceeded.
        exceptions (tuple): Exceptions that trigger a retry.
        error_message (str): Error message if the maximum retries are exceeded.

    Returns:
        any: The result of the decorated function or the default value.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Attempt {attempt + 1} of {retries}")
                    sleep(retry_delay)
            print(error_message)
            return default_return_value
        return wrapper
    return decorator

def retry_with_condition(retries=3, retry_delay=2, conditional=None, 
                         default_return_value=None, exceptions=(Exception,), 
                         error_message="Max retries exceeded"):
    """
    A decorator that retries a function if a specified condition is met or if specific exceptions are raised.

    Args:
        retries (int): The maximum number of attempts. Default is 3.
        retry_delay (int): Time in seconds to wait between retries. Default is 2.
        conditional (callable): A function that takes the result of the decorated function and returns True if a retry should occur. 
                                If None, only exceptions will trigger retries. Default is None.
        default_return_value (any): The value to return if the maximum number of retries is exceeded. Default is None.
        exceptions (tuple): A tuple of exceptions that will trigger a retry. Default is (Exception,).
        error_message (str): The error message to display if the maximum number of retries is exceeded.

    Returns:
        any: The result of the decorated function, or the default_return_value if the retries are exhausted.

    Example:
        @retry_with_condition(retries=5, retry_delay=3, conditional=lambda response: response["status_code"] == 500)
        def make_api_request(self, method, url, params=None, json=None, verify=False, headers=None, proxies=None):
            # Example API request function
            response = self.custom_base.get_restapi_instance().apirequest(
                method=method,
                url=url,
                json=json,
                verify=verify,
                headers=headers,
                params=params,
                proxies=proxies
            )
            return response

    How it works:
        - The decorator attempts to execute the decorated function up to `retries` times.
        - After each attempt, the function's result is checked against the `conditional` function, if provided.
        - If `conditional` returns True, or if an exception from the `exceptions` tuple is raised, the function will retry after `retry_delay` seconds.
        - If the condition is not met or no exception occurs, the result is returned immediately.
        - If the maximum number of retries is exceeded, the `default_return_value` is returned, and the `error_message` is printed.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    
                    # If a condition is provided, evaluate it
                    if conditional and conditional(result):
                        print(f"Condition for retry met. Attempt {attempt + 1} of {retries}.")
                        print(f"Retrying in {retry_delay} seconds...")
                        sleep(retry_delay)
                    else:
                        return result  # Return the result if the condition is not met
                    
                except exceptions as e:
                    print(f"Error: {e}. Attempt {attempt + 1} of {retries}.")
                    print(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
            
            print(error_message)
            return default_return_value
        return wrapper
    return decorator

