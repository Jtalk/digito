# Deployment for Digito Recogniser

This is a deployment supporting [https://digito.jtalk.me](https://digito.jtalk.me).

Some useful options:

```
ui.deployment.image.version = <version of the docker image to deploy, defaults to latest>
api.deployment.image.version = <version of the docker image to deploy, defaults to latest>

domains = <a list of domains the app is served on>
basePath = <a base path prefix for the app, if not served at the root of the domain>
api.basePath = <a base path prefix for the API, defaults to /api on the same domain>
```