FROM linuxserver/swag

RUN apk update && apk add logrotate
COPY site-confs/default /config/nginx/site-confs/default
COPY fail2ban/jail.local /config/fail2ban/jail.local
COPY fail2ban/fail2ban-logrotate.conf /etc/logrotate.d/fail2ban
COPY entrypoint.sh /config/entrypoint.sh
RUN ls -l /config
RUN chmod +x /config/entrypoint.sh
