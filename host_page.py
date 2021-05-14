import json
import hmac
from pathlib import Path
from aiohttp import web
import aiohttp_jinja2
import jinja2
import subprocess

router = web.RouteTableDef()


@router.get('/run')
async def show_present(request: web.Request) -> web.Response:
    context = {}
    response = aiohttp_jinja2.render_template(
        "target.html",
        request,
        context=context
    )
    print("In Run")
    subprocess.run(["./scripts/homepage.sh"])
    return response


@router.post('/homepage')
async def get_payload(request: web.Request) -> web.Response:
    print("in payload")
    with open("secrets.json") as json_file:
        jjj = json.load(json_file)
        secret = jjj["github-secret"]
    print("Got secret")
    assert request.content_length < 1000000, "Request content too fat"  # 1M
    digest, signature = request.headers['X-HUB-SIGNATURE'].split("=", 1)
    assert digest == "sha1", "Digest must be sha1"  # use a whitelist
    body = await request.content.read()
    h = hmac.HMAC(bytes(secret, "UTF8"), msg=body, digestmod=digest)
    assert h.hexdigest() == signature, "Bad signature"
    s_body = body.decode('UTF8')
    s = json.loads(s_body)
    print(s)
    subprocess.run(["./scripts/homepage.sh"])
    return web.Response(text="Success")


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(router)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(Path(__file__).parent / "templates"))
    )
    return app


if __name__ == '__main__':
    web.run_app(init_app(), port="8888")
