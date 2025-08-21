import os
import ffmpeg
import math
from sarvamai import SarvamAI
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")
MODEL = os.getenv("MODEL", "saarika:v2.5")
CHUNK_DURATION_SECONDS = int(os.getenv("CHUNK_DURATION_SECONDS", 30))

client = SarvamAI(api_subscription_key=API_KEY)

def get_audio_duration(audio_path):
    probe = ffmpeg.probe(audio_path)
    return float(probe['format']['duration'])

def split_audio(audio_path, chunk_duration=CHUNK_DURATION_SECONDS):
    duration = get_audio_duration(audio_path)
    num_chunks = math.ceil(duration / chunk_duration)
    chunk_paths = []
    for i in range(num_chunks):
        start_time = i * chunk_duration
        output_chunk = f"chunk_{i}.wav"
        (
            ffmpeg
            .input(audio_path, ss=start_time, t=chunk_duration)
            .output(output_chunk, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
        chunk_paths.append(output_chunk)
    return chunk_paths

def transcribe_chunk(chunk_path):
    with open(chunk_path, "rb") as f:
        response = client.speech_to_text.transcribe(
            file=f,
            model=MODEL,
            language_code="unknown"
        )
    return getattr(response, "transcript", "").strip()

def translate_to_english(text):
    if not text.strip():
        return ""
    return GoogleTranslator(source="auto", target="en").translate(text)

def transcribe_audio(audio_path, save_to_file=True):
    chunk_files = split_audio(audio_path)
    all_english_texts = []

    for chunk in chunk_files:
        print(f"🎙️ Transcribing {chunk}")
        try:
            original_text = transcribe_chunk(chunk)
            english_text = translate_to_english(original_text)
            all_english_texts.append(english_text)
        except Exception as e:
            print(f"❌ Error: {e}")
            all_english_texts.append("")
        finally:
            if os.path.exists(chunk):
                os.remove(chunk)

    if not any(all_english_texts):
        all_english_texts = ["No transcription available"]

    if save_to_file:
        transcript_path = os.path.splitext(audio_path)[0] + "_english_transcript.txt"
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write("\n".join(all_english_texts))

    return all_english_texts
