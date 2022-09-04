# Use an official node runtime as a parent image
FROM node:16.17.0-alpine

WORKDIR /app/

COPY package.json /app/

RUN npm install

COPY . /app/

EXPOSE 3000

RUN npm start