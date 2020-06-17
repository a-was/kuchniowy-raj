import re

from flask import Blueprint
from jinja2 import Markup, evalcontextfilter, escape

app = Blueprint('custom_template_filters', __name__)


@evalcontextfilter
@app.app_template_filter()
def newline_to_br(context, value):
    result = '<br />'.join(re.split(r'(?:\r\n|\r|\n){2,}', escape(value)))
    if context.autoescape:
        result = Markup(result)
    return result
