from backend.config.utils.vault_secrets import SecretsManager

secrets = SecretsManager()

broker_api = secrets.get_secret(
    "celery_flower",
    "FLOWER_BROKER_API",
    "http://rabbitmq:15672/api/",
)
basic_auth = secrets.get_secret(
    "celery_flower",
    "FLOWER_BASIC_AUTH",
    "['rabbitmq:rabbitmq']",
).split(",")
port = int(secrets.get_secret("celery_flower", "FLOWER_PORT", "5555"))
address = secrets.get_secret("celery_address", "FLOWER_ADDRESS", "0.0.0.0")
persistent = secrets.get_secret(
    "celery_flower",
    "FLOWER_PERSISTENT",
    "True",
) in ("TRUE", "1", "T", "t")
max_tasks = int(
    secrets.get_secret("celery_flower", "FLOWER_MAX_TASKS", "10000"),
)
inspect_timeout = float(
    secrets.get_secret("celery_flower", "FLOWER_INSPECT_TIMEOUT", "10.0"),
)
auth = secrets.get_secret("celery_flower", "FLOWER_AUTH", "basic")
db = secrets.get_secret("celery_flower", "FLOWER_DB", "/tmp/flower.db")
