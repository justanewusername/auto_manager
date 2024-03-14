FROM node:14.9
 
WORKDIR /app/frontend
COPY package*.json ./

RUN npm install
 
COPY . /app/frontend
EXPOSE 3000

CMD [ "npm", "start" ]