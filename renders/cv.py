from __future__ import annotations

from tempfile  import NamedTemporaryFile
from pathlib import Path

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

        data = self._to_dict(cv)
        html = self._render_template(data)

        if temp:
            tmp = NamedTemporaryFile(delete=False, suffix=".html")

            tmp.write(html.encode("utf-8"))
            tmp.close()

            return Path(tmp.name)

        output_file = self.output_dir / filename
        output_file.write_text(html, encoding="utf-8")

        return output_file

    async def render_pdf(
        self,
        cv,
        filename: str = "cv.pdf",
        temp: bool = False,
    ) -> Path:

        try:
            from playwright.async_api import async_playwright
        except ImportError as exc:
            raise ImportError(
                "Playwright is required for PDF output.\n"
                "Install with:\n"
                "  pip install playwright\n"
                "  playwright install chromium"
            ) from exc

        #data = self._to_dict(cv)
        #html_source = self._render_template(data)
        html_source = cv
        # --------------------------------------------------
        # 1. Create temporary HTML file
        # --------------------------------------------------
        with NamedTemporaryFile(
            mode="w",
            suffix=".html",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write(html_source)
            tmp_html = Path(tmp.name)

        # --------------------------------------------------
        # 2. Decide PDF output location
        # --------------------------------------------------
        if temp:
            pdf_tmp = NamedTemporaryFile(
                suffix=".pdf",
                delete=False,
            )
            pdf_tmp.close()
            pdf_file = Path(pdf_tmp.name)
        else:
            pdf_file = self.output_dir / filename

        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch()

                page = await browser.new_page()

                await page.goto(
                    tmp_html.as_uri(),
                    wait_until="networkidle",
                )

                await page.pdf(
                    path=str(pdf_file),
                    format="A4",
                    margin={
                        "top": "2.2cm",
                        "right": "2cm",
                        "bottom": "2.2cm",
                        "left": "2cm",
                    },
                    print_background=True,
                )

                await browser.close()

            return pdf_file

        finally:
            tmp_html.unlink(missing_ok=True)