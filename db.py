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
    
    role_secretary, created = await Roles.get_or_create(name="Оценщик")
    await role_secretary.save()

    role_admin, created = await Roles.get_or_create(name="Администратор")
    await role_admin.save()

    user, created = await Users.get_or_create(
        first_name="1",
        surname="1",
        patronymic="1",
        access_level=role_admin,
        password="1"
    )
    await user.save()
    


loop = asyncio.get_event_loop()
loop.run_until_complete(init())
