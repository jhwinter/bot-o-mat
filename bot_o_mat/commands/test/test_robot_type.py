"""[summary]
"""

import contextlib
import pathlib
import unittest

import bot_o_mat.utils.db_connect
import bot_o_mat.commands.robot_type


data_dir: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "data"
).resolve()
connection = bot_o_mat.utils.db_connect.open_db(path=data_dir)


class TestRobotType(unittest.TestCase):
    """Class for unit testing robot_type module

    :param unittest: [description]
    :type unittest: [type]
    """

    def test_get_robot_types(self):
        """[summary]
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = bot_o_mat.commands.robot_type.get_robot_types(
                cursor=cursor
            )

        self.assertIsInstance(result, list)

        [
            self.assertIsInstance(element, dict)
            for element in result
        ]

        self.assertGreaterEqual(len(result), 6)

    def test_robot_type_exists(
        self,
        robot_type: str = "Unipedal",
        expected_value: bool = True
    ):
        """[summary]
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = bot_o_mat.commands.robot_type.robot_type_exists(
                cursor=cursor,
                type=robot_type
            )

        self.assertEqual(result, expected_value)

    def test_robot_type_exists_fails(self):
        """[summary]
        """

        self.test_robot_type_exists(robot_type="asdfa", expected_value=False)

    def test_all_robot_types_succeed(self):
        """[summary]
        """

        with contextlib.closing(connection.cursor()) as cursor:
            robot_types: list = bot_o_mat.commands.robot_type.get_robot_types(
                cursor=cursor
            )
            [
                self.test_robot_type_exists(
                    robot_type=robot_type.get("id"),
                    expected_value=True
                )
                for robot_type in robot_types
            ]


if __name__ == "__main__":
    unittest.main()
    bot_o_mat.utils.db_connect.close_db(connection=connection)
