FROM node:16-alpine

EXPOSE 80
EXPOSE 443
WORKDIR /app
COPY build/ ./build
COPY node_modules/ ./node_modules
COPY package.json ./
COPY package-lock.json ./

ENV PORT=80

# Set by docker run, per-environment
# ENV REACT_APP_API_LOCATION=http://localhost:8080
# ENV NODE_ENV=production

CMD ["npm", "run", "serve"]