import re

def millisec(timeStr):
  spl = timeStr.split(":")
  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])) * 1000)
  return s

def group_output(output):
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

def parse_output(output):
    list = []

    for line in output:
        start, end = tuple(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', line))
        start = millisec(start)
        end = millisec(end)
        speaker = re.search(r"SPEAKER_\d{2}", line).group()
        list.append([start, end, speaker])

    return list

def normalize_annotation(text: str):
    return group_output(parse_output(text.splitlines()))