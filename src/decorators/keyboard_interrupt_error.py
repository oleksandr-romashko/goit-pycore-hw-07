def keyboard_interrupt_error(on_interrupt):
    """
    Decorator to handle KeyboardInterrupt exceptions in CLI apps.

    Args:
        on_interrupt (Callable): Function to call on KeyboardInterrupt.
                                 Must accept prefix and suffix keyword arguments.
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except KeyboardInterrupt:
                on_interrupt(prefix="\n", suffix="(Interrupted by user)")

        return inner

    return wrapper
