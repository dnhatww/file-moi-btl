import os
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "4")
import nbformat
from nbclient import NotebookClient
from datetime import datetime

def progress(cell, cell_index, **kwargs):
    print(f"{datetime.now().isoformat(timespec='seconds')} cell {cell_index}", flush=True)

if __name__ == "__main__":
    notebook = nbformat.read("benchmark_toxic_v2.ipynb", as_version=4)
    notebook.cells[2].source = "import sys; sys.path.append(str(__import__('pathlib').Path.cwd() / '.runtime'))\n" + notebook.cells[2].source
    client = NotebookClient(notebook, timeout=7200, kernel_name="python3", resources={"metadata": {"path": os.getcwd()}}, on_cell_start=progress)
    try:
        client.execute()
    finally:
        nbformat.write(notebook, "benchmark_toxic_v2_executed.ipynb")
    print("EXECUTION COMPLETED", flush=True)

