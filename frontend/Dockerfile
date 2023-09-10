FROM node:19.9-alpine
WORKDIR /app
COPY package.json ./
RUN yarn install --frozen-lockfile
COPY . .
EXPOSE 3000