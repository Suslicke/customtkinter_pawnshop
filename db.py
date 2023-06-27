from tortoise import Tortoise
import asyncio

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
