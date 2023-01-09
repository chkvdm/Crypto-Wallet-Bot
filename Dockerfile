FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "--app", "run", "run", "--host", "0.0.0.0"]


# FROM python:3

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]







# FROM python:3.10

# # RUN adduser -D appuser

# WORKDIR .
# COPY . .

# ENV FLASK_APP run.py
# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1
# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# # Install & use pipenv
# COPY Pipfile Pipfile.lock
# RUN python -m pip install --upgrade pip
# RUN pip install pipenv
# RUN pipenv install
# EXPOSE 5000

# # RUN chown -R appuser /crypto-sandbox-api
# # USER appuser
# ENTRYPOINT ["python"]
# CMD ["run.py"]

# # start by pulling the python image
# FROM python:3.8-alpine
# # copy the requirements file into the image
# COPY ./requirements.txt /app/requirements.txt
# # switch working directory
# WORKDIR /app
# # install the dependencies and packages in the requirements file
# RUN pip install -r requirements.txt
# # copy every content from the local file to the image
# COPY . /app
# # configure the container to run in an executed manner
# ENTRYPOINT ["python"]
# CMD ["app.py"]

# FROM python:3.10
# WORKDIR /app
# COPY . .
# RUN pip install pipenv
# RUN pipenv install
# ENTRYPOINT ["flask"]
# CMD ["run"]



# FROM python:3.6-alpine

# RUN adduser -D microblog

# WORKDIR /home/microblog

# COPY requirements.txt requirements.txt
# RUN python -m venv venv
# RUN venv/bin/pip install -r requirements.txt
# RUN venv/bin/pip install gunicorn

# COPY app app
# COPY migrations migrations
# COPY microblog.py config.py boot.sh ./
# RUN chmod +x boot.sh

# ENV FLASK_APP microblog.py

# RUN chown -R microblog:microblog ./
# USER microblog

# EXPOSE 5000
# ENTRYPOINT ["./boot.sh"]



# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.9-slim

# ENV VAR1=10

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# Install & use pipenv
# COPY Pipfile Pipfile.lock ./
# RUN python -m pip install --upgrade pip
# RUN pip install pipenv && pipenv install --dev --system --deploy

# WORKDIR /app
# COPY . /app

# # Creates a non-root user and adds permission to access the /app folder
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "main.py"]





# # Выкачиваем из dockerhub образ с python версии 3.9
# FROM python:3.9
# # Устанавливаем рабочую директорию для проекта в контейнере
# WORKDIR /backend
# # Скачиваем/обновляем необходимые библиотеки для проекта 
# COPY requirements.txt /backend
# RUN pip3 install --upgrade pip -r requirements.txt
# # |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# # в рабочую директорию контейнера
# COPY . /backend
# # Устанавливаем порт, который будет использоваться для сервера
# EXPOSE 5000