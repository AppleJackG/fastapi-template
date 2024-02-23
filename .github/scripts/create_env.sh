#!/bin/bash

echo MODE=${{ vars.MODE }} > .env
echo LOG_LEVEL=${{ vars.LOG_LEVEL }} >> .env
echo POSTGRES_DB=${{ secrets.POSTGRES_DB }} >> .env
echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env
echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env
echo POSTGRES_HOST=${{ secrets.POSTGRES_HOST }} >> .env
echo POSTGRES_PORT=${{ secrets.POSTGRES_PORT }} >> .env
echo TEST_POSTGRES_DB=${{ secrets.TEST_POSTGRES_DB }} >> .env
echo TEST_POSTGRES_USER=${{ secrets.TEST_POSTGRES_USER }} >> .env
echo TEST_POSTGRES_PASSWORD=${{ secrets.TEST_POSTGRES_PASSWORD }} >> .env
echo TEST_POSTGRES_HOST=${{ secrets.TEST_POSTGRES_HOST }} >> .env
echo TEST_POSTGRES_PORT=${{ secrets.TEST_POSTGRES_PORT }} >> .env
echo SECRET_KEY=${{ secrets.SECRET_KEY }} >> .env
echo PUBLIC_KEY=${{ secrets.PUBLIC_KEY }} >> .env
echo ADMIN_SECRET_KEY=${{ secrets.ADMIN_SECRET_KEY }} >> .env
echo ALGORITHM=${{ secrets.ALGORITHM }} >> .env
echo CORS_HEADERS=${{ vars.CORS_HEADERS }} >> .env
echo CORS_ORIGINS=${{ vars.CORS_ORIGINS }} >> .env
echo CORS_METHODS=${{ vars.CORS_METHODS }} >> .env
echo JUPYTER_PLATFORM_DIRS=${{ vars.JUPYTER_PLATFORM_DIRS }} >> .env
