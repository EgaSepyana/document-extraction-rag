import uvicorn
from fastapi import FastAPI
from datetime import datetime, timezone
from api.config.base import Setting
from api.config.base import settings
import argparse
import time

from fastapi.middleware.cors import CORSMiddleware

ROUTER_MODULES = {
    "qna": "qna"
}

argument_parser = argparse.ArgumentParser(
    description="Issue Cluster", formatter_class=argparse.RawDescriptionHelpFormatter
)
argument_parser.add_argument("-p", "--port", help="Port", metavar="", default="8020")
argument_parser.add_argument("-worker", "--worker", type=int, default=1)
# please use [...] for selecting some end points, ex: agent[add:get-one:get-all]
argument_parser.add_argument(
    "-routers", "--routers", help="Include Routers", default=None
)
argument_parser.add_argument(
    "-exc_routers", "--exc_routers", help="Exclude Routers", default=None
)
argument_parser.add_argument("-uenv", "--update_env", default=None)
argument_parser.add_argument("-fenv", "--file_env", default=".env")
args = argument_parser.parse_args()

settings = Setting(file=args.file_env, update_env=args.update_env, routers=args.routers)

app = FastAPI(**{"title": "Fusion Survey", "description": "REST API for Fusion"})
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", include_in_schema=False)
async def get_service_info():
    """
    Menampilkan informasi dasar dan status layanan API.
    """
    return {
        "service_name": app.title,
        "version": app.version,
        "status": "active",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "documentation_url": "/docs"
    }

exclude_routers = args.exc_routers or ''
for router_name, module_name in ROUTER_MODULES.items():
    if (not args.routers or router_name in args.routers) and router_name not in exclude_routers:
        module = __import__(f"api.controller.{module_name}", fromlist=["router"])
        app.include_router(module.router)

MAX_REQUEST_BODY = 1024 * 1024 * 1024

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(settings.PROJECT_SERVICE_PORT),
        workers=args.worker,
        reload=False if args.worker > 1 else True,
        limit_max_requests=MAX_REQUEST_BODY,
    )
