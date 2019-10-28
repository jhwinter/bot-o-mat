"""[summary]

:raises ValueError: [description]
:return: [description]
:rtype: [type]
"""

import json
import sqlite3
import time

import bot_o_mat.utils.db_connect
import bot_o_mat.commands.robot_type
import bot_o_mat.commands.task


def get_robot(cursor: sqlite3.Cursor, name: str) -> dict:
    """Gets robot row from db

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :param name: [description]
    :type name: str
    :param type: [description]
    :type type: dict
    """

    return cursor.execute(
        '''SELECT id, name, robot_type_id
        FROM robot
        WHERE name = :name''',
        {"name": name}
    ).fetchone()


def _create_robot(cursor: sqlite3.Cursor, name: str, type: str) -> int:
    """Creates a robot with given 'name' and 'type' in the 'robot'
    and 'leaderboard' tables in the db

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :param name: [description]
    :type name: str
    :param type: [description]
    :type type: str
    :return: id of the most recently created robot
    :rtype: int
    """

    cursor.execute(
        '''INSERT INTO robot(name, robot_type_id)
        VALUES (:name, :robot_type_id)''',
        {"name": name, "robot_type_id": type.upper()}
    )

    robot_id: int = cursor.lastrowid
    cursor.execute(
        '''INSERT INTO leaderboard(robot_id)
        VALUES (:robot_id)''',
        {"robot_id": robot_id}
    )
    try:
        cursor.connection.commit()
    except Exception as err:
        print({"err": err}, flush=True)
        cursor.connection.rollback()

    return robot_id


def create_unique_robot(cursor: sqlite3.Cursor, name: str, type: str) -> int:
    """Creates a unique robot given 'name' and 'type' in the 'robot'
    and 'leaderboard' tables in the db

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :param name: [description]
    :type name: [type]
    :return: returns the robot's id if the robot was created, 0 otherwise
    :rtype: int
    """

    preexisting_robot: dict = get_robot(
        cursor=cursor,
        name=name
    )

    return _create_robot(
        cursor=cursor,
        name=name,
        type=type
    ) if not preexisting_robot else preexisting_robot.get("id")


def _update_leaderboard(
    cursor: sqlite3.Cursor,
    robot_id: int,
    task_id: int
) -> bool:
    """Increments the value in the column corresponding to the task_id

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :param task_id: [description]
    :type task_id: [type]
    :return: [description]
    :rtype: [type]
    """

    leaderboard_column: str = f"task_{task_id}_score"
    cursor.execute(
        f'''UPDATE leaderboard
        SET {leaderboard_column} = {leaderboard_column} + 1
        WHERE robot_id = :robot_id''',
        {"robot_id": robot_id}
    )
    cursor.connection.commit()

    return True


class Robot(object):
    """[summary]

    :param object: [description]
    :type object: [type]
    :raises ValueError: [description]
    :return: [description]
    :rtype: [type]
    """

    def __init__(self, cursor: sqlite3.Cursor, name: str, type: str):
        """[summary]

        :param cursor: [description]
        :type cursor: sqlite3.Cursor
        :param name: [description]
        :type name: str
        :param type: [description]
        :type type: str
        :raises ValueError: [description]
        """

        self._cursor = cursor

        upper_type: str = type.strip().upper()
        valid_type: bool = bot_o_mat.commands.robot_type.robot_type_exists(
            cursor=self._cursor,
            type=upper_type
        )
        if not valid_type:
            raise ValueError(f"Robot Type '{upper_type}' does not exist")

        if valid_type:
            self._id = 0
            self._name = name.strip()
            self._type = upper_type
            self._task_list = []

    def create_this_unique_robot(self) -> int:
        """Creates this instance of robot in the db

        :return: [description]
        :rtype: int
        """

        robot_id: int = create_unique_robot(
            cursor=self._cursor,
            name=self._name,
            type=self._type
        )
        self._id = robot_id

        return self._id

    def __complete_task(self, eta) -> bool:
        """Completes the given task

        :param eta: amount of seconds required to complete the task
        :type eta: float
        :return: [description]
        :rtype: bool
        """

        time.sleep(eta)

        return True

    def __do_complete_task(self, task: dict) -> bool:
        """Completes given task and removes it from the list

        :param task: [description]
        :type task: dict
        :return: True if the task was completed, False otherwise
        :rtype: bool
        """

        def milliseconds_to_seconds(ms: int): return ms / 1000

        task_eta = milliseconds_to_seconds(ms=task.get("eta"))
        task_robot_type = task.get("robot_type")
        task_description = task.get("description")

        if task_robot_type != "" and task_robot_type != self._type:
            print(
                f"\n{self._name} the {self._type} Robot",
                f"cannot {task_description}"
            )
            self._task_list.remove(task)

            return False

        print(
            f"\n{self}",
            f"\nTask Description: {task_description}",
            f"\nTask ETA: {task_eta} seconds"
        )
        self.__complete_task(eta=task_eta)
        _update_leaderboard(
            cursor=self._cursor,
            robot_id=self._id,
            task_id=task.get("id")
        )
        self._task_list.remove(task)
        print(f"\n{task} removed from Task List")

        return True

    def do_complete_tasks(self) -> list:
        """Completes a list of random tasks

        Creating a copy of the task list was necessary because the
        index for the next item in the list would be inaccurate due
        to the list changing in size after every completed task

        :return: [description]
        :rtype: list
        """

        local_task_list = bot_o_mat.commands.task.get_random_tasks(
            cursor=self._cursor
        )
        # assign self.task_list to a copy of the local task list
        self._task_list = list(local_task_list)
        print(f"\n{self}")

        return [
            self.__do_complete_task(task=task)
            for task in local_task_list
        ]

    def __repr__(self) -> str:
        """Representation of this Robot instance

        :return: a JSON string of this Robot instance
        :rtype: str
        """

        return json.dumps(
            {
                "Robot": {
                    "id": self._id,
                    "name": self._name,
                    "type": self._type,
                    "task_list": self._task_list
                }
            }
        )
