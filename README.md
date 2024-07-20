# WebCache
## Simple caching

Requires Docker in some form or the other for the service. Python 3.10+ for client and some knowledge on how to use both.

Linux and Mac

### Client:

Place `WEBCACHE_URL` to point towards the webcache service gateway into your environment variables either `.bashrc` or `.zprofile` if you'd like.

```bash
export WEBCACHE_URL=http://localhost:8888/webcache
```

Read the root/Client/README.md to setup the wcc.sh.

### Service:

In the root/Service root run `docker compose up --build`.

For endpoint documentation with swagger, go to `http://localhost:8888/docs`. 

