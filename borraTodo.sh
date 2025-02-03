#!/bin/bash

#borra todas las imagenes sin etiqueta
docker image prune -a

#borra todos los contenedores detenidos
docker container prune

#borra todos los volumenes no utilizados
docker volume prune

#borra todas las imagenes, contenedores y volumenes no utilizados
docker system prune

#elimima el cahce de todas las imagenes
docker builder prune
