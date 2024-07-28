from dotenv import dotenv_values

envs = dotenv_values("./app/.env")

def get_env(env_name: str):
    env = envs.get(env_name, None)
    if not env:
        raise EnvironmentError
    return env