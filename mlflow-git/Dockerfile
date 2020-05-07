FROM conda/miniconda3

USER root

#RUN mkdir /build_scripts
#WORKDIR /build_scripts
#COPY install_miniconda.sh /build_scripts
#RUN ./install_miniconda.sh

RUN apt update && apt install -y cron git-core

ENV PATH="/opt/conda/bin:${PATH}"
RUN conda install -c anaconda scikit-learn
RUN conda install -c conda-forge mlflow
RUN conda install -c anaconda flask
RUN conda install -c anaconda flask-cors
RUN conda install -c conda-forge python-crontab


RUN mkdir /mlflow/

COPY app/ /mlflow/app/
WORKDIR /mlflow/app

#RUN git clone $URL_GIT repositorio
#RUN git clone https://oauth2:ujGaAxaLqf6LXywK7s_G@gitlab.com/FabianMariqueo/wine-mlflow.git repositorio
COPY modelo/ /mlflow/app/modelo

RUN python3 services/Cron_service.py

RUN touch /var/log/cron.log

CMD python3 mlflow_run.py && python3 controller.py && cron && python3 Servicio_prediccion.py