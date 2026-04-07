from typing import List, NamedTuple


class ModelEnv(NamedTuple):
    api_base_version: str
    docker_name: str
    docker_tag: str
    allowed_extensions: List[str]
    max_file_weight: int
    time_out: int
    app_secret: str
    api_host: str
    api_port: int
    rpc_port: int
    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
