[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hLqvXyMi)

Please use a virtual environment. After cloning, run:
1. cd .\project-a-28\
2. py -m venv .venv
3. .venv\Scripts\activate
4. pip install django==5.1.6 whitenoise
5. python manage.py runserver

Your local database is SQLite, but there is a seperate, server-side database using PostgreSQL. If you want to use the server-side database on your local build, run:
$env:DATABASE_URL="postgres://u87mp92uopqaal:pf31c4371fa143258fec18cb4976521f082fcdda3d4a7f15b1068a7e7af3f3b3c@c8m0261h0c7idk.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcee73lo5rne93"

# Webpage
https://supplysite-20c1e0704260.herokuapp.com/menu/

