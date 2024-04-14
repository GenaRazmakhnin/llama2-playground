import re
from annotation import normalize_annotation

def write_to_file(file, text):
    with open(file, 'w') as file:
        file.write(str(text))

transcriptions =  []
annotations = normalize_annotation(open("/Users/gena.razmakhnin/Documents/unknown/project/a.txt", "r").read())

def fuse_annotation_and_transcription(annotations, transcriptions):
    data = []

    for transcription_item in transcriptions:
        transcription_item_start = transcription_item["timestamp"][0] * 1000
        transcription_item_end  = transcription_item["timestamp"][1] * 1000

        for annotation_item in annotations:
            annotation_item_start, annotation_item_end, speaker = annotation_item

            if (transcription_item_start >= annotation_item_start and transcription_item_start <= annotation_item_end) or (transcription_item_end >= annotation_item_start and transcription_item_end <= annotation_item_end):
                data.append((speaker, transcription_item["text"]))
                break

    text = "" 
    temp_string = ""
    speaker = None

    for item in data:
        if speaker is None: speaker = item[0]
        
        if speaker == item[0]:
            temp_string = temp_string + item[1]
        else:  
            text = text + speaker + ": " + temp_string + "\n"
            speaker = item[0]
            temp_string = item[1]

    return text


write_to_file("done.txt", fuse_annotation_and_transcription(annotations, transcriptions));

# def group_by_speaker():
#     row_groups = []

#     for row in text.split('\n'):
#         temp: tuple[str, str] = (row[0:10], row[12:])

#         if len(row_groups) > 0:
#             last_group = row_groups[-1]
#             if last_group[0][0] == temp[0]: last_group.append(temp)
#             else: row_groups.append([temp])
#         else: row_groups.append([temp])


#     return row_groups

# def groups_to_text(groups):
#     text = ""

#     for group in groups:
#         text = text + group[0] + ": " + group[1] + "\n"

#     return text



# for item in data:
#     string = item["text"].strip()
    
    # def whishper_normalize(data):
    # print(data)
    # normalized_data = []
    # for item in data:
    #     start, end = item['timestamp']
    #     normalized_data.append({
    #         "timestamp": (start*1000, (start if end is None else end )*1000),
    #         "text": item["text"]
    #     })

    # return normalized_data