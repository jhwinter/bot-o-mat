"""[summary]
"""

import contextlib
import pathlib
import unittest

import bot_o_mat.utils.db_connect
import scripts.setup_db


data_dir: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "data"
).resolve()
connection = bot_o_mat.utils.db_connect.open_db(path=data_dir)


class TestSetupDB(unittest.TestCase):
    """Class for unit testing setup_db script

    :param unittest: [description]
    :type unittest: [type]
    """

    def test_initialize_robot_type_table(self):
        """Test 1
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = scripts.setup_db.initialize_robot_type_table(
                cursor=cursor
            )

        self.assertEqual(result, True)

    def test_initialize_task_table(self):
        """Test 2
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = scripts.setup_db.initialize_task_table(cursor=cursor)

        self.assertEqual(result, True)

    def test_create_robot_table(self):
        """Test 3
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = scripts.setup_db.create_robot_table(cursor=cursor)

        self.assertEqual(result, True)

    def test_create_leaderboard_table(self):
        """Test 4
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = scripts.setup_db.create_leaderboard_table(cursor=cursor)

        self.assertEqual(result, True)

    def test_main(self):
        """this test assumes a non-existent database
        """
        pass


if __name__ == "__main__":
    unittest.main()
    bot_o_mat.utils.db_connect.close_db(connection=connection)
