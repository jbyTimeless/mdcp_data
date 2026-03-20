import asyncio
from common.dependencies.es_client import es_client

async def test_es_connection():
    try:
        info = await es_client.info()
        print(f"ES Connection Success: {info['version']['number']}")
    except Exception as e:
        print(f"ES Connection Failed: {str(e)}")
    finally:
        await es_client.close()

if __name__ == "__main__":
    asyncio.run(test_es_connection())
