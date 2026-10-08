FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN chmod +x scripts/docker-entrypoint.sh

EXPOSE 5173

CMD ["/bin/sh", "/app/scripts/docker-entrypoint.sh"]
