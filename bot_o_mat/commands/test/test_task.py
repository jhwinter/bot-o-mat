"""[summary]
"""

import contextlib
import pathlib
import unittest

import bot_o_mat.utils.db_connect
import bot_o_mat.commands.task


data_dir: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "data"
).resolve()
connection = bot_o_mat.utils.db_connect.open_db(path=data_dir)


class TestTask(unittest.TestCase):
    """Class for unit testing task module

    :param unittest: [description]
    :type unittest: [type]
    """

    def test_get_tasks(self):
        """[summary]
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result: list = bot_o_mat.commands.task.get_tasks(cursor=cursor)

        self.assertIsInstance(result, list)

        [
            self.assertIsInstance(element, dict)
            for element in result
        ]

        self.assertGreaterEqual(len(result), 16)

    def test_get_random_tasks(self):
        """[summary]
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result: list = bot_o_mat.commands.task.get_random_tasks(
                cursor=cursor
            )

        self.assertIsInstance(result, list)

        [
            self.assertIsInstance(element, dict)
            for element in result
        ]

        self.assertEqual(len(result), 5)


if __name__ == "__main__":
    unittest.main()
    bot_o_mat.utils.db_connect.close_db(connection=connection)
