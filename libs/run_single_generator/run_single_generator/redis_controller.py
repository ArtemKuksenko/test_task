import asyncio
import pickle

from aioredis.client import Pipeline

AWAIT_TIME = 0.1


class RedisController:
    def __init__(self, redis, name: str):
        self.redis = redis
        key = f"run_single_generator:{name}"
        self.key_number = f"{key}:number"
        self.key_res = f"{key}:res"

    async def incr(self) -> int:
        return await self.redis.incr(self.key_number)

    async def decr(self) -> None:
        await self.redis.decr(self.key_number)

    async def is_somebody_want_rerun_alg(self, my_number) -> bool:
        max_number = int(await self.redis.get(self.key_number))
        return max_number > my_number

    async def await_result(self):
        while True:
            await asyncio.sleep(AWAIT_TIME)
            res = await self.redis.get(self.key_res)
            if res:
                return pickle.loads(res)

    async def set_result(self, res):
        await self.redis.set(self.key_res, pickle.dumps(res))

    async def clear_res(self):
        await self.redis.delete(self.key_res)

    # async def is_running(self) -> bool:
    #     return bool(await self.pipe.get(self.running_key))
    #
    # async def is_stopped(self) -> bool:
    #     return bool(await self.pipe.get(self.running_key))
    #
    # async def stop_running(self) -> None:
    #     await self.pipe.set(self.stop_key, True)
    #     await self.pipe.execute()
    #
    #     #  Ждем пока алгоритм не будет остановлен
    #     while True:
    #         await asyncio.sleep(AWAIT_TIME)



    # async def get_data(self) -> dict:
    #     data = await self.pipe.get(self.key)
    #     if not data:
    #         return dict()
    #     return pickle.loads(data)
    #
    # async def set_data(self, data: dict) -> None:
    #     await self.pipe.set(self.key, pickle.dumps(data))
    #     await self.pipe.execute()
