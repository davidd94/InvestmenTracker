from threading import Thread


def async_task(f):
    def async_wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return async_wrapper