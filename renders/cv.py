from __future__ import annotations

from tempfile  import NamedTemporaryFile
from pathlib import Path
from playwright.sync_api import playwright
import tempfile

from jinja2 import Template

_HERE = Path(__file__).parent.parent



class CVRenderer:


    def __init__(
        self,
        template_path: str = "template/standard.html",
        output_dir: str = "output3",
    ):
        self.template_path = Path(template_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

   

    def _to_dict(self, cv) -> dict:
        """Accept a Pydantic model or plain dict."""
        if hasattr(cv, "model_dump"):
            return cv.model_dump()
        return cv

    def _render_template(self, data: dict) -> str:
        """Render the Jinja2 HTML template with CV data."""
        source = self.template_path.read_text(encoding="utf-8")
        template = Template(source)
        return template.render(**data)




    def render_html(self, cv, filename: str = "cv.html", temp: bool = False) -> Path:
        """Render CV to HTML file (persistent or temporary)."""
        html = cv

        if temp:
            tmp = NamedTemporaryFile(delete=False, suffix=".html")

            tmp.write(html.encode("utf-8"))
            tmp.close()

            return Path(tmp.name)

        output_file = self.output_dir / filename
        output_file.write_text(html, encoding="utf-8")

        return output_file

    def render_pdf(self, cv, filename: str = "cv.pdf", temp: bool = False):


        html_source = cv

        if temp:
            pdf_tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            pdf_tmp.close()
            pdf_file = Path(pdf_tmp.name)
        else:
            pdf_file = self.output_dir / filename

        with playwright() as pw:
            
            browser = pw.chromium.launch(

                )
            

            page =  browser.new_page()

            # KEY FIX: no file:// temp file
            page.set_content(html_source)

            page.pdf(
                path=str(pdf_file),
                format="A4",
                margin={
                    "top": "0.5cm",
                    "right": "0.5cm",
                    "bottom": "0.5cm",
                    "left": "0.5cm",
                },
                print_background=True,
            )

            await browser.close()

        return pdf_file
   