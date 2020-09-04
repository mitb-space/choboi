import functools

from sqlalchemy.orm import Session


def begin_tx(func):
    # TODO: replace *args, *kwargs with a context obj
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('hello')
        tx = None
        conn = kwargs.get('conn')
        if conn:
            tx = Session(bind=conn)
        try:
            kwargs['tx'] = tx
            return func(*args, **kwargs)
        except Exception:
            if tx:
                tx.rollback()
        finally:
            if tx:
                tx.close()
    return wrapper
