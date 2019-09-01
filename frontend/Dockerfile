FROM node:10-alpine
RUN apk update && apk add --no-cache nginx
RUN mkdir -p /run/nginx
RUN mkdir -p /usr/share/nginx/html
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build
RUN cp -r /app/dist/ngapp/* /usr/share/nginx/html/
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
