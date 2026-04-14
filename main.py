from src.driving.cli.CliTask import CliTask

if __name__ == "__main__":
    command_group = CliTask.make_task_cli()
    command_group()
