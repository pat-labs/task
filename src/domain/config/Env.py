from typing import List, NamedTuple


class Env(NamedTuple):
    api_base_version: str
    node: int
    worker: int
    docker_name: str
    docker_tag: str
    allowed_extensions: List[str]
    max_file_weight: int
    time_out: int
    resource_dir: str
    error_file_name: str
    log_level: str
    log_dir: str
    log_to_console: bool
    app_secret: str
    api_host: str
    api_port: int
    rpc_port: int
    filesystem_database_dir: str
    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
    postgres_max_connections: int
    postgres_min_connections: int
