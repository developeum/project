FROM node:alpine AS builder   

WORKDIR /app
COPY WEB-client .

RUN npm install
RUN npm run ng -- build --prod

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist/WEB-client /var/www/html
