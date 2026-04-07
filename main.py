from src.driven.cli.CliTask import make_task_cli

if __name__ == "__main__":
    command_group = make_task_cli()
    command_group()
