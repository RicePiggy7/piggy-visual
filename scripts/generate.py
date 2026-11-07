#!/usr/bin/env python3
"""Generate an image through the configured OpenAI-compatible image API.

Reads IMAGE_API_BASE and IMAGE_API_KEY from the environment and ships the
request with curl (some relays sit behind WAFs that drop Python's TLS
fingerprint). With --ref images it calls /v1/images/edits (multipart) so
characters can match the bundled reference art; otherwise it calls
/v1/images/generations. Writes the returned PNG(s) to --output (extra
images get -2, -3 suffixes).

Usage:
    python3 generate.py "prompt" -o out.png
    python3 generate.py "prompt" -o out.png --ref refs/wo.png
    python3 generate.py "prompt" -o out.png --ref refs/yuanzai-sit.png \
        --background transparent --size 1024x1024 --quality medium

Environment:
    IMAGE_API_BASE       required, e.g. https://api.example.com
    IMAGE_API_KEY        required
    PIGGY_IMAGE_MODEL    optional default for --model
                         (fallback: gpt-image-2.6-sunburst)

Requires curl on PATH.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys


def _die(message: str) -> None:
    print(f"generate.py: {message}", file=sys.stderr)
    sys.exit(1)


def _curl(args: list[str], timeout: int) -> str:
    if shutil.which("curl") is None:
        _die("curl not found on PATH")
    result = subprocess.run(
        ["curl", "-sS", "--max-time", str(timeout), *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        _die(f"curl failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout


def _post_json(url: str, key: str, payload: dict, timeout: int) -> dict:
    body = _curl(
        ["-X", "POST", url,
         "-H", f"Authorization: Bearer {key}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload),
         "-w", "\n%{http_code}"],
        timeout,
    )
    body, _, status = body.rpartition("\n")
    if status.strip() != "200":
        _die(f"HTTP {status.strip()} from {url}\n{body[:2000]}")
    return json.loads(body)


def _post_multipart(url: str, key: str, fields: dict, files: list[tuple[str, str]],
                    timeout: int) -> dict:
    args = ["-X", "POST", url, "-H", f"Authorization: Bearer {key}"]
    for name, value in fields.items():
        args += ["-F", f"{name}={value}"]
    for name, path in files:
        args += ["-F", f"{name}=@{path}"]
    args += ["-w", "\n%{http_code}"]
    body = _curl(args, timeout)
    body, _, status = body.rpartition("\n")
    if status.strip() != "200":
        _die(f"HTTP {status.strip()} from {url}\n{body[:2000]}")
    return json.loads(body)


def _download(url: str, timeout: int) -> bytes:
    result = subprocess.run(
        ["curl", "-sS", "--max-time", str(timeout), url],
        capture_output=True,
    )
    if result.returncode != 0:
        _die(f"curl download failed: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


def _save_images(payload: dict, output: str) -> list[str]:
    items = payload.get("data") or []
    if not items:
        _die(f"no image data in response: {json.dumps(payload)[:2000]}")
    saved: list[str] = []
    stem, ext = os.path.splitext(output)
    for index, item in enumerate(items):
        path = output if index == 0 else f"{stem}-{index + 1}{ext}"
        if item.get("b64_json"):
            with open(path, "wb") as handle:
                handle.write(base64.b64decode(item["b64_json"]))
        elif item.get("url"):
            with open(path, "wb") as handle:
                handle.write(_download(item["url"], 120))
        else:
            _die(f"response item {index} has neither b64_json nor url")
        saved.append(path)
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("prompt", help="image prompt text")
    parser.add_argument("-o", "--output", required=True, help="output PNG path")
    parser.add_argument("--ref", action="append", default=[],
                        help="reference image to attach (repeatable)")
    parser.add_argument("--model",
                        default=os.environ.get("PIGGY_IMAGE_MODEL", "gpt-image-2.6-sunburst"))
    parser.add_argument("--size", default="auto", help="e.g. 1024x1024, 1024x1536")
    parser.add_argument("--quality", default="medium", help="low | medium | high | auto")
    parser.add_argument("--background", default="auto",
                        choices=["auto", "transparent", "opaque"],
                        help="transparent requests a native alpha channel")
    parser.add_argument("--timeout", type=int, default=300, help="seconds")
    args = parser.parse_args()

    base = os.environ.get("IMAGE_API_BASE", "").rstrip("/")
    key = os.environ.get("IMAGE_API_KEY", "")
    if not base or not key:
        _die("set IMAGE_API_BASE and IMAGE_API_KEY in the environment")

    for path in args.ref:
        if not os.path.isfile(path):
            _die(f"reference image not found: {path}")

    common = {
        "model": args.model,
        # The relay's image URLs live on a host that refuses connections, so
        # always ask for inline base64 data instead of a download link.
        "response_format": "b64_json",
    }
    if args.size != "auto":
        common["size"] = args.size
    if args.quality != "auto":
        common["quality"] = args.quality
    if args.background != "auto":
        common["background"] = args.background

    if args.ref:
        url = f"{base}/v1/images/edits"
        files = [("image[]", path) for path in args.ref]
        payload = _post_multipart(url, key, {**common, "prompt": args.prompt},
                                  files, args.timeout)
    else:
        url = f"{base}/v1/images/generations"
        payload = _post_json(url, key, {**common, "prompt": args.prompt},
                             args.timeout)

    for path in _save_images(payload, args.output):
        print(path)


if __name__ == "__main__":
    main()
