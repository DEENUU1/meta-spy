FROM node:16 AS build

WORKDIR /app

COPY facebookspy/src/server/frontend/package*.json ./

RUN npm install

COPY facebookspy/src/server/frontend/ ./

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
