from pathlib import Path
import subprocess
import tempfile
import logging
from . import stt_service
from ..config import DEFAULT_WHISPER_MODEL

logger = logging.getLogger("omnisia.video")


def extract_audio_from_video(
    video_path: Path, output_path: Path = None, format: str = "wav"
) -> Path:
    """Extrai áudio de um arquivo de vídeo"""
    try:
        logger.info(f"Extraindo áudio do vídeo: {video_path}")

        if not output_path:
            output_path = video_path.parent / f"{video_path.stem}.{format}"

        # Comando ffmpeg para extrair áudio
        cmd = [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vn",  # Sem vídeo
            "-acodec",
            "pcm_s16le" if format == "wav" else "libmp3lame",
            "-ar",
            "16000",  # Sample rate para Whisper
            "-ac",
            "1",  # Mono
            "-y",  # Sobrescrever arquivo existente
            str(output_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Erro no ffmpeg: {result.stderr}")

        logger.info(f"Áudio extraído para: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Erro ao extrair áudio: {str(e)}")
        raise Exception(f"Erro ao extrair áudio do vídeo: {str(e)}")


def transcribe_video(
    video_path: Path, model_size: str = None, extract_audio: bool = True
) -> dict:
    """Transcreve vídeo para texto extraindo o áudio"""
    try:
        model_size = model_size or DEFAULT_WHISPER_MODEL
        logger.info(f"Transcrevendo vídeo: {video_path} com modelo {model_size}")

        # Cria arquivo temporário para o áudio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio_path = Path(temp_audio.name)

        try:
            # Extrai áudio do vídeo
            audio_path = extract_audio_from_video(video_path, temp_audio_path)

            # Transcreve o áudio
            transcription_result = stt_service.transcribe_audio(
                audio_path, model_size=model_size
            )

            # Adiciona informações do vídeo
            video_info = get_video_info(video_path)

            result = {
                **transcription_result,
                "video_file": str(video_path),
                "video_info": video_info,
                "audio_extracted": True,
                "temp_audio_path": str(audio_path) if not extract_audio else None,
            }

            logger.info(
                f"Transcrição de vídeo concluída. Texto: {len(result['text'])} caracteres"
            )
            return result

        finally:
            # Remove arquivo temporário se necessário
            if extract_audio and temp_audio_path.exists():
                temp_audio_path.unlink()
                logger.info("Arquivo de áudio temporário removido")

    except Exception as e:
        logger.error(f"Erro na transcrição de vídeo: {str(e)}")
        raise Exception(f"Erro na transcrição de vídeo: {str(e)}")


def get_video_info(video_path: Path) -> dict:
    """Obtém informações sobre o arquivo de vídeo"""
    try:
        logger.info(f"Obtendo informações do vídeo: {video_path}")

        # Comando ffprobe para obter informações
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Erro no ffprobe: {result.stderr}")

        import json

        data = json.loads(result.stdout)

        # Extrai informações relevantes
        format_info = data.get("format", {})
        video_stream = None
        audio_stream = None

        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video" and not video_stream:
                video_stream = stream
            elif stream.get("codec_type") == "audio" and not audio_stream:
                audio_stream = stream

        info = {
            "filename": video_path.name,
            "size_bytes": int(format_info.get("size", 0)),
            "duration": float(format_info.get("duration", 0)),
            "bitrate": int(format_info.get("bit_rate", 0)),
            "format_name": format_info.get("format_name", ""),
        }

        if video_stream:
            info["video"] = {
                "codec": video_stream.get("codec_name", ""),
                "width": video_stream.get("width", 0),
                "height": video_stream.get("height", 0),
                "fps": eval(video_stream.get("r_frame_rate", "0/1")),
                "bitrate": int(video_stream.get("bit_rate", 0)),
            }

        if audio_stream:
            info["audio"] = {
                "codec": audio_stream.get("codec_name", ""),
                "sample_rate": int(audio_stream.get("sample_rate", 0)),
                "channels": int(audio_stream.get("channels", 0)),
                "bitrate": int(audio_stream.get("bit_rate", 0)),
            }

        return info

    except Exception as e:
        logger.error(f"Erro ao obter informações do vídeo: {str(e)}")
        return {"filename": video_path.name, "error": str(e)}


def convert_video_format(
    input_path: Path, output_path: Path, target_format: str = "mp4"
) -> Path:
    """Converte vídeo para outro formato"""
    try:
        logger.info(f"Convertendo vídeo {input_path} para {target_format}")

        # Configurações baseadas no formato
        if target_format.lower() == "mp4":
            codec_args = ["-c:v", "libx264", "-c:a", "aac", "-crf", "23"]
        elif target_format.lower() == "webm":
            codec_args = ["-c:v", "libvpx-vp9", "-c:a", "libopus"]
        else:
            codec_args = ["-c:v", "copy", "-c:a", "copy"]  # Apenas recontainer

        cmd = [
            "ffmpeg",
            "-i",
            str(input_path),
            *codec_args,
            "-y",  # Sobrescrever
            str(output_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Erro na conversão: {result.stderr}")

        logger.info(f"Vídeo convertido para: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Erro na conversão de vídeo: {str(e)}")
        raise Exception(f"Erro na conversão de vídeo: {str(e)}")


def extract_frames(
    video_path: Path, output_dir: Path, fps: float = 1.0, format: str = "jpg"
) -> list:
    """Extrai frames do vídeo"""
    try:
        logger.info(f"Extraindo frames do vídeo: {video_path}")

        output_dir.mkdir(parents=True, exist_ok=True)

        # Padrão de nome dos arquivos
        output_pattern = output_dir / f"frame_%04d.{format}"

        cmd = [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            f"fps={fps}",
            "-y",
            str(output_pattern),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Erro na extração de frames: {result.stderr}")

        # Lista arquivos criados
        frames = sorted(output_dir.glob(f"frame_*.{format}"))

        logger.info(f"Extraídos {len(frames)} frames")
        return [str(frame) for frame in frames]

    except Exception as e:
        logger.error(f"Erro na extração de frames: {str(e)}")
        raise Exception(f"Erro na extração de frames: {str(e)}")


def check_ffmpeg_available() -> bool:
    """Verifica se o ffmpeg está disponível"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_supported_formats() -> dict:
    """Retorna formatos suportados pelo ffmpeg"""
    if not check_ffmpeg_available():
        return {"error": "FFmpeg não disponível"}

    try:
        # Obtém formatos de entrada
        result = subprocess.run(["ffmpeg", "-formats"], capture_output=True, text=True)

        formats = {"input": [], "output": [], "video_codecs": [], "audio_codecs": []}

        # Parse básico da saída do ffmpeg
        lines = result.stdout.split("\n")
        in_formats_section = False

        for line in lines:
            line = line.strip()
            if "File formats:" in line:
                in_formats_section = True
                continue

            if in_formats_section and line.startswith("--"):
                break

            if in_formats_section and line:
                parts = line.split()
                if len(parts) >= 3:
                    flags = parts[0]
                    format_name = parts[1]

                    if "D" in flags:  # Demuxing (input)
                        formats["input"].append(format_name)
                    if "E" in flags:  # Muxing (output)
                        formats["output"].append(format_name)

        return formats

    except Exception as e:
        logger.error(f"Erro ao obter formatos suportados: {str(e)}")
        return {"error": str(e)}
