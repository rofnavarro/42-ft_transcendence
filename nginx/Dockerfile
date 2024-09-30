FROM 	nginx

RUN		apt update -y && \
		apt full-upgrade -y && \
		apt install nginx openssl -y && \
		apt clean

RUN		mkdir -p /etc/nginx/ssl/private /etc/nginx/ssl/certs

RUN 	openssl req -batch -x509 -sha256 -nodes -newkey rsa:2048 -days 365 \
		-keyout /etc/nginx/ssl/private/localhost.key \
		-out /etc/nginx/ssl/certs/localhost.crt

COPY	./nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

RUN		mkdir -p /var/www/html

COPY	./static /var/www/html/static
COPY	./media /var/www/html/media

RUN		chmod 755 /var/www/html

RUN		chmod 644 /etc/nginx/ssl/certs/localhost.crt
RUN		chmod 644 /etc/nginx/ssl/private/localhost.key


RUN		chown -R www-data:www-data /var/www/html

CMD		[ "nginx", "-g", "daemon off;" ]