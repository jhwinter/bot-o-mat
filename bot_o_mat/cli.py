"""Main entrypoint for the cli application

:return: [description]
:rtype: [type]
"""

# std library
import concurrent.futures
import contextlib
import pathlib
import typing

# third party
import click
import pandas

# local imports
import bot_o_mat.commands.robot
import bot_o_mat.utils.db_connect
import scripts.setup_db


data_dir: pathlib.Path = pathlib.Path(__file__).parent.joinpath(
    "data"
).resolve()
database_file: pathlib.Path = data_dir.joinpath("bot_o_mat.db").resolve()
if not database_file.is_file():
    print("\nDatabase file not found. Creating it now.\n", flush=True)
    scripts.setup_db.main(path=data_dir)


def create_robot_and_execute_tasks(type: str, name: str) -> bool:
    """Creates a Robot and immediately assigns it tasks to complete

    :return: [description]
    :rtype: [type]
    """

    try:
        with contextlib.closing(
            bot_o_mat.utils.db_connect.open_db(
                path=data_dir
            )
        ) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                this_robot: bot_o_mat.commands.robot.Robot = bot_o_mat.commands.robot.Robot(
                    cursor=cursor,
                    type=type,
                    name=name
                )
                this_robot.create_this_unique_robot()
                this_robot.do_complete_tasks()

        return True
    except Exception as err:
        print(err, flush=True)
        return None


def display_robot_types():
    """display robot types to the user

    :return: [description]
    :rtype: [type]
    """

    with contextlib.closing(
        bot_o_mat.utils.db_connect.open_db(
            path=data_dir
        )
    ) as connection:
        robot_types: typing.List[dict] = bot_o_mat.commands.robot_type.get_robot_types(
            cursor=connection.cursor()
        )

    return "|".join(
        [robot_type.get("name") for robot_type in robot_types]
    )


def display_leaderboard():
    """displays and formats the data from the leaderboard table
    """

    # connection = bot_o_mat.utils.db_connect.open_db()
    with contextlib.closing(
        bot_o_mat.utils.db_connect.open_db(
            path=data_dir
        )
    ) as connection:
        tasks: list = connection.cursor().execute(
            "SELECT id, description FROM task"
        ).fetchall()
        task_ids: list = [task.get("id") for task in tasks]
        column_list: list = [
            f"leaderboard.task_{task_id}_score AS '{task.get('description')}'"
            for task_id, task in zip(task_ids, tasks)
        ]
        columns: str = ", ".join(column_list)

        query: str = f'''
        SELECT robot.name, robot_type.id AS robot_type, {columns}
        FROM leaderboard
        INNER JOIN robot ON leaderboard.robot_id = robot.id
        INNER JOIN robot_type ON robot.robot_type_id = robot_type.id
        '''
        leaderboard = pandas.read_sql_query(
            sql=query,
            con=connection,
            index_col="name"
        )

    leaderboard_file: pathlib.Path = data_dir.joinpath(
        "leaderboard.csv"
    ).resolve()
    leaderboard.to_csv(path_or_buf=leaderboard_file)
    print(leaderboard, flush=True)


@click.command()
@click.option(
    "--robot",
    "-r",
    type=(str, str),
    multiple=True,
    help=f"[{display_robot_types()}] robot_name"
)
@click.argument("leaderboard", nargs=-1)
def main(robot=None, leaderboard=None):
    """Main entrypoint for handling user input

    :param robot: tuple of strings for customizing robot
    :type robot: tuple
    :param leaderboard: argument to display the leaderboard
    :type leaderboard: None
    """
    if leaderboard:
        display_leaderboard()
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            [
                executor.submit(
                    create_robot_and_execute_tasks,
                    this_robot[0],
                    this_robot[1]
                )
                for this_robot in robot
            ]


if __name__ == "__main__":
    main()
