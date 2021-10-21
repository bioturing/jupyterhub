FROM python:3

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 


ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}

COPY . ./app
RUN chown -R jovyan:jovyan /app

EXPOSE 8000
USER jovyan
WORKDIR /app

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0"]
