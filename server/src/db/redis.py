import redis.asyncio as aioredis

from src.config import Config

JTI_EXPIRY = 3600 # 1 hour

token_blocklist = aioredis.from_url(
    Config.REDIS_URL,
    # decode_responses=True,
)

async def token_in_blocklist(jti: str) -> bool:
    """
    Check if the token is in the blocklist.
    """
    jti = await token_blocklist.get(jti)

    return jti is not None
    

async def add_jti_to_blocklist(jti: str) -> None:
    """
    Add the token to the blocklist.
    """
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)