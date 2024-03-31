from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import Dataset, Audio
from pyannote.audio import Pipeline
from moviepy.editor import *
import torch
import torchaudio
from pyannote.audio.pipelines.utils.hook import ProgressHook
import re
from speechbox import ASRDiarizationPipeline


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

def write_to_file(text):
    with open('result.txt', 'w') as file:
        file.write(str(text))

def transcribe_voice_record(path):
    audio_dataset = Dataset.from_dict({ "audio": [path] }).cast_column("audio", Audio()) # sampling_rate=16000
    sample = audio_dataset[0]["audio"]

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    result = pipe(sample.copy(), generate_kwargs={"language": "english"}, return_timestamps=True)

    # print(result)
    return result['chunks']

def transform_video_to_wav(path_from, path_to):
    video = VideoFileClip(path_from)
    video.audio.write_audiofile(path_to)

def diarize_speakers(path):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="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",
    )

    pipeline.to(torch.device("cuda"))

    with ProgressHook() as hook:
        waveform, sample_rate = torchaudio.load(path)
        annotation = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook)
        # print(str(annotation))
        return str(annotation)




# transform_video_to_wav("/root/llama2-playground/whishper/coda meeting.mp4", 'output.wav')

def millisec(timeStr):
  spl = timeStr.split(":")
  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
  return s

def whishper_normalize(data):
    print(data)
    normalized_data = []
    for item in data:
        start, end = item['timestamp']
        normalized_data.append({
            "timestamp": (start*1000, (start if end is None else end )*1000),
            "text": item["text"]
        })

    return normalized_data

def group_dz_output(output):
    grouped_data_updated = []
    temp_group = None

    for item in output:
        if temp_group is None or item[2] != temp_group[2]:
            if temp_group is not None:
                grouped_data_updated.append(temp_group)
            temp_group = item
        else:
            temp_group[1] = item[1]

    if temp_group is not None:
        grouped_data_updated.append(temp_group)

    return grouped_data_updated

def parse_dz_output(dz):
    dzList = []
    temp_group = []

    for l in dz:
        start, end = tuple(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', l))
        start = millisec(start)
        end = millisec(end)
        speaker = re.search(r"SPEAKER_\d{2}", l).group()
        dzList.append([start, end, speaker])

    return dzList

def dz_normalize(data):
    dzList = parse_dz_output(data.splitlines())
    return group_dz_output(dzList)


def link_annotation_and_transcription(annotation, transcription):
    data = whishper_normalize(transcription)
    dz = dz_normalize(annotation)
    final_data = []

    for item in data:
        start, end = item["timestamp"]
        added = False

        for dz_item in dz:
            dz_start, dz_end, speaker = dz_item

            if (start >= dz_start and start <= dz_end) or (end >= dz_start and end <= dz_end):
                final_data.append((speaker, item["text"]))
                break
                added = True

        # if not added: print(start, end, item["text"])

    string = ""

    for item in final_data:
        string = string + item[0] + ":" + item[1] + "\n"

    write_to_file(string)
    return final_data


annotation = diarize_speakers('/root/llama2-playground/whishper/output.wav')
transcription = transcribe_voice_record('/root/llama2-playground/whishper/output.wav')

link_annotation_and_transcription(annotation, transcription)
# print(len(test()))
