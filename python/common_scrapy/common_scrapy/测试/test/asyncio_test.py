# -*- coding:utf-8 -*-
import asyncio


async def show(num):
    print("Number is {}".format(num))


# coroutine = [(show(i)) for i in range(10)]  # 指定协程函数的方式创建协程对象

task = [asyncio.ensure_future(show(i)) for i in range(10)]  # 把协程对象加入任务队列

loop = asyncio.get_event_loop()
for t in task:
    loop.run_until_complete(t)  # 循环执行任务队列里面的任务
