FROM nickgryg/alpine-pandas
ARG TZ="America/New_York"

RUN apk update && \
    apk upgrade && \
    apk add --no-cache sqlite

COPY ./ /app

WORKDIR /app

RUN pip install --upgrade pip && \
    python setup.py install && \
    python scripts/setup_db.py

VOLUME [ "/app/bot_o_mat/data" ]

ENTRYPOINT [ "python", "bot_o_mat/cli.py" ]
