import logging
import os

import hvac
import redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class SecretsManager:
    """
    Менеджер секретов с многоуровневым доступом к конфиденциальным данным.

    Обеспечивает получение секретов из следующих источников
        (в порядке приоритета):
    1. Redis (кэш)
    2. Hashicorp Vault
    3. Переменные окружения
    4. Значение по умолчанию

    Attributes:
        cache_ttl (int): Время жизни кэша в секундах
        redis_client (redis.StrictRedis): Клиент Redis для кэширования
        vault_client (hvac.Client): Клиент Vault для получения секретов
    """

    def __init__(
        self,
        redis_host: str = "redis",
        redis_port: int = 6379,
        vault_url: str = "http://vault:8200",
        vault_token: str = os.getenv("VAULT_TOKEN", ""),
        cache_ttl: int = 3600,
    ):
        self.cache_ttl = cache_ttl
        self.redis_client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            db=0,
            socket_connect_timeout=5,
            decode_responses=True,
        )
        self.vault_client = hvac.Client(
            url=vault_url,
            token=vault_token,
            timeout=5,
        )

    def get_from_redis(self, cache_key: str) -> str | None:
        try:
            value = self.redis_client.get(cache_key)
            return str(value) if value is not None else None
        except RedisError as e:
            logger.error(f"Redis error: {e}")
            return None

    def get_from_vault(self, path: str, key: str) -> str | None:
        try:
            secret = self.vault_client.secrets.kv.read_secret_version(
                path=path,
                mount_point="secrets",
            )
            return secret["data"]["data"].get(key)
        except Exception as e:
            logger.error(f"Vault error: {e}")
            return None

    def cache_secret(self, cache_key: str, value: str) -> None:
        try:
            self.redis_client.set(cache_key, value, ex=self.cache_ttl)
        except RedisError as e:
            logger.error(f"Failed to cache secret: {e}")

    def get_secret(
        self,
        path: str,
        key: str,
        default: str = "",
    ) -> str:
        """Get secret from Redis → Vault → env → default."""
        cache_key = f"vault:{path}:{key}"

        # Try Redis cache first
        cached_value = self.get_from_redis(cache_key)
        if cached_value:
            logger.debug(f"Secret {key} retrieved from cache")
            return cached_value

        # Try Vault
        vault_value = self.get_from_vault(path, key)
        if vault_value:
            self.cache_secret(cache_key, vault_value)
            return vault_value

        # Try environment variable
        env_value = os.environ.get(key)
        if env_value:
            logger.debug(f"Secret {key} retrieved from env")
            return env_value

        # Return default
        logger.debug(f"Using default value for {key}")
        return default
