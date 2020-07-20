FROM node:10-alpine as builder

ENV VUE_APP_API_URL "VUE_APP_API_URL"

# install and cache app dependencies
COPY package.json package-lock.json ./
RUN npm install && mkdir /frontend && mv ./node_modules ./frontend

WORKDIR /frontend

COPY . .

RUN npm run build

# ------------------------------------------------------
# Production Build
# ------------------------------------------------------
FROM nginx:1.16.0-alpine

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY --from=builder /frontend/dist /usr/share/nginx/html
EXPOSE 80

ENTRYPOINT [ "/entrypoint.sh" ]
