"""[summary]

:return: [description]
:rtype: [type]
"""

import sqlite3
import typing


def get_robot_types(cursor: sqlite3.Cursor) -> typing.List[dict]:
    """Gets all robot types from the db

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :return: [description]
    :rtype: typing.List[dict]
    """

    return cursor.execute(
        "SELECT id, name FROM robot_type"
    ).fetchall()


def robot_type_exists(cursor: sqlite3.Cursor, type: str) -> bool:
    """Determines whether or not the robot type exists in the db

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :param type: [description]
    :type type: str
    :return: [description]
    :rtype: bool
    """

    type_exists: int = cursor.execute(
        '''SELECT COUNT(*)
        FROM robot_type
        WHERE id = :id''',
        {"id": type.upper()}
    ).fetchone().get("COUNT(*)")

    return True if type_exists == 1 else False
