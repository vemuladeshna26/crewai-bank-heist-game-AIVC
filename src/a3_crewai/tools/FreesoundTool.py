# src/a3/tools/FreesoundTool.py
import os
import requests
import json # Import json
from crewai.tools.base_tool import BaseTool
from typing import Optional

class FreesoundTool(BaseTool):
    api_key: Optional[str]
    output_dir: str

    def __init__(self, api_key: Optional[str] = None, output_dir: str = "output/sounds"):
        effective_api_key = "" #Enter the API key
        super().__init__(
            name="freesound",
            description="Download audio from Freesound.org. Input should be a dictionary with 'query', optional 'license_filter' (default 'Creative Commons 0'), and optional 'filename'. Returns JSON status.",
            api_key=effective_api_key,
            output_dir=output_dir
        )
        # Ensure 'sounds' dir exists relative to where script is run
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"FreesoundTool initialized. Output directory: {os.path.abspath(self.output_dir)}") # Debug print
        if not self.api_key:
            print("Warning: FreesoundTool initialized without API key.")

    def _run(self, query: str, license_filter: str = "Creative Commons 0", filename: Optional[str] = None) -> str:
        """
        Downloads audio from Freesound. Returns a JSON string indicating success/failure and path/error.
        Args:
            query: Search term for the sound.
            license_filter: Freesound license filter (default: "Creative Commons 0").
            filename: Optional desired filename (e.g., 'explosion.mp3'). If None, generated from query.
        Returns:
            JSON string: {"success": true, "path": "path/to/sound.mp3", "license": "license_info"} or {"success": false, "error": "error message"}
        """
        if not self.api_key:
            error_msg = "Freesound API key is missing. Cannot perform search."
            print(f"Error: {error_msg}")
            return json.dumps({"success": False, "error": error_msg})

        if not filename:
            safe_query = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in query).rstrip()
            filename = f"{safe_query[:50].replace(' ', '_')}.mp3"

        full_path = os.path.abspath(os.path.join(self.output_dir, filename))
        print(f"FreesoundTool: Attempting to download sound for query '{query}' to '{filename}'") # Debug print

        try:
            resp = requests.get(
                "https://freesound.org/apiv2/search/text/",
                params={
                    "query": query, "token": self.api_key, "filter": f'license:"{license_filter}"',
                    "fields": "id,name,previews,license", "sort": "rating_desc"},
                headers={'User-Agent': 'CrewAI FreesoundTool/1.1'}, # Updated user agent slightly
                timeout=30 # Add timeout
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])

            if not results:
                error_msg = f"No Freesound results found for query='{query}' with license='{license_filter}'."
                print(f"Warning: {error_msg}")
                return json.dumps({"success": False, "error": error_msg})

            sound_info = results[0]
            previews = sound_info.get("previews", {})
            download_url = previews.get("preview-hq-mp3") or previews.get("preview-lq-mp3")
            license_info = sound_info.get('license', 'Unknown')

            if not download_url:
                 error_msg = f"No preview URL found for sound ID {sound_info.get('id', 'N/A')} ('{sound_info.get('name', 'N/A')}')."
                 print(f"Warning: {error_msg}")
                 return json.dumps({"success": False, "error": error_msg})

            print(f"FreesoundTool: Downloading from {download_url}...")
            clip_resp = requests.get(download_url, headers={'User-Agent': 'CrewAI FreesoundTool/1.1'}, timeout=60)
            clip_resp.raise_for_status()

            print(f"FreesoundTool: Saving sound to {full_path}")
            with open(full_path, "wb") as f:
                f.write(clip_resp.content)

            print(f"FreesoundTool: Success. Sound saved to {full_path}")
            return json.dumps({"success": True, "path": full_path, "license": license_info})

        except requests.exceptions.RequestException as e:
            error_msg = f"FreesoundTool: API request error for query '{query}': {e}"
            print(f"Error: {error_msg}")
            return json.dumps({"success": False, "error": error_msg})
        except IOError as e:
            error_msg = f"FreesoundTool: File saving error for '{filename}': {e}"
            print(f"Error: {error_msg}")
            return json.dumps({"success": False, "error": error_msg})
        except Exception as e:
            error_msg = f"FreesoundTool: Unexpected error for query '{query}': {e}"
            print(f"Error: {error_msg}")
            return json.dumps({"success": False, "error": error_msg})