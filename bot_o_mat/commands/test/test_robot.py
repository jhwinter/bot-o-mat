"""[summary]
"""

import contextlib
import pathlib
import unittest

import bot_o_mat.utils.db_connect
import bot_o_mat.commands.robot
import bot_o_mat.commands.task


data_dir: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "data"
).resolve()
connection = bot_o_mat.utils.db_connect.open_db(path=data_dir)


class TestRobot(unittest.TestCase):
    """Class for unit testing robot module and Robot class

    :param unittest: [description]
    :type unittest: [type]
    """

    @staticmethod
    def helper__get_robot(name: str):
        with contextlib.closing(connection.cursor()) as cursor:
            result: dict = bot_o_mat.commands.robot.get_robot(
                cursor=cursor,
                name=name
            )

        return result

    @staticmethod
    def helper__create_robot(name: str, type: str):
        """[summary]

        :param name: [description]
        :type name: str
        :param type: [description]
        :type type: str
        :return: [description]
        :rtype: [type]
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = bot_o_mat.commands.robot._create_robot(
                cursor=cursor,
                name=name,
                type=type
            )

        return result

    @staticmethod
    def helper__create_unique_robot(name: str, type: str):
        """[summary]

        :param name: [description]
        :type name: str
        :param type: [description]
        :type type: str
        """

        with contextlib.closing(connection.cursor()) as cursor:
            result = bot_o_mat.commands.robot.create_unique_robot(
                cursor=cursor,
                name=name,
                type=type
            )

        return result

    def test__create_robot(self):
        """Test create robot
        This test assumes a freshly built database
        """

        name: str = "Larry"
        type: str = "Unipedal"
        result = self.helper__create_robot(name=name, type=type)

        self.assertGreater(result, 0)
        result = self.helper__get_robot(name=name)
        self.assertGreater(result.get("id"), 0)

    def test_create_unique_robot(self):
        """Test create unique robot
        This test assumes a freshly built database
        """

        name: str = "Barry"
        type: str = "Bipedal"
        robot_id = self.helper__create_unique_robot(name=name, type=type)

        self.assertGreater(robot_id, 0)
        result = self.helper__get_robot(name=name)
        self.assertGreater(result.get("id"), 0)

    def test_get_robot(self):
        """Test get robot
        This test assumes a freshly built database
        """

        name: str = "Kerry"
        type: str = "Quadrupedal"
        self.helper__create_unique_robot(name=name, type=type)
        result = self.helper__get_robot(name=name)

        self.assertIsInstance(result, dict)
        self.assertGreater(result.get("id"), 0)
        self.assertEqual(result.get("name"), name)
        self.assertEqual(result.get("robot_type_id"), type.upper())

    def test__update_leaderboard(self):
        """Test update leaderboard
        This test assumes a freshly built database
        """

        name: str = "Harry"
        type: str = "Arachnid"
        self.helper__create_unique_robot(name=name, type=type)

        robot: dict = self.helper__get_robot(name=name)

        with contextlib.closing(connection.cursor()) as cursor:
            tasks: list = bot_o_mat.commands.task.get_tasks(cursor=cursor)
            result = bot_o_mat.commands.robot._update_leaderboard(
                cursor=cursor,
                robot_id=robot.get("id"),
                task_id=tasks[0].get("id")
            )

        self.assertEqual(result, True)

    def test_robot_init(self):
        """Test initialize robot instance
        This test assumes a freshly built database
        """

        name: str = "Gary"
        type: str = "Radial"
        with contextlib.closing(connection.cursor()) as cursor:
            result = bot_o_mat.commands.robot.Robot(
                cursor=cursor,
                type=type,
                name=name
            )

        self.assertIsInstance(result, bot_o_mat.commands.robot.Robot)

        self.assertEqual(result._type, type.upper())
        self.assertNotEqual(result._type, type)

        self.assertEqual(result._name, name)

        self.assertEqual(result._task_list, [])

    def test_do_complete_tasks(self):
        """Test robot completes tasks
        This test assumes a freshly built database
        """

        name: str = "Terry"
        type: str = "Aeronautical"
        with contextlib.closing(connection.cursor()) as cursor:
            robot = bot_o_mat.commands.robot.Robot(
                cursor=cursor,
                type=type,
                name=name
            )
            robot.create_this_unique_robot()
            result: list = robot.do_complete_tasks()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        [
            self.assertIsInstance(element, bool)
            for element in result
        ]


if __name__ == "__main__":
    unittest.main()
    bot_o_mat.utils.db_connect.close_db(connection=connection)
