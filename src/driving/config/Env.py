import os

from src.domain.model.ModelEnv import ModelEnv


class Env:
    @staticmethod
    def load_env() -> ModelEnv:
        return ModelEnv(
            api_base_version=os.getenv("API_BASE_VERSION", "1.0.0.0"),
            docker_name=os.getenv("DOCKER_NAME", "task"),
            docker_tag=os.getenv("DOCKER_TAG", "test"),
            allowed_extensions=os.getenv("ALLOWED_EXTENSIONS", "pdf,jpg,png").split(
                ","
            ),
            max_file_weight=int(os.getenv("MAX_FILE_WEIGHT", "16000")),
            time_out=int(os.getenv("TIME_OUT", "600")),
            app_secret=os.getenv(
                "APP_SECRET",
                "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf",
            ),
            api_host=os.getenv("API_HOST", "127.0.0.1"),
            api_port=int(os.getenv("API_PORT", "5000")),
            rpc_port=int(os.getenv("RPC_PORT", "50051")),
            postgres_host=os.getenv("POSTGRES_HOST", "172.17.0.3"),
            postgres_user=os.getenv("POSTGRES_USER", "postgres"),
            postgres_password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            postgres_db=os.getenv("POSTGRES_DB", "task"),
            postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        )
