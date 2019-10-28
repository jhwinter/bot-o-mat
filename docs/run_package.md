# Executing bot-o-mat as a package

## Setup

Follow the setup instructions for Local Setup

### How to create Robots to execute assigned tasks

`bot_o_mat {-r | --robot} {robot_type} {robot_name}`

#### Example

```shell
bot_o_mat -r Bipedal Bender -r Arachnid Spidey -r Radial BB8
```

### How to display the leaderboard

`bot_o_mat leaderboard`

### Help

`bot_o_mat --help`

#### Note

The database and leaderboard files will get created within the package directory (which is located with your python executable). So, it may be difficult to find
