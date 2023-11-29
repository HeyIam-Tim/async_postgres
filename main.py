import asyncio
import asyncpg


QUERY = """INSERT INTO async_table VALUES ($1, $2, $3)"""


async def make_request(counter: int, db_pool) -> None:
    """Делает запрос в бд."""

    await db_pool.fetch(QUERY, 1, 'adfadf', 33)
    print('Делаю запрос в бд: ', counter)
    await asyncio.sleep(2)
    return None


async def main() -> None:
    """Основная курутина."""

    tasks_list = []
    chunck = 10
    max_range = 10000
    pended = 0

    # db_pool = await asyncpg.create_pool("postgresql://localhost:5432/test_async")
    db_pool = await asyncpg.create_pool("")

    for counter in range(max_range):
        task = asyncio.create_task(make_request(counter=counter, db_pool=db_pool))
        tasks_list.append(task)
        pended += 1

        if tasks_list == chunck or pended == max_range:
            await asyncio.gather(*tasks_list, return_exceptions=True)
            tasks_list = []
            print(pended)

asyncio.run(main())
