import re
from annotation import normalize_annotation

def write_to_file(file, text):
    with open(file, 'w') as file:
        file.write(str(text))

transcriptions =  []

annotations = normalize_annotation(
    open("/Users/gena.razmakhnin/Documents/unknown/project/a.txt", "r").read()
)

def attach_word(text, word):
    if word[0] in ["-"]: return text + word
    
    return text + " " + word
    
def combine_words_into_sentence(transcriptions):
    data = [{ "items": []}]

    for transcription_item in transcriptions:
        text = transcription_item["text"].strip()
        start, end = transcription_item["timestamp"]

        data[-1]["items"].append({ "text": text, "timestamp": [start * 1000, end * 1000] })

        if text[-1] in [".", "?", "!", ";"]: data.append({ "items": []})
    
    return data

def reduce_speakers(speakers):
    speaker_result = None

    for speaker in speakers:
        if speaker_result is None: speaker_result = speaker
        if speaker["piece"] > speaker_result["piece"]: speaker_result = speaker
    
    return speaker_result["speaker"]

def fuse(annotations, transcriptions):
    for transcription_item in transcriptions:
        if len(transcription_item["items"]) == 0: continue
        start = transcription_item["items"][0]["timestamp"][0]
        end = transcription_item["items"][-1]["timestamp"][1]
        diff = end - start
        one_percent = diff / 100
        transcription_item["speakers"] = []

        for annotation_item in annotations:
            annotation_item_start, annotation_item_end, speaker = annotation_item

            if start <= annotation_item_start and annotation_item_end <= end:
                transcription_item["speakers"].append({
                    "speaker": speaker,
                    "piece": round((annotation_item_end - annotation_item_start) / one_percent)
                })
            
            if start >= annotation_item_start and annotation_item_end > start and annotation_item_end < end:
                transcription_item["speakers"].append({
                    "speaker": speaker,
                    "piece": round((annotation_item_end - start) / one_percent)
                })

            if start < annotation_item_start and annotation_item_start < end and annotation_item_end >= end:
                transcription_item["speakers"].append({
                    "speaker": speaker,
                    "piece": round((end - annotation_item_start) / one_percent)
                })

            if start > annotation_item_start and annotation_item_end > end:
                transcription_item["speakers"].append({
                    "speaker": speaker,
                    "piece": round((end - start) / one_percent)
                })


    text = ""
    transcriptions = transcriptions[:-1]
    
    for idx, transcription in enumerate(transcriptions):
        if len(transcription["speakers"]) == 0: continue
        
        if len(transcription["speakers"]) == 1:
            text = text + transcription["speakers"][0]["speaker"]
            for item in transcription["items"]:
                text = attach_word(text, item["text"])
        
        else:
            text = text + reduce_speakers(transcription["speakers"])
            for item in transcription["items"]:
                text = attach_word(text, item["text"])

        text = text + "\n"

    return text

def replace_aidbox(text):
    patterns = [
        r"8boxes", r"8box", r"a boxes", r"a box", r"aid boxes", r"aid box", r"8-boxes", r"8-box", r"eight boxes", r"eight box", r"aboxes", r"abox",  r"a-boxes", r"a-box"
    ]
    
    for pattern in patterns:
        text = re.compile(pattern, re.IGNORECASE).sub('Aidbox', text)
    
    return text


write_to_file(
    "done.txt", 
    replace_aidbox(fuse(annotations, combine_words_into_sentence(transcriptions)))
)
