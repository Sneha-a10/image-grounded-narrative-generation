import os
import json
from urllib import error, request
from dotenv import load_dotenv

load_dotenv()

"""
sample input text:

"Fujifilm cameras are my favourite DSLRs, their built in film simulations make it so much easier to take pretty photos"

This includes the word "Fujifilm" which is not a usual word in english, this ensures that the model is able to guess the correct way to pronounce words that are unlikely to be in the training set.

"DSLRs" is an abbreveation and is usually pronounced as "dee-es-el-ars" where the final 's' is concatenated with the pronunciation of the letter 'R' while the remaining letters are pronounced individually.

"""


input_text = (
	"Fujifilm cameras are my favourite DSLRs, their built in film simulations "
	"make it so much easier to take pretty photos"
)


"""
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/hpp4J3VqNfWAUOO0d1Us?output_format=mp3_44100_128" \
     -H "xi-api-key: xi-api-key" \
     -H "Content-Type: application/json" \
     -d '{
  "text": "The first move is what sets everything in motion.",
  "model_id": "eleven_flash_v2_5"
}'
"""


def generate_audio(text: str):
	if not text or not text.strip():
		raise ValueError("text must be a non-empty string")

	api_key = os.environ.get("ELEVENLABS_API_KEY")
	if not api_key:
		raise EnvironmentError("ELEVENLABS_API_KEY is not set")

	url = (
		"https://api.elevenlabs.io/v1/text-to-speech/"
		"hpp4J3VqNfWAUOO0d1Us?output_format=mp3_44100_128"
	)
	payload = {
		"text": text.strip(),
		"model_id": "eleven_flash_v2_5",
	}
	body = json.dumps(payload).encode("utf-8")

	req = request.Request(
		url,
		data=body,
		method="POST",
		headers={
			"xi-api-key": api_key,
			"Content-Type": "application/json",
		},
	)

	try:
		with request.urlopen(req) as response:
			audio_bytes = response.read()
	except error.HTTPError as exc:
		error_body = exc.read().decode("utf-8", errors="replace")
		raise RuntimeError(
			f"ElevenLabs API request failed ({exc.code}): {error_body}"
		) from exc
	except error.URLError as exc:
		raise RuntimeError(f"Failed to reach ElevenLabs API: {exc.reason}") from exc

	output_path = "output.mp3"
	with open(output_path, "wb") as file:
		file.write(audio_bytes)

	return output_path
	
	

if __name__ == "__main__":
	generate_audio(input_text)
	

