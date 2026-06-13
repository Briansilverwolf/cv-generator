from pathlib import Path
from tempfile import NamedTemporaryFile

from renders.builder import RenderTreeBuilder
from renders.engine import TemplateEngine


class CVRenderer:

    def __init__(
        self,
        output_dir: str = "output",
    ):

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.builder = RenderTreeBuilder()
        self.engine = TemplateEngine()

    def render_html(
        self,
        cv_ir,
        template_name: str = "professional",
        filename: str = "cv.html",
        temp: bool = False,
    ):

        tree = self.builder.build(cv_ir)

        html = self.engine.render(
            template_name=template_name,
            render_tree=tree.model_dump(),
        )

        if temp:

            tmp = NamedTemporaryFile(
                delete=False,
                suffix=".html"
            )

            tmp.write(
                html.encode("utf-8")
            )

            tmp.close()

            return Path(tmp.name)

        output_file = self.output_dir / filename

        output_file.write_text(
            html,
            encoding="utf-8"
        )

        return output_file