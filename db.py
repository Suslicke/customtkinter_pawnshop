from tortoise import Tortoise
import asyncio

from models import Users, Roles

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
    
    roles = Roles(name="Секретарь", description="1")
    await roles.save()
    user = Users(first_name="1", surname="1", patronymic="1", access_level=roles, password="1")
    await user.save()
    


loop = asyncio.get_event_loop()
loop.run_until_complete(init())
