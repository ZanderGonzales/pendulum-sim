"""Vendor the pinned official Crazyflie model; not needed for normal simulation.

Run from the repository root. Only the upstream XML, meshes, README, and license
are downloaded. A SHA-256 manifest records the unmodified upstream files.
"""

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request


REVISION = "71f066ad0be9cd271f7ed58c030243ef157af9f4"
REPOSITORY = "https://github.com/google-deepmind/mujoco_menagerie"
PREFIX = "bitcraze_crazyflie_2/"
DESTINATION = Path(__file__).resolve().parents[2] / "src/drone_sim/assets/bitcraze_crazyflie_2"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "pendulum-sim-drone"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    tree = json.loads(fetch(f"https://api.github.com/repos/google-deepmind/mujoco_menagerie/git/trees/{REVISION}?recursive=1"))
    if tree.get("truncated"):
        raise RuntimeError("Upstream tree listing was truncated")
    paths = sorted(item["path"][len(PREFIX):] for item in tree["tree"]
                   if item["type"] == "blob" and item["path"].startswith(PREFIX)
                   and (item["path"].endswith((".xml", ".obj"))
                        or item["path"][len(PREFIX):] in ("LICENSE", "README.md")))
    if not {"cf2.xml", "scene.xml", "LICENSE", "README.md"}.issubset(paths):
        raise RuntimeError("Required model files are missing upstream")

    def download(relative: str) -> tuple[str, str]:
        payload = fetch(f"https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/{REVISION}/{PREFIX}{relative}")
        target = DESTINATION / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        return relative, hashlib.sha256(payload).hexdigest()

    with ThreadPoolExecutor(max_workers=6) as pool:
        hashes = dict(pool.map(download, paths))
    manifest = {"repository": REPOSITORY, "revision": REVISION, "model": PREFIX.rstrip("/"),
                "license": "MIT", "sha256": hashes}
    (DESTINATION / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Vendored {len(hashes)} unmodified model files at {REVISION}")


if __name__ == "__main__":
    main()
