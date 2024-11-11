FROM linuxserver/swag

FROM linuxserver/swag

RUN apk update && apk add logrotate

# Copiar configuraciones de nginx y fail2ban desde la ruta relativa al contexto raíz
COPY .docker/nginx/dev/site-confs/default /config/nginx/site-confs/default
COPY .docker/nginx/dev/fail2ban/jail.local /config/fail2ban/jail.local
COPY .docker/nginx/dev/fail2ban/fail2ban-logrotate.conf /etc/logrotate.d/fail2ban

# Copiar el script de inicio desde la ubicación correcta
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /config/entrypoint.sh

# Establecer el script como entrypoint
ENTRYPOINT ["entrypoint.sh"]
