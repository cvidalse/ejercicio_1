#!/usr/bin/env bash
IMAGE_NAME="modelo-prediccion-mp"
CONTAINER_NAME="modelo-prediccion-mp"

echo "(1/8) > Deteniendo contenedor ${CONTAINER_NAME}"
docker stop ${CONTAINER_NAME}

echo "(2/8) > Eliminando contenedor ${CONTAINER_NAME}"
docker rm -f ${CONTAINER_NAME}

echo "(3/8) > Eliminando imagen ${IMAGE_NAME}"
docker images -a | grep "${IMAGE_NAME}" | awk '{print $3}' | xargs docker rmi

echo "(4/8) > Cargando imagen ${IMAGE_NAME}"
docker load <"$1"

echo "(5/8) > Eliminando archivo de imagen ${1}"
rm -rf "$1"

echo "(6/8) > Creando contenedor ${CONTAINER_NAME} con imagen ${IMAGE_NAME}:$2"
docker create -p 8091:8090 --restart always --name ${CONTAINER_NAME} ${IMAGE_NAME}:"$2"

echo "(7/8) > Iniciando contenedor ${CONTAINER_NAME}"
docker start ${CONTAINER_NAME}

echo "(8/8) > Comprobando Inicio del contenedor ${CONTAINER_NAME}"
docker ps -f NAME=${CONTAINER_NAME}

echo "> Finalizado"