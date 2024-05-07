from whishper.model import transform_video_to_wav, diarize_speakers, transcribe_voice_record
from fusion_sentence import combine_words_into_sentence, fuse, replace_aidbox, write_to_file
from annotation import normalize_annotation

transform_video_to_wav("/root/coda meeting.mp4", 'output.wav')

annotation = diarize_speakers('/root/llama2-playground/output.wav')
transcription = transcribe_voice_record('/root/llama2-playground/output.wav')

write_to_file(
    "done.txt", 
    replace_aidbox(fuse(normalize_annotation(annotation), combine_words_into_sentence(transcription)))
)