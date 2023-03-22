# Section1: Base Image
FROM python:3.9

# Section2: Python Interpreter Flags

# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application (e.g. django logs)
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

# Section3: Compiler and OS libraries
ENV TZ Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo $TZ > /etc/timezone
RUN sed -i -e 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list
RUN apt update && apt install -y locales tzdata
RUN dpkg-reconfigure -f noninteractive tzdata
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.UTF-8

# Section4: Project libraries and User Creation
COPY ./requirements.txt /tmp/requirements.txt

RUN pip3 install -U -i https://mirrors.aliyun.com/pypi/simple/ pip \
    && pip3 install -U -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

# Section5: Code and User Setup
RUN addgroup --system app && adduser --system --group app
WORKDIR /app

COPY ./app ./app
# COPY ./alembic.ini ./alembic.ini
COPY ./docker /usr/local/bin/

RUN chmod +x /usr/local/bin/*.sh

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
# Switch to a non-root user
USER app

# ENV PYTHONPATH /app

# Docker Run Checks and Configurations
ENTRYPOINT ["entrypoint.sh"]
CMD ["start.sh"]
