from pathlib import Path

from typing import List
from typing import Set


DEFAULT_EXTENSIONS: Set[str] = {

    ".py",
    ".java",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",

    ".md",
    ".txt",
    ".rst",

    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",

    ".html",
    ".css",
    ".scss",

    ".sql",

    ".xml"

}


DEFAULT_EXCLUDED_DIRECTORIES: Set[str] = {

    ".git",

    ".github",

    ".idea",

    ".vscode",

    "__pycache__",

    "venv",

    ".venv",

    "node_modules",

    "dist",

    "build",

    ".next",

    ".pytest_cache",

    ".mypy_cache",

    ".ruff_cache",

    ".cache"

}


class ProjectScanner:


    def __init__(

        self,

        extensions: Set[str] | None = None,

        excluded_directories: Set[str] | None = None

    ):

        self.extensions = (

            extensions

            if extensions is not None

            else DEFAULT_EXTENSIONS

        )

        self.excluded_directories = (

            excluded_directories

            if excluded_directories is not None

            else DEFAULT_EXCLUDED_DIRECTORIES

        )


    # --------------------------------------------------
    # Scan Project
    # --------------------------------------------------

    def scan(

        self,

        root_directory: str

    ) -> List[Path]:

        root = (

            Path(

                root_directory

            ).resolve()

        )

        if not root.exists():

            raise FileNotFoundError(

                root

            )

        files: List[Path] = []

        for path in root.rglob("*"):

            if not path.is_file():

                continue

            if self._is_excluded(

                path

            ):

                continue

            if path.suffix.lower() not in self.extensions:

                continue

            files.append(

                path

            )

        return sorted(

            files

        )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _is_excluded(

        self,

        path: Path

    ) -> bool:

        return any(

            part in self.excluded_directories

            for part in path.parts

        )


    def supported_extensions(

        self

    ) -> List[str]:

        return sorted(

            self.extensions

        )


    def excluded_folders(

        self

    ) -> List[str]:

        return sorted(

            self.excluded_directories

        )