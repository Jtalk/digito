FROM node:12
EXPOSE 80
EXPOSE 443
COPY . /app
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=80
# ENV REACT_APP_API_LOCATION=depends on deployment
RUN npm install
RUN CI=true npm run test src
RUN npm run build
RUN echo Building for $NODE_ENV
RUN test "$NODE_ENV" = 'production' && rm -r src || echo -n ''
CMD ["npm", "run", "serve"]