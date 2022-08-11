FROM node:13.12.0-alpine as build-stage
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build


FROM nginx:1.8-alpine
COPY --from=build-stage /app/build /usr/share/nginx/html
RUN chown nginx.nginx /usr/share/nginx/html/ -R
EXPOSE 80