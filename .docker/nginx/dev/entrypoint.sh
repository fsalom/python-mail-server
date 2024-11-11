#!/bin/bash

cp /config/fail2ban-logrotate.conf /etc/logrotate.d/fail2ban
service fail2ban start
while true; do
    logrotate /etc/logrotate.d/fail2ban
    sleep 86400  # Espera de 24 horas (86400 segundos)
done &

nginx -g 'daemon off;'