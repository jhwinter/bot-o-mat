"""[summary]

:return: [description]
:rtype: [type]
"""

import pathlib
import sqlite3


def open_db(
    path: pathlib.Path = pathlib.Path(__file__).parent.parent.joinpath(
        "data"
    ).resolve()
) -> sqlite3.Connection:
    """Opens a connection to the bot_o_mat.db file.
    Configures the row_factory to return a List[dict] instead of List[tuple].
    Returns the connection object

    :return: [description]
    :rtype: sqlite3.Connection
    """

    db_file: pathlib.Path = path.joinpath("bot_o_mat.db").resolve()
    connection: sqlite3.Connection = sqlite3.connect(database=db_file)
    # https://stackoverflow.com/a/49725294/12132366
    # this is used for changing the return type from tuple -> dict
    connection.row_factory = lambda c, row: {
        col[0]: row[index]
        for index, col in enumerate(c.description)
    }

    # must enable foreign_keys for each connection
    connection.cursor().execute("PRAGMA foreign_keys = 1")
    connection.commit()

    return connection


def close_db(connection: sqlite3.Connection) -> bool:
    """Closes the provided db connection object

    :param connection: [description]
    :type connection: sqlite3.Connection
    :return: [description]
    :rtype: bool
    """
    connection.close()
    return True
