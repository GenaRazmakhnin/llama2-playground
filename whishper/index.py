import time
import json
from model import transcribe_voice_record, link_annotation_and_transcription

import sys
import os
# sys.path.insert(0, '/home/ec2-user')

def transcription_handler(params):
    data = transcribe_voice_record(params['path'])
    result = link_annotation_and_transcription(params['annotation'], data)

    result_2 = []
    for item in result:
        result_2.append(item[0] + ": " + item[1])

    return { 'text': "\n".join(result_2) }



