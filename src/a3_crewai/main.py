import sys
import yaml
from a3_crewai.crew import GameBuilderCrew
sys.stdout.reconfigure(line_buffering=True)
import os
import requests
import json

def batch_download_image_assets():
    images_json_path = "./output/images/manifest.json"  # Or wherever your manifest is

    if os.path.exists(images_json_path):

        with open(images_json_path, "r") as f:
            manifest = json.load(f)

        assets = manifest.get("assets", [])

        if not assets:
            print("⚠️ No assets found in the manifest!")
            return

        os.makedirs("output/images", exist_ok=True)

        for asset in assets:
            filename = asset.get("filename")
            url = asset.get("url")

            if not filename or not url:
                print(f"⚠️ Skipping invalid entry: {asset}")
                continue

            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    image_path = os.path.join("output/images", filename)
                    with open(image_path, "wb") as img_file:
                        img_file.write(response.content)
                    print(f"✅ Image saved: {filename}")
                else:
                    print(f"⚠️ Failed to download {filename}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Error downloading {filename}: {e}")

    else:
        print("❌ Manifest file not found at:", images_json_path)

def run():
    print("## Welcome to the Game Crew")
    print('-------------------------------')

    # Load game design instructions from gamedesign.yaml
    with open('src/a3_crewai/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
        gamedesign = yaml.safe_load(file)

    # Load the game template from the templates folder
    with open('src/a3_crewai/config/gametemplate.html', 'r', encoding='utf-8') as template_file:
        template = template_file.read()

    # Prepare inputs using {game} and {template}
    inputs = {
        'game_title': "Bank Heist",
        'input_path': gamedesign['bank_heist'],  # Generic instructions for a stealth and card-based game
        'template_path': template
    }

    # Kick off the Crew pipeline, chaining outputs from each task
    final_game_code = GameBuilderCrew().crew().kickoff(inputs=inputs)

    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("Final HTML code for the game:")
    print(final_game_code)
    batch_download_image_assets()

if __name__ == "__main__":
    run()
