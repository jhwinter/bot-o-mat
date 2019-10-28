# Executing bot-o-mat via Docker

## Setup

### Build the container

`./build_container.{sh|bat}`

### How to create Robots to execute assigned tasks

```shell
docker run -it -v /path/to/bot_o_mat/data:/app/bot_o_mat/data jwinter/bot_o_mat -r {robot_type} {robot_name}
```

#### Example

```shell
docker run -it -v /path/to/bot_o_mat/data:/app/bot_o_mat/data jwinter/bot_o_mat -r Bipedal Bender -r Arachnid Spidey -r Radial BB8
```

### Displaying the leaderboard

```shell
docker run -it -v /path/to/bot-o-mat/bot_o_mat/data:/app/bot_o_mat/data jwinter/bot_o_mat leaderboard
```

#### Help

You can get help like so

```shell
docker run -it -v /path/to/bot-o-mat/bot_o_mat/data:/app/bot_o_mat/data jwinter/bot_o_mat --help

```
