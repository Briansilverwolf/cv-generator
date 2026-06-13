from fastapi import UploadFile
from markitdown import MarkItDown
import tempfile



async def aextract_file(file: UploadFile):
    md = MarkItDown()
    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    result = md.convert(tmp_path)

    return  result.text_content
    