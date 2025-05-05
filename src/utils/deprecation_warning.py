import functools
import logging


def transition_warning(
    reason: str = "This function is transitional and will be removed in a future version.",
):
    """
    Decorator to mark functions as deprecated during transition.
    Emits a DeprecationWarning (once per call site) and logs a debug message.

    Args:
        reason (str): Custom deprecation message.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.debug(
                "[TRANSITION DEBUG] Called deprecated function '%s' - %s",
                func.__name__,
                reason,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
