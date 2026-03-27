from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "build" / "release"
README_PATH = REPO_ROOT / "README.md"
SKILL_SOURCE_DIR = REPO_ROOT / "client_assets" / "skills" / "kompas-mcp-operator"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a client-facing release zip from either a compiled client zip or a downloaded GitHub Actions artifact zip.",
    )
    parser.add_argument(
        "--source-zip",
        required=True,
        help="Path to either a compiled client zip or a downloaded GitHub Actions artifact zip.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where the final client package zip will be written.",
    )
    parser.add_argument(
        "--version-label",
        required=True,
        help="Version or tag label to embed in the final package name, for example v1.0.16.",
    )
    parser.add_argument(
        "--bundle-name",
        default="KOMPAS-3D-MCP-bin",
        help="Base name for the staged package directory and final zip file.",
    )
    return parser.parse_args()


def _extract_zip(zip_path: Path, target_dir: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(target_dir)


def _find_inner_client_zip(extracted_dir: Path) -> Path | None:
    matches = sorted(extracted_dir.rglob("kompas-mcp-client-win-py314-*.zip"))
    if matches:
        return matches[0]
    return None


def _copy_tree_contents(source_dir: Path, target_dir: Path) -> None:
    for item in source_dir.iterdir():
        destination = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)


def _prepare_payload(artifact_zip: Path, staging_root: Path) -> Path:
    outer_dir = staging_root / "outer"
    _extract_zip(artifact_zip, outer_dir)

    inner_zip = _find_inner_client_zip(outer_dir)
    if inner_zip is not None:
        payload_dir = staging_root / "payload"
        _extract_zip(inner_zip, payload_dir)
        return payload_dir

    return outer_dir


def _flatten_single_root_dir(payload_dir: Path) -> Path:
    entries = [entry for entry in payload_dir.iterdir()]
    if len(entries) != 1:
        return payload_dir
    only_entry = entries[0]
    if not only_entry.is_dir():
        return payload_dir
    return only_entry


def _remove_unwanted_files(target_dir: Path) -> None:
    for path in list(target_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith(".zip"):
            path.unlink()
            continue
        if path.name == "nuitka-report.xml":
            path.unlink()


def _create_release_zip(source_dir: Path, destination_zip: Path) -> None:
    if destination_zip.exists():
        destination_zip.unlink()
    shutil.make_archive(str(destination_zip.with_suffix("")), "zip", root_dir=source_dir.parent, base_dir=source_dir.name)


def main() -> int:
    args = _parse_args()
    artifact_zip = Path(args.source_zip).resolve()
    output_dir = Path(args.output_dir).resolve()
    bundle_name = str(args.bundle_name)
    version_label = str(args.version_label)

    if not artifact_zip.is_file():
        raise FileNotFoundError(f"Artifact zip not found: {artifact_zip}")
    if not README_PATH.is_file():
        raise FileNotFoundError(f"README.md not found: {README_PATH}")
    if not SKILL_SOURCE_DIR.is_dir():
        raise FileNotFoundError(f"Skill directory not found: {SKILL_SOURCE_DIR}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="kompas-client-package-") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        payload_dir = _flatten_single_root_dir(_prepare_payload(artifact_zip, temp_dir))

        package_root = temp_dir / bundle_name
        package_root.mkdir(parents=True, exist_ok=True)

        _copy_tree_contents(payload_dir, package_root)
        _remove_unwanted_files(package_root)

        shutil.copy2(README_PATH, package_root / "README.md")

        skills_root = package_root / "skills"
        skills_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SKILL_SOURCE_DIR, skills_root / "kompas-mcp-operator", dirs_exist_ok=True)

        destination_zip = output_dir / f"{bundle_name}-{version_label}.zip"
        _create_release_zip(package_root, destination_zip)
        print(destination_zip)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
