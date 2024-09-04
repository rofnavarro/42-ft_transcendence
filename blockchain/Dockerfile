FROM node:latest

WORKDIR /app/hardhat

COPY /hardhat .

RUN apt-get update

RUN npm install

RUN npx hardhat compile

CMD ["npx", "hardhat", "node"]