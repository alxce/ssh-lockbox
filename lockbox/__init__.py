from starlette.applications import Starlette
from starlette.routing import Route, Mount

from starlette.requests import Request

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from starlette.staticfiles import StaticFiles

from lockbox.db import database
from lockbox.config import SESSION_SECRET_KEY
from lockbox.auth import SessionAuthBackend

from lockbox.routes.main_page import main_page_endpoint
from lockbox.routes.login import login_endpoint, logout_endpoint
from lockbox.routes.register import register_page_endpoint, register_endpoint
from lockbox.routes.change_password import change_password_page_endpoint, change_password_endpoint
from lockbox.routes.deploy_key import deploy_key_endpoint
from lockbox.routes.list_keys import list_keys_endpoint
from lockbox.routes.delete_key import delete_key_endpoint

from lockbox.integrations.github import (
    initiate_github_integration,
    complete_github_integration,
    force_sync_github_integration,
)

app = Starlette(
    routes=[
        Route("/", endpoint=main_page_endpoint),
        Route("/login", endpoint=login_endpoint, methods=["POST"]),
        Route("/logout", endpoint=logout_endpoint, methods=["POST"]),
        Route("/register/", endpoint=register_page_endpoint),
        Route("/register", endpoint=register_endpoint, methods=["POST"]),
        Route("/deploy", endpoint=deploy_key_endpoint, methods=["POST"]),
        Route("/change_password/", endpoint=change_password_page_endpoint),
        Route("/change_password", endpoint=change_password_endpoint, methods=["POST"]),
        Route("/keys/{user}", endpoint=list_keys_endpoint),
        Route("/delete_key", endpoint=delete_key_endpoint, methods=["POST"]),
        Mount("/static", app=StaticFiles(directory="static"), name="static"),
        Route("/integrations/github/initiate", endpoint=initiate_github_integration),
        Route("/integrations/github/complete", endpoint=complete_github_integration),
        Route(
            "/integrations/github/force_sync", endpoint=force_sync_github_integration
        ),
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY),
        Middleware(AuthenticationMiddleware, backend=SessionAuthBackend()),
    ],
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
