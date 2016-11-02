FROM python:3-onbuild
EXPOSE 80
CMD gunicorn server:server_app --bind 0.0.0.0:80 --worker-class aiohttp.worker.GunicornUVLoopWebWorker
