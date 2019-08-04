FROM node:12
EXPOSE 80
EXPOSE 443
COPY . /app
WORKDIR /app
ARG API_LOCATION=http://localhost:8080
ARG PREBUILT=0
ENV NODE_ENV=production
ENV PORT=80
ENV REACT_APP_API_LOCATION=$API_LOCATION
ENV PREBUILT=$PREBUILT
RUN npm install
RUN test "$PREBUILT" != 0 && echo "Pre-building CRA" && npm run build || echo "CRA pre-build disabled"
RUN echo Building for $NODE_ENV
RUN test "$NODE_ENV" = 'production' && test "$PREBUILT" != 0 \
        && echo "Building for production with a pre-built CRA, removing sources" && rm -r src \
        || echo -n ''
CMD ["npm", "run", "serve-docker"]