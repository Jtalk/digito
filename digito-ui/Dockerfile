FROM node:12

EXPOSE 80
EXPOSE 443
WORKDIR /app
COPY build ./
COPY package.json ./
COPY package-lock.json ./

ARG API_LOCATION=http://localhost:8080
ENV NODE_ENV=production
ENV PORT=80
ENV REACT_APP_API_LOCATION=$API_LOCATION

CMD ["npm", "run", "serve"]