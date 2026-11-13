"""Convert the '# %%' cell-marked source into a Jupyter notebook."""
import re
import sys
from pathlib import Path

import nbformat as nbf

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])
cells = []
for block in re.split(r"^# %%", src, flags=re.M)[1:]:
    header, _, body = block.partition("\n")
    body = body.strip("\n")
    if "[markdown]" in header:
        text = "\n".join(line[2:] if line.startswith("# ") else line.lstrip("#") for line in body.splitlines())
        cells.append(nbf.v4.new_markdown_cell(text))
    else:
        cells.append(nbf.v4.new_code_cell(body))
nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, out)
print(f"Wrote {out} with {len(cells)} cells")
