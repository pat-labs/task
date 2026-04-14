import json
import os
from typing import List

import click

from src.domain.model.Task import Task
from src.domain.service.ServiceTask import ServiceTask
from src.driving.cli.mapper.MapperCliTask import MapperCliTask
from src.driving.cli.WrapException import wrap_exception
from src.driving.config.BuilderBootstrap import BuilderBootstrap

ASSET_DIR = "db"
TEMPLATE_DIR = "tmp"
TASK_NEW_FILE_NAME = "new_task.json"
TASK_UPDATE_FILE_NAME = "update_task.json"
ASSET_TEMPLATE_PATH = os.path.join(ASSET_DIR, TEMPLATE_DIR)


class CliTask:
    def __init__(self):
        self.bootstrap = BuilderBootstrap.load_bootstrap()
        self.service_task = ServiceTask(self.bootstrap)
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
        task = MapperCliTask.args_to_model(title=title, user_wrote_id=user_wrote_id)
        self.service_task.create(task, user_wrote_id)
        click.echo(f"Task '{task.title}' created successfully!")

    @wrap_exception
    def fetch_headers(self):
        tasks = self.service_task.fetch_headers()
        self.print_task_table(tasks)

    @wrap_exception
    def fetch_by_id(self, task_id: str):
        task = self.service_task.fetch_by_id(task_id)
        if not task:
            click.echo("No task found.")
            return

        file_path = self._get_path(is_new=False)
        self._save_json(task.as_dict(), file_path)
        click.launch(file_path)
        click.echo(f"Opening {file_path}...")

    @wrap_exception
    def fetch_by_param(self, key: str, value: str):
        tasks = self.service_task.fetch_by_param(key, value)
        self.print_task_table(tasks)

    @wrap_exception
    def create(self, user_wrote_id: str):
        file_path = self._get_path(is_new=True)
        if self._file_missing(file_path, "get_template"):
            return

        data = self._load_json(file_path)
        task = MapperCliTask.dict_to_model(data)
        self.service_task.create(task, user_wrote_id)
        click.echo(f"Task created successfully from {file_path}!")

    @wrap_exception
    def update(self, user_wrote_id: str):
        file_path = self._get_path(is_new=False)
        if self._file_missing(file_path, "fetch_by_id"):
            return

        data = self._load_json(file_path)
        task = MapperCliTask.dict_to_model(data)
        self.service_task.update(task, user_wrote_id)
        click.echo(f"Task updated successfully from {file_path}!")

    @staticmethod
    def print_task_md(task: List[Task]):
        pass

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

    @staticmethod
    def make_task_cli() -> click.Group:
        cli_task = CliTask()
        parent_cmd = click.Group()

        parent_cmd.add_command(
            click.Command(
                name="get_template",
                callback=cli_task.get_template,
                help="Generate a new task template JSON file.",
                params=[click.Option(["--user_wrote_id"], default="0004")],
            )
        )
        parent_cmd.add_command(
            click.Command(
                name="create",
                callback=cli_task.create,
                help="Create a task from the new_task.json file.",
                params=[click.Option(["--user_wrote_id"], default="0004")],
            )
        )
        parent_cmd.add_command(
            click.Command(
                name="create_base",
                callback=cli_task.create_base,
                help="Create a basic task with title.",
                params=[
                    click.Option(["--title"], prompt="Title"),
                    click.Option(["--user_wrote_id"], default="0004"),
                ],
            )
        )
        parent_cmd.add_command(
            click.Command(
                name="fetch_headers",
                callback=cli_task.fetch_headers,
                help="List summary headers for all tasks.",
            )
        )
        parent_cmd.add_command(
            click.Command(
                name="fetch_by_id",
                callback=cli_task.fetch_by_id,
                help="Fetch a full task by ID and save to update_task.json.",
                params=[click.Option(["--task_id"], prompt="Identifier")],
            )
        )
        parent_cmd.add_command(
            click.Command(
                name="fetch_by_param",
                callback=cli_task.fetch_by_param,
                help="Search tasks by title, status, or tag.",
                params=[
                    click.Option(
                        ["--key"],
                        type=click.Choice(["title", "status", "tag"]),
                        prompt="Search by",
                    ),
                    click.Option(["--value"], prompt="Search term"),
                ],
            )
        )
        parent_cmd.add_command(
            click.Command(
                name="update",
                callback=cli_task.update,
                help="Update an existing task from the update_task.json file.",
                params=[click.Option(["--user_wrote_id"], default="0004")],
            )
        )

        return parent_cmd
