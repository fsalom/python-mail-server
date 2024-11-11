#!/bin/bash

service fail2ban start

while true; do
    logrotate /etc/logrotate.d/fail2ban
    sleep 86400
done &

nginx -g 'daemon off;'
