def undocumented(func: Callable) -> Callable:
    @functools.wraps(func)
    def __wrapped(*args, **kwargs):
        fname = func.__qualname__.split(".")
        if len(fname) == 2:
            log(logger.warning, fname[0], fname[1], f"{Bo}{Y}Undocumented{E}")
        else:
            mname = func.__globals__["__file__"].split(".")
            log(logger.warning, mname[0], fname[0], f"{Bo}{Y}Undocumented{E}")
        return func(*args, **kwargs)

    return __wrapped
