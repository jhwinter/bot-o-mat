"""[summary]
"""

import pathlib
import unittest

import click.testing

import bot_o_mat.cli


data_dir: pathlib.Path = pathlib.Path(__file__).parent.parent.joinpath(
    "data"
).resolve()
connection = bot_o_mat.utils.db_connect.open_db(path=data_dir)


class TestCLI(unittest.TestCase):
    """Class for unit testing cli module

    :param unittest: [description]
    :type unittest: [type]
    """

    def test_create_robot_and_execute_tasks(self):
        """[summary]
        """

        pass

    def test_display_robot_types(self):
        """[summary]
        """

        pass

    def test_main():
        """[summary]
        """

        runner = click.testing.CliRunner()
        result = runner.invoke(
            bot_o_mat.cli.main,
            ["Unipedal", "Larry"]
        )

        assert result.exit_code == 0
        assert result.output == ""

    def test_leaderboard():
        """[summary]
        """

        pass


if __name__ == "__main__":
    unittest.main()
    bot_o_mat.utils.db_connect.close_db(connection=connection)
