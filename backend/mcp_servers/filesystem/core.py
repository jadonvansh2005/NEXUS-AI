from __future__ import annotations
import fnmatch, hashlib, os, shutil
from pathlib import Path
from typing import Iterable
import ctypes
import msvcrt
import os

import ctypes
import msvcrt
import tempfile

DEFAULT_ROOT = r"D:\UPSS\backend"
MAX_READ_BYTES = 1_000_000
MAX_WRITE_BYTES = 1_000_000
MAX_SEARCH_RESULTS = 500
MAX_DIRECTORY_ENTRIES = 500
SKIP_DIR_NAMES = {".git", ".venv", "venv", "__pycache__", "node_modules"}

class FilesystemError(ValueError):
    """Safe, user-facing filesystem operation error."""

def configured_roots() -> list[Path]:
    raw = os.environ.get("NEXUS_MCP_ALLOWED_ROOTS", "").strip()
    values = raw.split(os.pathsep) if raw else [DEFAULT_ROOT]
    roots = []
    for value in values:
        if not value.strip():
            continue
        candidate = Path(value).expanduser().resolve(strict=True)
        if not candidate.is_dir():
            raise FilesystemError(f"Configured root is not a directory: {candidate}")
        if candidate not in roots:
            roots.append(candidate)
    if not roots:
        raise FilesystemError("No allowed filesystem roots are configured.")
    return roots

def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False

def resolve_allowed(path_text: str, roots: Iterable[Path], *, must_exist: bool = True) -> Path:
    roots = list(roots)
    if not isinstance(path_text, str) or not path_text.strip():
        raise FilesystemError("A non-empty path is required.")
    raw = Path(path_text).expanduser()
    candidates = [raw] if raw.is_absolute() else [root / raw for root in roots]
    for candidate in candidates:
        try:
            resolved = candidate.resolve(strict=must_exist)
        except (OSError, RuntimeError):
            continue
        if any(_is_within(resolved, root) for root in roots):
            return resolved
    raise FilesystemError("Path is outside configured allowed roots or cannot be resolved.")

def list_directory(path: str, roots: Iterable[Path]) -> dict:
    target = resolve_allowed(path, roots)
    if not target.is_dir():
        raise FilesystemError("Path is not a directory.")
    entries = []
    for child in sorted(target.iterdir(), key=lambda p: p.name.casefold()):
        try:
            safe = resolve_allowed(str(child), roots)
            is_dir = safe.is_dir()
            size = None if is_dir else safe.stat().st_size
        except (FilesystemError, OSError):
            continue
        entries.append({"name": child.name, "path": str(child), "type": "directory" if is_dir else "file", "size_bytes": size})
        if len(entries) >= MAX_DIRECTORY_ENTRIES:
            break
    return {"path": str(target), "entries": entries, "truncated": len(entries) >= MAX_DIRECTORY_ENTRIES}

def search_files(root: str, pattern: str = "*", max_results: int = 100, roots: Iterable[Path] = ()) -> dict:
    target = resolve_allowed(root, roots)
    if not target.is_dir():
        raise FilesystemError("Search root is not a directory.")
    if not pattern or len(pattern) > 256:
        raise FilesystemError("Pattern must contain 1–256 characters.")
    if not 1 <= max_results <= MAX_SEARCH_RESULTS:
        raise FilesystemError(f"max_results must be between 1 and {MAX_SEARCH_RESULTS}.")
    results, truncated = [], False
    for current, dirs, names in os.walk(target, followlinks=False):
        current_path = Path(current)
        safe_dirs = []
        for name in dirs:
            candidate = current_path / name
            if name in SKIP_DIR_NAMES or candidate.is_symlink():
                continue
            try:
                if resolve_allowed(str(candidate), roots).is_dir():
                    safe_dirs.append(name)
            except (FilesystemError, OSError):
                continue
        dirs[:] = safe_dirs
        for name in sorted(names, key=str.casefold):
            candidate = current_path / name
            if not fnmatch.fnmatch(name, pattern):
                continue
            try:
                safe = resolve_allowed(str(candidate), roots)
                if not safe.is_file():
                    continue
                results.append({"name": name, "path": str(safe), "size_bytes": safe.stat().st_size})
            except (FilesystemError, OSError):
                continue
            if len(results) >= max_results:
                truncated = True
                break
        if truncated:
            break
    return {"root": str(target), "pattern": pattern, "results": results, "truncated": truncated}

def read_file(path: str, roots: Iterable[Path]) -> dict:
    target = resolve_allowed(path, roots)
    if not target.is_file():
        raise FilesystemError("Path is not a file.")
    size = target.stat().st_size
    if size > MAX_READ_BYTES:
        raise FilesystemError(f"File is {size} bytes; limit is {MAX_READ_BYTES} bytes.")
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise FilesystemError("File is not valid UTF-8 text.") from exc
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {"path": str(target), "size_bytes": size, "sha256": digest, "content": content}

