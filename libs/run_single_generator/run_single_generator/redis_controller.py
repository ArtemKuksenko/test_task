import asyncio
import pickle

from aioredis import StrictRedis

AWAIT_TIME = 0.1
REDIS_KEY = "run_single_generator"


class RedisController:
    def __init__(self, redis: StrictRedis, name: str, app_prefix: str):
        self.redis = redis
        key = f"{REDIS_KEY}:{app_prefix}:{name}"
        self.key_number = f"{key}:number"
        self.key_res = f"{key}:res"
        self.key_running = f"{key}:run"

    async def incr(self) -> int:
        return await self.redis.incr(self.key_number)

    async def decr(self) -> None:
        await self.redis.decr(self.key_number)

    async def is_somebody_want_rerun_alg(self, my_number) -> bool:
        """
        Если номер вызова функции превышает текущий,
        значит алгоритм был вызван повторно
        :param my_number:
        :return:
        """
        max_number = int(await self.redis.get(self.key_number))
        return max_number > my_number

    async def await_result(self):
        """
        Ожидаем, пока алгоритм открутится в другом вызове
        :return:
        """
        while True:
            await asyncio.sleep(AWAIT_TIME)
            res = await self.redis.get(self.key_res)
            if res:
                return pickle.loads(res)

    async def set_result(self, res) -> None:
        """
        Проставляем вычисленный результат, очищаем метаданные
        :param res:
        :return:
        """
        await self.redis.set(self.key_res, pickle.dumps(res))
        await self.redis.delete(self.key_number)
        await self.redis.delete(self.key_running)

    async def clear_res(self) -> None:
        await self.redis.delete(self.key_res)

    async def set_running(self) -> None:
        await self.redis.set(self.key_running, 1)

    async def set_stopped(self) -> None:
        await self.redis.set(self.key_running, 0)

    async def await_stop_running(self) -> None:
        """
        Ожидаем пока алгоритм прекратит вычисляться в старом вызове
        :return:
        """
        while True:
            await asyncio.sleep(AWAIT_TIME)
            is_running = await self.redis.get(self.key_running)
            if is_running == b'0':
                return
