#!/bin/sh
for file in /usr/share/nginx/html/js/app.*.js;
do
  sed -i 's@VUE_APP_API_URL@'"$VUE_APP_API_URL"'@g' $file;
done
echo "Starting Nginx"
nginx -g 'daemon off;'
