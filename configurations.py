from dotenv import dotenv_values

envs = dotenv_values(".env")

def get_env(env_name: str):
    return envs.get(env_name)
