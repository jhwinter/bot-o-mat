#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name="bot_o_mat",
    version="1.0.0",
    packages=setuptools.find_packages(where="./"),
    package_dir={"bot_o_mat": "bot_o_mat"},
    include_package_data=True,
    package_data={"bot_o_mat": ["data/*.db"]},
    scripts=["scripts/setup_db.py"],
    install_requires=[
        "Click",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "bot_o_mat = bot_o_mat.cli:main"
        ]
    }
)
