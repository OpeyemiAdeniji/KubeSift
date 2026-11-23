"""krew-index rules the manifest must keep: a short tagline and no usage strings (krew prints those itself)."""

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def manifest(tmp_path):
    spec = importlib.util.spec_from_file_location("krew_manifest", ROOT / "scripts" / "krew_manifest.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for os_, arch in mod.PLATFORMS:
        ext = "zip" if os_ == "windows" else "tar.gz"
        name = f"kubectl-sift_{os_}_{arch}.{ext}"
        (tmp_path / f"{name}.sha256").write_text(f"{'a' * 64}  {name}\n")
    return yaml.safe_load(mod.manifest("v9.9.9", tmp_path))


def test_short_description_is_a_tagline_of_at_most_50_characters(tmp_path):
    short = manifest(tmp_path)["spec"]["shortDescription"]
    assert len(short) <= 50 and not short.endswith("."), short


def test_no_usage_strings(tmp_path):
    spec = manifest(tmp_path)["spec"]
    for field in ("description", "caveats"):
        assert "kubectl sift" not in spec[field] and "Run `" not in spec[field], spec[field]


def test_every_platform_has_a_quoted_sha(tmp_path):
    platforms = manifest(tmp_path)["spec"]["platforms"]
    assert len(platforms) == 5 and all(isinstance(p["sha256"], str) and len(p["sha256"]) == 64 for p in platforms)


def test_the_index_manifest_keeps_krew_rules():
    """plugins/sift.yaml is KubeSift's own krew index (`kubectl krew index add kubesift <repo>`)."""
    spec = yaml.safe_load((ROOT / "plugins" / "sift.yaml").read_text(encoding="utf-8"))["spec"]
    assert len(spec["shortDescription"]) <= 50
    assert "kubectl sift" not in spec["description"] + spec["caveats"]
    version = spec["version"]
    assert len(spec["platforms"]) == 5
    for p in spec["platforms"]:
        assert f"/releases/download/{version}/" in p["uri"], p["uri"]  # every archive is from the same release
        assert isinstance(p["sha256"], str) and len(p["sha256"]) == 64
