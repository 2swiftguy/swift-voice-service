from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Optional


def transcribe_audio(data: bytes, model_name: str = "small") -> str:
    """Transcribe audio bytes using faster-whisper.

    The audio content is kept entirely in memory via :class:`io.BytesIO`
    and passed directly to :meth:`WhisperModel.transcribe`.
    """
    from faster_whisper import WhisperModel

    buffer = BytesIO(data)
    model = WhisperModel(model_name)
    segments, _ = model.transcribe(buffer)
    return "".join(segment.text for segment in segments)


def buffer_to_tempfile(buffer: BytesIO, suffix: str = ".wav") -> str:
    """Persist a ``BytesIO`` buffer to a uniquely named temporary file.

    Returns the file path so callers that still require a file on disk can
    access the audio without clobbering other processes.
    """
    with NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(buffer.getvalue())
        return tmp.name
