#!/bin/bash

openssl req -x509 -newkey rsa:4096 -keyout haproxy-selfsigned.key -out haproxy-selfsigned.crt -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN="

cat haproxy-selfsigned.crt haproxy-selfsigned.key > /etc/haproxy/haproxy.pem

echo "
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats timeout 300s
    user haproxy
    group haproxy
    daemon

    ssl-default-bind-options no-sslv3

defaults
    log global
    mode http
    option httplog
    option dontlognull
    option http-server-close
    option clitcpka
    option srvtcpka
    timeout connect 10s
    timeout client  3m
    timeout server  3m
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

frontend https-in
    bind *:443 ssl crt /etc/haproxy/haproxy.pem
    mode http
    default_backend bge_m3_backend

backend bge_m3_backend
    mode http
    server bge_m3_server 127.0.0.1:8093 maxconn 4 maxqueue 100
" > /etc/haproxy/haproxy.cfg

haproxy -f /etc/haproxy/haproxy.cfg -db &

pip install -r requirements.txt
pip install gunicorn
