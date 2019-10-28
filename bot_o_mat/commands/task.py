"""[summary]

:return: [description]
:rtype: [type]
"""

import random
import sqlite3
import typing


def get_tasks(cursor: sqlite3.Cursor) -> typing.List[dict]:
    """Gets the tasks from the db

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :return: [description]
    :rtype: typing.List[dict]
    """

    return cursor.execute(
        "SELECT id, description, eta, robot_type FROM task"
    ).fetchall()


def get_random_tasks(cursor: sqlite3.Cursor) -> typing.List[dict]:
    """Gets 5 random tasks

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :return: [description]
    :rtype: typing.List[dict]
    """

    return random.sample(population=get_tasks(cursor=cursor), k=5)
