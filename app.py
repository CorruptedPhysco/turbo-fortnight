from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch the video link
def get_video_link(url):
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the video link using the JWPlayer setup
        script_tags = soup.find_all('script')
        for script in script_tags:
            if "jwplayer" in script.text and "file" in script.text:
                # Extract the video link from the script
                start_index = script.text.find('file: "') + len('file: "')
                end_index = script.text.find('",', start_index)
                video_link = script.text[start_index:end_index]
                return video_link

        return None
    except requests.exceptions.RequestException as e:
        return None

# Flask route to get the video link
@app.route('/get-video-link', methods=['GET'])
def fetch_video_link():
    # Default URL if no parameter is provided
    default_url = "https://www.kaduvatv.cam/page-34/10/Geetha-Govindam-Serial.html"

    # Get the URL parameter (if provided)
    url = request.args.get('url', default_url)

    # Fetch the video link
    video_link = get_video_link(url)

    # Return the result as JSON
    if video_link:
        return jsonify({"success": True, "video_link": video_link})
    else:
        return jsonify({"success": False, "message": "Video link not found or an error occurred."})

# Main entry point
if __name__ == '__main__':
    # Note: debug=True is not recommended for production
    app.run(debug=True)
