from functools import wraps

import aioredis
from .redis_controller import RedisController

REDIS_KEY = "run_single_generator"


class RunSingleGenerator:
    def __init__(self, redis: aioredis.StrictRedis, app_prefix: str, logger):
        self.redis = redis
        self.app_prefix = app_prefix
        self.logger = logger
        self.key = f"{REDIS_KEY}:{app_prefix}"

    async def clear_redis_data(self) -> None:
        """
        Очищаем данные по ключам приложения.
        :return:
        """
        self.logger.info(f"clear '{self.key}:*'")
        keys = await self.redis.keys(f"{self.key}:*")
        if not keys:
            return
        pipe = await self.redis.pipeline()
        for k in keys:
            await pipe.delete(k)
        await pipe.execute()

    def __call__(self, users_generator):
        @wraps(users_generator)
        async def wrapper(*args, **kwargs):
            r_data = RedisController(
                self.redis, f"{self.key}:{users_generator.__name__}"
            )
            my_number = await r_data.incr()
            self.logger.info(f"enter {my_number}")
            if my_number == 1:
                # при первом вызове очищаем результат вычислений
                await r_data.clear_res()
                await r_data.set_running()
            else:
                await r_data.await_stop_running()
                await r_data.set_running()

            res = None
            g = users_generator(*args, **kwargs)

            while True:
                rerun = await r_data.is_somebody_want_rerun_alg(my_number)
                if rerun:
                    await g.aclose()
                    await r_data.set_stopped()
                    self.logger.info(f"stopped {my_number}")
                    res = await r_data.await_result()
                    return res
                try:
                    res = await anext(g)
                except StopAsyncIteration:
                    await r_data.set_result(res)
                    self.logger.info(f"calculate {my_number}")
                    return res
                except Exception as ex:
                    await r_data.set_result(res)
                    raise ex
        return wrapper
