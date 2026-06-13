from abc import ABC, abstractmethod
from pathlib import Path

from abc import ABC, abstractmethod
from pathlib import Path


class BaseRenderer(ABC):
    def __init__(
        self,
        template_path: str = "template.html",
        output_dir: str = "output",
    ):
        self.template_path = Path(template_path)
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ==================================================
    # SHARED HELPERS
    # ==================================================

    def _to_dict(self, cv):
        """
        Accepts:
        - Pydantic model (model_dump)
        - dict
        """
        if hasattr(cv, "model_dump"):
            return cv.model_dump()
        return cv

    @abstractmethod
    def render_html(self, cv, filename: str = "cv.html") -> Path:
        pass

    @abstractmethod
    def render_pdf(self, cv, filename: str = "cv.pdf") -> Path:
        pass

    @abstractmethod
    def render_docx(self, cv, filename: str = "cv.docx") -> Path:
        pass