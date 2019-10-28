@echo off

docker build \
    --file ./Dockerfile \
    --tag jwinter/bot_o_mat:latest \
    ./
