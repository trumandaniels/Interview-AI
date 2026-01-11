import io
from faster_whisper import WhisperModel

model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(audio_file):
    """
    Transcribes audio using faster-whisper.
    
    Args:
        audio_file: Can be a file path (str), a file-like object, or raw bytes.
    """
    
    # If the input is raw bytes (like from streamlit audio_recorder), wrap it in BytesIO
    if isinstance(audio_file, bytes):
        audio_file = io.BytesIO(audio_file)
    
    # transcribe() returns a generator, so we iterate to get the text segments
    segments, info = model.transcribe(audio_file, beam_size=5)
    transcription = " ".join([segment.text for segment in segments])
    return transcription.strip()