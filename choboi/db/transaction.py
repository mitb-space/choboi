import functools

from sqlalchemy.orm import sessionmaker


def begin_tx(func):
    # TODO: replace *args, *kwargs with a context obj
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('hello')
        tx = None
        conn = kwargs.get('conn')
        if conn:
            tx = sessionmaker(bind=conn)()
        try:
            kwargs['tx'] = tx
            res = func(*args, **kwargs)
            tx.commit()
            return res
        except Exception:
            if tx:
                tx.rollback()
        finally:
            if tx:
                tx.close()
    return wrapper
