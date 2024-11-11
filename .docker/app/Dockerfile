FROM rudodeveloper/python:3.12.0
RUN apt-get update && apt-get install -y supervisor
RUN pip install poetry
RUN mkdir /code
WORKDIR /code
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-interaction --no-ansi --no-root
COPY . /code/
RUN chmod +x /code/start.sh
EXPOSE 8000 8001
CMD ["/code/start.sh"]