from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from template.registry import TEMPLATES,MAPPING, TemplateSelection


class TemplateEngine:

    def __init__(self, dir_name: str):

        self.base_path = Path(__file__).parent.parent / dir_name

        self.env = Environment(
            loader=FileSystemLoader(self.base_path),
            autoescape=True
        )

    # -------------------------
    # TEMPLATE RESOLUTION
    # -------------------------

    def _resolve_template(self, slot: str):

        if slot not in TEMPLATES:
            raise ValueError(f"Unknown template slot: {slot}")

        return TEMPLATES[slot]

    # -------------------------
    # CSS RESOLUTION
    # -------------------------

    def _load_css(self,slot, path: str) -> str:
        """
        Read CSS file as raw string
        """
        full_path = self.base_path / slot / path

        if not full_path.exists():
            raise FileNotFoundError(f"CSS not found: {full_path}")

        return full_path.read_text(encoding="utf-8")

    def _resolve_variant_css(self, variant: str) -> str:
        return MAPPING.get(variant, "styles/base.css")

    # -------------------------
    # RENDER
    # -------------------------

    def render(
        self,
        template: TemplateSelection,
        render_tree: dict,
    ) -> str:

        # 1. Resolve template
        definition = self._resolve_template(template.slot)

        jinja_template = self.env.get_template(
            definition.layout_path
        )

        # 2. Load CSS (REAL CONTENT, not filenames)
        base_css = self._load_css(template.slot,"styles/base.css")
        variant_css = self._load_css(
            template.slot,
            self._resolve_variant_css(template.variant)
        )

        # 3. Build context
        context = {
            **render_tree,
            "template_slot": template.slot,
            "variant": template.variant,
            "base_css": base_css,
            "variant_css": variant_css,
        }

        return jinja_template.render(**context)