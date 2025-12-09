from google import genai
import uuid
import os
import json
import yt_dlp
import whisper

def my_hook(d):
    """
    Progress hook used by yt_dlp.
    This function is triggered during the download process.
    It returns the status dictionary only when the download
    has fully finished.
    """
    if d['status'] == 'finished':
        return d

def video_donwload(self,request):
 """
    Downloads the audio track from a given YouTube URL using yt_dlp.
    The audio is saved as an MP3 file with a unique filename.

    Args:
        request: Django REST Framework request containing a 'url' field.

    Returns:
        A tuple containing:
        - audio_path: The file path where the audio was saved.
        - URL: The original YouTube URL.
    """
 URL=request.data.get('url')
 unique_id = uuid.uuid4().hex
 audio_path = f"media/audio_{unique_id}.mp3"
 ydl_opts = { "format": "bestaudio/best",

    "outtmpl": audio_path,

    'verbose': True,

    "noplaylist": True,
    'progress_hooks': [my_hook],
    }
 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download(URL)
 return audio_path,URL

def transcript_video(self,audio_path):
  """
    Generates a transcript from an audio file using the Whisper model.

    Args:
        audio_path: Path to the audio file to be transcribed.

    Returns:
        The transcript text extracted from the audio.
    """
  model = whisper.load_model("tiny")
  result = model.transcribe(audio_path)
  transcript=result["text"]
  return transcript

def build_prompt():
     """
    Builds and returns the prompt text used to instruct the LLM to
    generate a quiz based on a transcript.

    The prompt strictly defines the required JSON structure and
    includes rules such as:
       - exactly 10 questions
       - each with 4 unique answer options
       - a clean JSON output without code fences or explanations

    Returns:
        A formatted string containing the LLM prompt.
    """
     return f"""Based on the following transcript, generate a quiz in valid JSON format.

The quiz must follow this exact structure:

{{

  "title": "Create a concise quiz title based on the topic of the transcript.",

  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",

  "questions": [

    {{

      "question_title": "The question goes here.",

      "question_options": ["Option A", "Option B", "Option C", "Option D"],

      "answer": "The correct answer from the above question_options like Option A and no exact text"

    }},

    ...

    

  ]

}}

Requirements:
-(exactly 10 questions)

- Each question must have exactly 4 distinct answer options.

- Only one correct answer is allowed per question, and it must be present in 'question_options'.

- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).

- Do not include explanations, comments, or any text outside the JSON.
- DO NOT add code fences like ```json.
- DO NOT change the key names.
- DO NOT invent validation messages or reasoning. Only produce the JSON.
           """     


def generate_quiz(self,transcript):
   """
    Generates a 10-question quiz based on the transcript.
    It sends the prompt + transcript to the Gemini model and parses
    the resulting JSON string into a Python dictionary.

    Args:
        transcript: The text transcript extracted from the video/audio.

    Returns:
        A Python dict representing the generated quiz JSON.
    """
   client = genai.Client()
   prompt_text = build_prompt()
   response = client.models.generate_content(
           model="gemini-2.5-flash", contents=prompt_text+transcript,
            
        )
        
   raw_output = response.text.strip()
   raw_output = (
   raw_output.replace("```json", "")
              .replace("```", "")
              .strip())
   quiz_json = json.loads(raw_output)
   return quiz_json