FROM linuxserver/swag

RUN apt-get update && apt-get install -y logrotate
COPY site-confs/default /config/nginx/site-confs/default
COPY fail2ban/jail.local /config/fail2ban/jail.local
COPY fail2ban/fail2ban-logrotate.conf /etc/logrotate.d/fail2ban
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
