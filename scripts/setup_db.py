#!/usr/bin/env python3
"""[summary]

:return: [description]
:rtype: [type]
"""

import pathlib
import sqlite3
import sys


def initialize_robot_type_table(cursor: sqlite3.Cursor) -> bool:
    """Creates and populates the robot_type table with default values

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :return: [description]
    :rtype: bool
    """

    def create() -> bool:
        """Create robot_type table

        :return: [description]
        :rtype: bool
        """

        cursor.execute(
            '''
            CREATE TABLE robot_type(
                id      TEXT    PRIMARY KEY NOT NULL,
                name    TEXT    UNIQUE NOT NULL
            );
            '''
        )
        cursor.connection.commit()
        return True

    def populate() -> bool:
        """Populate robot_type table

        :return: [description]
        :rtype: bool
        """

        robot_type_sequence: list = [
            ("UNIPEDAL", "Unipedal"),
            ("BIPEDAL", "Bipedal"),
            ("QUADRUPEDAL", "Quadrupedal"),
            ("ARACHNID", "Arachnid"),
            ("RADIAL", "Radial"),
            ("AERONAUTICAL", "Aeronautical")
        ]

        cursor.executemany(
            "INSERT INTO robot_type(id, name) VALUES (?, ?)",
            robot_type_sequence
        )
        cursor.connection.commit()
        return True

    if create() and populate():
        return True

    return False


def initialize_task_table(cursor: sqlite3.Cursor) -> bool:
    """Creates and populates the task table with default values

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :return: [description]
    :rtype: bool
    """

    def create() -> bool:
        """Create task table

        :return: [description]
        :rtype: bool
        """

        cursor.execute(
            '''
            CREATE TABLE task(
                id              INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,
                description     TEXT        UNIQUE NOT NULL,
                eta             INT         NOT NULL,
                robot_type      TEXT        NOT NULL DEFAULT ""
            );
            '''
        )
        cursor.connection.commit()
        return True

    def populate() -> bool:
        """Populate task table

        :return: [description]
        :rtype: bool
        """

        tasks: list = [
            {
                "description": "do the dishes",
                "eta": 1000
            },
            {
                "description": "sweep the house",
                "eta": 3000
            },
            {
                "description": "do the laundry",
                "eta": 10000
            },
            {
                "description": "take out the recycling",
                "eta": 4000
            },
            {
                "description": "make a sammich",
                "eta": 7000
            },
            {
                "description": "mow the lawn",
                "eta": 20000
            },
            {
                "description": "rake the leaves",
                "eta": 18000
            },
            {
                "description": "give the dog a bath",
                "eta": 14500
            },
            {
                "description": "bake some cookies",
                "eta": 8000
            },
            {
                "description": "wash the car",
                "eta": 20000
            }
        ]
        task_sequence: list = [
            (task.get("description"), task.get("eta"))
            for task in tasks
        ]

        cursor.executemany(
            "INSERT INTO task(description, eta) VALUES (?, ?)",
            task_sequence
        )
        cursor.connection.commit()
        return True

    def populate_type_specific_tasks() -> bool:
        """Populate task table with type-specific tasks

        :return: [description]
        :rtype: bool
        """

        tasks: list = [
            {
                "description": "hop on one leg",
                "eta": 3000,
                "robot_type": "UNIPEDAL"
            },
            {
                "description": "do jumping jacks",
                "eta": 10000,
                "robot_type": "BIPEDAL"
            },
            {
                "description": "outrun a dog",
                "eta": 5000,
                "robot_type": "QUADRUPEDAL"
            },
            {
                "description": "clean the ceiling",
                "eta": 20000,
                "robot_type": "ARACHNID"
            },
            {
                "description": "roll down the stairs",
                "eta": 7000,
                "robot_type": "RADIAL"
            },
            {
                "description": "collect water from the clouds",
                "eta": 20000,
                "robot_type": "AERONAUTICAL"
            }
        ]
        task_sequence: list = [
            (task.get("description"), task.get("eta"), task.get("robot_type"))
            for task in tasks
        ]

        cursor.executemany(
            "INSERT INTO task(description, eta, robot_type) VALUES (?, ?, ?)",
            task_sequence
        )
        cursor.connection.commit()
        return True

    if create() and populate() and populate_type_specific_tasks():
        return True

    return False


def create_robot_table(cursor: sqlite3.Cursor) -> bool:
    """Create robot table

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :return: [description]
    :rtype: bool
    """

    cursor.execute(
        '''
        CREATE TABLE robot(
            id                  INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,
            name                TEXT        UNIQUE NOT NULL,
            robot_type_id       TEXT         NOT NULL,
            FOREIGN KEY(robot_type_id)
                REFERENCES robot_type(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
        );
        '''
    )
    cursor.connection.commit()
    return True


def create_leaderboard_table(cursor: sqlite3.Cursor) -> bool:
    """Create leaderboard table

    :param cursor: [description]
    :type cursor: sqlite3.Cursor
    :return: [description]
    :rtype: bool
    """

    cursor.execute(
        '''
        CREATE TABLE leaderboard(
            id               INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,
            robot_id         INT         NOT NULL,
            task_1_score     INT         NOT NULL DEFAULT 0,
            task_2_score     INT         NOT NULL DEFAULT 0,
            task_3_score     INT         NOT NULL DEFAULT 0,
            task_4_score     INT         NOT NULL DEFAULT 0,
            task_5_score     INT         NOT NULL DEFAULT 0,
            task_6_score     INT         NOT NULL DEFAULT 0,
            task_7_score     INT         NOT NULL DEFAULT 0,
            task_8_score     INT         NOT NULL DEFAULT 0,
            task_9_score     INT         NOT NULL DEFAULT 0,
            task_10_score    INT         NOT NULL DEFAULT 0,
            task_11_score    INT         NOT NULL DEFAULT 0,
            task_12_score    INT         NOT NULL DEFAULT 0,
            task_13_score    INT         NOT NULL DEFAULT 0,
            task_14_score    INT         NOT NULL DEFAULT 0,
            task_15_score    INT         NOT NULL DEFAULT 0,
            task_16_score    INT         NOT NULL DEFAULT 0,
            FOREIGN KEY(robot_id)
                REFERENCES robot(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
        );
        '''
    )
    cursor.connection.commit()
    return True


def main(path: pathlib.Path = pathlib.Path(__file__).parent.parent.joinpath(
        "bot_o_mat",
        "data",
    ).resolve()
):
    """Create bot_o_mat.db if it does not already exist in bot_o_mat/data
    """

    database_file: pathlib.Path = path.joinpath("bot_o_mat.db").resolve()

    if not path.exists():
        path.mkdir(exist_ok=True)

    if not database_file.is_file():
        with sqlite3.connect(database_file) as connection:
            print("Opened connection to database successfully\n")

            # must enable foreign_keys for each connection
            connection.cursor().execute("PRAGMA foreign_keys = 1")
            connection.commit()

            if initialize_robot_type_table(connection.cursor()):
                print("robot type table created and populated")

            if initialize_task_table(connection.cursor()):
                print("task table created and populated")

            if create_robot_table(connection.cursor()):
                print("robot table created successfully")

            if create_leaderboard_table(connection.cursor()):
                print("leaderboard table created successfully")

        print(
            "\nClosed connection to database successfully",
            "\nSQLite Database successfully configured\n"
        )
        return True

    print(f"{database_file} already exists")


if __name__ == "__main__":
    main()
    sys.exit()
