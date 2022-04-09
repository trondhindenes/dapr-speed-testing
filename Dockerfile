FROM python:3.10-slim-buster as base
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip pipenv
COPY Pipfile .
COPY Pipfile.lock .

FROM base as dep
RUN pipenv install --system --deploy

FROM base as final
ENV PYTHONPATH="/usr/src/app:/usr/src/app/app"
COPY . .
COPY --from=dep /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=dep /usr/local/bin /usr/local/bin
CMD ["python", "app/runserver.py"]
