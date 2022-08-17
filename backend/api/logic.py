from django.template.loader import render_to_string
from weasyprint import HTML


def get_pdf(context: dict) -> bytes:
    template = render_to_string(
        template_name='pdf_template.html', context=context
    )
    html = HTML(string=template)
    return html.write_pdf()
