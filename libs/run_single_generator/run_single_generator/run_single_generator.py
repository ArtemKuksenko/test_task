from functools import wraps

import aioredis
from .redis_controller import RedisController


class RunSingleGenerator:
    def __init__(self, redis: aioredis.StrictRedis):
        self.redis = redis

    def __call__(self, users_generator):
        @wraps(users_generator)
        async def wrapper(*args, **kwargs):
            r_data = RedisController(self.redis, users_generator.__name__)
            my_number = await r_data.incr()
            print(f"enter {my_number}")
            if my_number == 1:
                await r_data.clear_res()
                await r_data.set_running()
            else:
                await r_data.await_stop_running()
                await r_data.set_running()

            res = None
            g = users_generator(*args, **kwargs)

            while True:
                if await r_data.is_somebody_want_rerun_alg(my_number):
                    await g.aclose()
                    await r_data.set_stopped()
                    print(f"stopped {my_number}")
                    res = await r_data.await_result()
                    return res
                try:
                    res = await anext(g)
                except StopAsyncIteration:
                    await r_data.set_result(res)
                    print(f"calculate {my_number}")
                    return res
                except Exception as ex:
                    await r_data.decr()
                    raise ex
        return wrapper