def create_file(path: str, content: str, confirm: bool, roots: Iterable[Path]) -> dict:
    if not confirm:
        raise FilesystemError("Creation requires confirm=true after user approval.")
    if not isinstance(content, str):
        raise FilesystemError("content must be text.")
    data = content.encode("utf-8")
    if len(data) > MAX_WRITE_BYTES:
        raise FilesystemError(f"Content exceeds {MAX_WRITE_BYTES} bytes.")
    target = resolve_allowed(path, roots, must_exist=False)
    if target.exists():
        raise FilesystemError("File already exists; create_file never overwrites.")
    if not target.parent.exists() or not target.parent.is_dir():
        raise FilesystemError("Parent directory must already exist.")
    try:
        with target.open("x", encoding="utf-8", newline="") as f:
            f.write(content)
    except FileExistsError as exc:
        raise FilesystemError("File already exists; create_file never overwrites.") from exc
    return {"path": str(target), "created": True, "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}



def edit_file(
    path: str,
    content: str,
    expected_sha256: str,
    confirm: bool,
    roots: Iterable[Path],
) -> dict:
    if not confirm:
        raise FilesystemError(
            "Editing requires confirm=true after user approval."
        )

    if (
        not isinstance(expected_sha256, str)
        or len(expected_sha256) != 64
        or any(c not in "0123456789abcdefABCDEF" for c in expected_sha256)
    ):
        raise FilesystemError(
            "A valid expected_sha256 from read_file is required."
        )

    if not isinstance(content, str):
        raise FilesystemError("content must be text.")

    data = content.encode("utf-8")
    if len(data) > MAX_WRITE_BYTES:
        raise FilesystemError(
            f"Content exceeds {MAX_WRITE_BYTES} bytes."
        )

    target = resolve_allowed(path, roots)
    if not target.is_file():
        raise FilesystemError("Target must be a regular file.")

    # Windows CreateFileW constants.
    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_DELETE = 0x00000004
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    create_file.restype = ctypes.c_void_p

    handle = create_file(
        str(target),
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )

    if handle == INVALID_HANDLE_VALUE:
        error = ctypes.get_last_error()
        raise FilesystemError(
            f"Cannot safely access file (Windows error {error})."
        )

    fd = None
    temp_path = None

    try:
        fd = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
        handle = None  # The file descriptor now owns the handle.

        size = os.fstat(fd).st_size
        if size > MAX_READ_BYTES:
            raise FilesystemError(
                "Target must be a text file no larger than 1 MB."
            )

        os.lseek(fd, 0, os.SEEK_SET)
        chunks = []
        remaining = size

        while remaining:
            chunk = os.read(fd, min(remaining, 65536))
            if not chunk:
                raise FilesystemError(
                    "File could not be read completely; refusing to edit."
                )
            chunks.append(chunk)
            remaining -= len(chunk)

        current_data = b"".join(chunks)
        current_hash = hashlib.sha256(current_data).hexdigest()

        if current_hash.lower() != expected_sha256.lower():
            raise FilesystemError(
                "File changed since it was read; refusing to overwrite."
            )

        # Prepare the complete replacement beside the original.
        # Same-directory replacement avoids cross-volume moves.
        temp_fd, temp_name = tempfile.mkstemp(
            prefix=f".{target.name}.",
            suffix=".tmp",
            dir=str(target.parent),
        )
        temp_path = Path(temp_name)

        with os.fdopen(temp_fd, "wb") as temp_file:
            temp_file.write(data)
            temp_file.flush()
            os.fsync(temp_file.fileno())

        # Recheck the original handle before replacing the path.
        # Its sharing mode denies new write handles while permitting
        # the delete/rename access required by replacement.
        os.lseek(fd, 0, os.SEEK_SET)
        check_chunks = []
        remaining = size

        while remaining:
            chunk = os.read(fd, min(remaining, 65536))
            if not chunk:
                raise FilesystemError(
                    "File changed during edit; refusing replacement."
                )
            check_chunks.append(chunk)
            remaining -= len(chunk)

        check_hash = hashlib.sha256(b"".join(check_chunks)).hexdigest()
        if check_hash.lower() != expected_sha256.lower():
            raise FilesystemError(
                "File changed during edit; refusing replacement."
            )

        # Replace only after the complete temporary file is ready.
        # If replacement fails, the original path remains untouched.
        replace_file = kernel32.ReplaceFileW
        replace_file.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        replace_file.restype = ctypes.c_int

        success = replace_file(
            str(target),
            str(temp_path),
            None,
            0,
            None,
            None,
        )

        if not success:
            error = ctypes.get_last_error()
            raise FilesystemError(
                f"Cannot safely replace file (Windows error {error})."
            )

        temp_path = None

        return {
            "path": str(target),
            "edited": True,
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    except FilesystemError:
        raise
    except OSError as exc:
        raise FilesystemError(
            f"Cannot safely edit file: {exc}"
        ) from exc
    finally:
        if fd is not None:
            os.close(fd)

        if handle is not None:
            kernel32.CloseHandle(handle)

        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass




def move_file(
    source: str,
    destination: str,
    confirm: bool,
    roots: Iterable[Path],
) -> dict:
    if not confirm:
        raise FilesystemError(
            "Moving requires confirm=true after user approval."
        )

    src = resolve_allowed(source, roots)
    if not src.is_file():
        raise FilesystemError(
            "Source must be a file; directory moves are not supported."
        )

    dst = resolve_allowed(destination, roots, must_exist=False)

    if dst.exists():
        raise FilesystemError(
            "Destination already exists; refusing to overwrite."
        )

    if not dst.parent.exists() or not dst.parent.is_dir():
        raise FilesystemError(
            "Destination parent directory must already exist."
        )

    try:
        # On Windows, os.rename fails if the destination already exists.
        # Unlike shutil.move, it does not redirect the source into a
        # destination directory created after the earlier existence check.
        os.rename(str(src), str(dst))
    except FileExistsError as exc:
        raise FilesystemError(
            "Destination appeared during move; refusing to overwrite."
        ) from exc
    except OSError as exc:
        raise FilesystemError(
            f"Cannot safely move file: {exc}"
        ) from exc

    return {
        "source": str(src),
        "destination": str(dst),
        "moved": True,
    }

