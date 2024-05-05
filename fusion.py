import re
from annotation import normalize_annotation

def write_to_file(file, text):
    with open(file, 'w') as file:
        file.write(str(text))

transcriptions =  []
annotations = normalize_annotation(open("/Users/gena.razmakhnin/Documents/unknown/project/a.txt", "r").read())

def is_tail(word: str):
    return not word.isupper() and word[-1] in ["?", ".", "!", ";"]

def is_head(word: str):
    return word[1].isupper()

def fuse_annotation_and_transcription(annotations, transcriptions):
    data = []
    zero_group = []

    for transcription_item in transcriptions:
        is_collected = False
        transcription_item_start = transcription_item["timestamp"][0] * 1000
        transcription_item_end  = transcription_item["timestamp"][1] * 1000

        for annotation_item in annotations:
            annotation_item_start, annotation_item_end, speaker = annotation_item

            if (
                transcription_item_start >= annotation_item_start and 
                transcription_item_start <= annotation_item_end
            ) and (
                transcription_item_end >= annotation_item_start and 
                transcription_item_end <= annotation_item_end
            ):
                is_collected = True
                zero_group.append(transcription_item)
                data.append((speaker, transcription_item["text"]))
                break
    
        if (not is_collected and is_tail(transcription_item["text"])):
            is_collected = True
            zero_group.append(transcription_item)
            data.append((data[-1][0], transcription_item["text"]))

        if (not is_collected and is_head(transcription_item["text"])):
            is_collected = True
            zero_group.append(transcription_item)
            data.append((None, transcription_item["text"]))

    for idx, transcription_item in enumerate(transcriptions):
        if (not transcription_item in zero_group):
            print(transcription_item["text"])

    text = "" 
    temp_string = ""
    speaker = None

    for item in data:
        if speaker is None: speaker = item[0]
        if item[0] is None: continue
        
        if speaker == item[0]:
            temp_string = temp_string + item[1]
        else: 
            text = text + speaker + ": " + temp_string + "\n"
            speaker = item[0]
            temp_string = item[1]

    return text


write_to_file("done.txt", fuse_annotation_and_transcription(annotations, transcriptions));
