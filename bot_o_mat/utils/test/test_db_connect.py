"""[summary]
"""

import pathlib
import sqlite3
import unittest

import bot_o_mat.utils.db_connect


data_dir: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "data"
).resolve()


class TestDBConnect(unittest.TestCase):
    """Class for unit testing db_connect module

    :param unittest: [description]
    :type unittest: [type]
    """

    def test_open_db(self):
        """[summary]
        """

        connection = bot_o_mat.utils.db_connect.open_db(path=data_dir)

        self.assertIsInstance(connection, sqlite3.Connection)
        self.assertIsInstance(connection.cursor(), sqlite3.Cursor)

    def test_close_db(self):
        """[summary]
        """

        connection = bot_o_mat.utils.db_connect.open_db(path=data_dir)
        self.assertIsInstance(connection, sqlite3.Connection)

        bot_o_mat.utils.db_connect.close_db(connection=connection)
        self.assertNotEqual(connection, sqlite3.Connection)


if __name__ == "__main__":
    unittest.main()
