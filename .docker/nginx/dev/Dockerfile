# Dentro del Dockerfile de .docker/nginx/dev/
FROM linuxserver/swag

RUN apk update && apk add logrotate

# Copiar configuraciones de nginx y fail2ban
COPY site-confs/default /config/nginx/site-confs/default
COPY fail2ban/jail.local /config/fail2ban/jail.local
COPY fail2ban/fail2ban-logrotate.conf /etc/logrotate.d/fail2ban

# Copiar el script de inicio desde la ubicación correcta
COPY entrypoint.sh /config/entrypoint.sh
RUN chmod +x /config/entrypoint.sh

# Establecer el script como entrypoint
ENTRYPOINT ["/config/entrypoint.sh"]