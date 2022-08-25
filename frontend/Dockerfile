FROM node:13.12.0-alpine as build-stage
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build


FROM nginx:1.23.1-alpine
COPY --from=build-stage /app/build /usr/share/nginx/html
COPY --from=build-stage /app/docs /usr/share/nginx/html/api/docs/
ENTRYPOINT ["nginx", "-g", "daemon off;"]