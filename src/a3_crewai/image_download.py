import os
import json
import requests

MANIFEST_PATH = "./images/manifest.json"
OUTPUT_DIR    = "output/images"

def load_assets(manifest_path):
    """Return a list of {"filename": .., "url": ..} dicts, no matter the JSON layout."""
    with open(manifest_path, "r") as f:
        data = json.load(f)

    # 1) Already an array of objects
    if isinstance(data, list):
        return data

    # 2) Wrapped as { "assets": [ {...}, ... ] }
    if isinstance(data, dict) and "assets" in data:
        return data["assets"]

    # 3) Flat mapping { "file.png": "https://..." }
    if isinstance(data, dict):
        return [ {"filename": k, "url": v} for k, v in data.items() ]

    # Anything else is unsupported
    raise ValueError("Unrecognised manifest format")

def batch_download_image_assets():
    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ Manifest not found: {MANIFEST_PATH}")
        return

    try:
        assets = load_assets(MANIFEST_PATH)
    except Exception as e:
        print(f"❌ Failed to parse manifest: {e}")
        return

    if not assets:
        print("⚠️ Manifest is empty.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for asset in assets:
        filename = asset.get("filename")
        url      = asset.get("url")

        if not filename or not url:
            print(f"⚠️ Skipping invalid entry: {asset}")
            continue

        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            with open(os.path.join(OUTPUT_DIR, filename), "wb") as img:
                img.write(r.content)
            print(f"✅ Saved {filename}")
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")

if __name__ == "__main__":
    batch_download_image_assets()
