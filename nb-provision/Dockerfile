FROM continuumio/miniconda3:4.10.3

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG HOME=/home/jovyan

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}

COPY environment.yaml environment.yaml
RUN conda env create --name nb_provision -f environment.yaml

COPY . ./app

COPY condarc /opt/condarc
RUN chown jovyan:jovyan /opt/condarc
RUN chown -R jovyan:jovyan /app
RUN chown  jovyan:jovyan /opt/conda/envs/nb_provision

USER jovyan

EXPOSE 8000
WORKDIR /app

CMD ["conda", "run", "--no-capture-output", "-n", "nb_provision", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0"]
