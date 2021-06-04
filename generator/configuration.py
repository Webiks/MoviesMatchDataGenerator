import os
import logging
from enum import Enum
from environs import Env
from dotenv.main import load_dotenv


logger = logging.getLogger("configuration")
env = Env()


def get_env_value_by_type(field_key, data_type):
    env_value = None
    try:
        if data_type == dict:
            env_value = env.json(field_key, None)
        elif data_type == list:
            env_value = env.list(field_key, None)
        elif data_type == bool:
            env_value = env.bool(field_key, None)
        elif data_type == int:
            env_value = env.int(field_key, None)
        elif data_type == float:
            env_value = env.float(field_key, None)
        elif data_type == str:
            env_value = env.str(field_key, None)
        elif issubclass(data_type, Enum):
            env_value = env.enum(field_key, type=data_type).name
        else:
            env_value = env(field_key, None)
    except:
        pass

    return env_value


def get_env_value(field_key, default_value, mapped_data_type=None):
    if mapped_data_type is not None:
        try:
            env_value = get_env_value_by_type(field_key, mapped_data_type)
        except:
            env_value = default_value
            if env(field_key):
                logger.warning(f"couldn't load field {field_key} from environment")
    else:
        env_value = get_env_value_by_type(field_key, type(default_value))

    return env_value


class Config:
    log_level = "INFO"
    generate_interval_sec = 60.0
    generate_interval_jitter_sec = 0
    records_to_generate = 1
    records_to_generate_jitter = 0
    existing_users_first_id = 1
    existing_users_last_id = 270896
    new_users_first_id = 300001
    new_users_last_id = 300300
    new_user_rating_prob = 0.5
    movies_ratings_distribution_file = "movies_ratings_distribution.csv"
    random_seed = 0

    def __init__(self):
        self.env_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..\\.env"
        )
        self.prefix = "MOVIES_MATCH_"
        load_dotenv(self.env_path, encoding="utf-8")
        for attr in dir(self):
            if not attr.startswith(("__", "_")) and attr not in [
                "type_mappings",
                "get_instance",
                "env_path",
                "prefix",
            ]:
                default_value = self.__getattribute__(attr)
                mapped_data_type = (
                    self.type_mappings.get(attr, None)
                    if hasattr(self, "type_mappings")
                    else None
                )
                attr_with_prefix = f"{self.prefix}{attr}".upper()
                env_value = get_env_value(
                    attr_with_prefix, default_value, mapped_data_type
                )
                setattr(
                    self, attr, env_value if env_value is not None else default_value
                )

    def get_sanitized(self):
        sanitized_config = {
            key: value
            for key, value in vars(self).items()
            if not callable(value) and not key.startswith(("__", "_"))
        }
        # TODO delete sensitive keys (if any)
        return sanitized_config
