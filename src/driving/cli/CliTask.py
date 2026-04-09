import json
import os

import click

from src.domain.error.WrapException import wrap_exception
from src.domain.mapper.MapperTask import MapperTask
from src.domain.model.task.Task import Task
from src.domain.model.task.TaskHeader import TaskHeader
from src.driven.app.AppTask import AppTask
from src.driving.config.BuilderBootstrap import BuilderBootstrap

ASSET_DIR = "db"
TEMPLATE_DIR = "tmp"
TASK_NEW_FILE_NAME = "new_task.json"
TASK_UPDATE_FILE_NAME = "update_task.json"
ASSET_TEMPLATE_PATH = os.path.join(ASSET_DIR, TEMPLATE_DIR)


class CliTask:
    def __init__(self):
        self.bootstrap = BuilderBootstrap.load_bootstrap()
        self.app_task = AppTask(self.bootstrap)
        os.makedirs(ASSET_TEMPLATE_PATH, exist_ok=True)

    @wrap_exception
    def get_template(self, user_wrote_id: str):
        template_dict = Task.get_template(user_wrote_id).as_dict()
        file_path = self._get_path(is_new=True)
        self._save_json(template_dict, file_path)
        click.echo(f"File saved: {file_path}")
        click.launch(file_path)
        click.echo(f"Opening {file_path}...")

    @wrap_exception
    def create_base(self, title, user_wrote_id):
        task = MapperTask.args_to_model(title=title, user_wrote_id=user_wrote_id)
        self.app_task.create(task, user_wrote_id)
        click.echo(f"Task '{task.title}' created successfully!")

    @wrap_exception
    def fetch_headers(self):
        tasks = self.app_task.fetch_headers()
        if not tasks:
            click.echo("No tasks found.")
            return

        headers = TaskHeader._fields
        header_line = f" | {' | '.join(headers)} |"
        click.echo(header_line)
        click.echo("-" * len(header_line))

        for task in tasks:
            row = [str(getattr(task, h, "")) for h in headers]
            click.echo(f" | {' | '.join(row)} |")

    @wrap_exception
    def fetch_by_id(self, task_id: str):
        task = self.app_task.fetch_by_id(task_id)
        if not task:
            click.echo("No current_task found.")
            return

        file_path = self._get_path(is_new=False)
        self._save_json(task.as_dict(), file_path)
        click.launch(file_path)
        click.echo(f"Opening {file_path}...")

    @wrap_exception
    def create(self, user_wrote_id: str):
        file_path = self._get_path(is_new=True)
        if self._file_missing(file_path, "get_template"):
            return

        data = self._load_json(file_path)
        self.app_task.create(MapperTask.dict_to_model(data), user_wrote_id)
        click.echo(f"Task created successfully from {file_path}!")

    @wrap_exception
    def update(self, user_wrote_id: str):
        file_path = self._get_path(is_new=False)
        if self._file_missing(file_path, "fetch_by_id"):
            return

        data = self._load_json(file_path)
        self.app_task.update(MapperTask.dict_to_model(data), user_wrote_id)
        click.echo(f"Task updated successfully from {file_path}!")

    def _get_path(self, is_new: bool) -> str:
        file_name = TASK_NEW_FILE_NAME if is_new else TASK_UPDATE_FILE_NAME
        return os.path.join(ASSET_TEMPLATE_PATH, file_name)

    def _save_json(self, data: dict, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _load_json(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _file_missing(self, path: str, suggestion: str) -> bool:
        if not os.path.exists(path):
            click.echo(
                f"Error: File not found at {path}. Please run {suggestion} first.",
                err=True,
            )
            return True
        return False


def make_task_cli() -> click.Group:
    cli_task = CliTask()
    parent_cmd = click.Group()

    commands = [
        click.Command(
            name="get_template",
            callback=cli_task.get_template,
            help="Get current_task template.",
            params=[
                click.Option(["--user_wrote_id"], default="0004"),
            ],
        ),
        click.Command(
            name="create",
            callback=cli_task.create,
            help="Create current_task from file.",
            params=[
                click.Option(["--user_wrote_id"], default="0004"),
            ],
        ),
        click.Command(
            name="create_base",
            callback=cli_task.create_base,
            help="Create base current_task.",
            params=[
                click.Option(["--title"], prompt="Title"),
                click.Option(["--user_wrote_id"], default="0004"),
            ],
        ),
        click.Command(
            name="fetch_headers", callback=cli_task.fetch_headers, help="Fetch headers."
        ),
        click.Command(
            name="fetch_by_id",
            callback=cli_task.fetch_by_id,
            help="Fetch by ID.",
            params=[click.Option(["--task_id"], prompt="Identifier")],
        ),
        click.Command(
            name="update",
            callback=cli_task.update,
            help="Update current_task from file.",
            params=[
                click.Option(["--user_wrote_id"], default="0004"),
            ],
        ),
    ]

    for cmd in commands:
        parent_cmd.add_command(cmd)

    return parent_cmd
