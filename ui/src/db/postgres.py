from services.postgres import sessionmanager


async def get_db():
    async with sessionmanager.session() as session:
        yield session
