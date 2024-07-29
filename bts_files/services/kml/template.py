from django.template import loader  # type: ignore


def render_template(temp_name: str, context: dict = None) -> str:  # type: ignore
    """Render a template with the given context."""
    temp_path = f'bts_files/{temp_name}'
    template = loader.get_template(temp_path)

    if context is None:
        context = {}

    return template.render(context)
