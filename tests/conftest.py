import graphene
from pathlib import Path
import pytest
import multiprocessing
import concurrent.futures

import responder
from responder.templates import Templates


@pytest.fixture
def data_dir(current_dir):
    yield current_dir / "data"


@pytest.fixture()
def current_dir():
    yield Path(__file__).parent


@pytest.fixture
def api():
    return responder.API(debug=False, allowed_hosts=[";"])


@pytest.fixture
def session(api):
    return api.requests


@pytest.fixture
def url():
    def url_for(s):
        return f"http://;{s}"

    return url_for


@pytest.fixture
def flask():
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"

    return app


@pytest.fixture
def schema():
    class Query(graphene.ObjectType):
        hello = graphene.String(name=graphene.String(default_value="stranger"))

        def resolve_hello(self, info, name):
            return f"Hello {name}"

    return graphene.Schema(query=Query)


@pytest.fixture
def templates_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("templates")


@pytest.fixture
def templates(templates_dir):
    return Templates(templates_dir)


@pytest.fixture
def template_file(templates, tmpdir_factory):
    templates_dir = tmpdir_factory.mktemp("templates")

    template = templates_dir.join("index.html")
    template.write("<h1>Hello {{ name }}!</h1>")

    return template
