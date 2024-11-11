FROM linuxserver/swag

FROM linuxserver/swag

RUN apk update && apk add logrotate

COPY .docker/nginx/dev/site-confs/default /config/nginx/site-confs/default
COPY .docker/nginx/dev/fail2ban/jail.local /config/fail2ban/jail.local
COPY .docker/nginx/dev/fail2ban/fail2ban-logrotate.conf /etc/logrotate.d/fail2ban

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
