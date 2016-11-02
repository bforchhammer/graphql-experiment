import asyncio

import graphene
import ujson
import uvloop
from aiohttp import web
from aiohttp.web_reqrep import json_response
from graphql.execution.executors.asyncio import AsyncioExecutor

policy = asyncio.get_event_loop_policy()
if not isinstance(policy, uvloop.EventLoopPolicy):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Query(graphene.ObjectType):
    hello = graphene.String()
    hello2 = graphene.String()

    def resolve_hello(self, args, context, info):
        return 'Hello world!'

    def resolve_hello2(self, args, context, info):
        raise Exception("hello2 exception")


schema = graphene.Schema(query=Query)


async def handler(request):
    # query = '{ hello, hello2 }'
    query = '{ hello }'
    result = await schema.execute(query, executor=AsyncioExecutor(), return_promise=True)
    data = {'data': result.data}
    if result.errors:
        data['errors'] = [str(e) for e in result.errors]
    return json_response(data, dumps=ujson.dumps)


def init(argv=None):
    # Run server (1): python3 -m aiohttp.web -H localhost -P 8080 server:init
    app = web.Application()
    app.router.add_get('/', handler)
    return app

# Run server (2): gunicorn server:server_app --bind 0.0.0.0:8080 --worker-class aiohttp.worker.GunicornUVLoopWebWorker
server_app = init()

if __name__ == "__main__":
    # Run server (3): python3 server.py
    web.run_app(server_app)
