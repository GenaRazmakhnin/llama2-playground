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


    list2 = None
    
    for index, line in enumerate(list):
        if list2 is None: list2 = [[0, line[1], line[2]]]; continue;

        if list2[-1][2] == line[2]: list2.append(line)
        elif list2[-1][2] == list[index + 1][2] and line[1] - line[0] < 1000: continue;
        else: list2.append(line)

    result = None
    
    for line in list2:
        if result is None: result = [line]; continue;
        
        if result[-1][2] == line[2]: result[-1][1] = line[1]
        else: result.append(line)
    
    return result

def normalize_annotation(text: str):
    return group_output(parse_output(text.splitlines()))