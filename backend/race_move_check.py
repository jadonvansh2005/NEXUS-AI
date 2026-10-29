import tempfile
from pathlib import Path
import shutil
from unittest.mock import patch

from mcp_servers.filesystem import core

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp).resolve()
    source = root / "source.txt"
    destination = root / "destination.txt"
    source.write_text("move me", encoding="utf-8")

    real_move = shutil.move

    def simulate_destination_change(src, dst, *args, **kwargs):
        Path(dst).mkdir()
        return real_move(src, dst, *args, **kwargs)

    with patch.object(core.shutil, "move", simulate_destination_change):
        try:
            result = core.move_file(
                source=str(source),
                destination=str(destination),
                confirm=True,
                roots=[root],
            )
            print("Move returned:", result)
        except Exception as exc:
            print("Move raised:", type(exc).__name__, str(exc))

    print("Source still exists:", source.exists())
    print(
        "File moved inside newly created directory:",
        (destination / source.name).exists(),
    )
