FROM nginx:latest

RUN apt-get update && apt-get install -y openssl

RUN rm -f /etc/nginx/conf.d/default.conf
RUN mkdir -p /home/web/www
 
RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048 && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/certs/self.key -out /etc/ssl/certs/self.crt \
    -subj "/C=UA/ST=Kyiv/L=Khreshchatyk/O=Azzrael Code/OU=Org/CN=azz.code"

COPY nginx.conf /etc/nginx/conf.d
COPY ssl-params.conf /etc/nginx/ssl-params.conf
COPY proxy_params.conf /etc/nginx/proxy_params.conf