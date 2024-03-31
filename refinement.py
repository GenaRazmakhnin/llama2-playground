from llama.llm import execute_pipeline, load_llm_in_memory

def group_text_by_speaker():
    f = open("./whishper/result.txt", "r")
    text = f.read()
    row_groups = []

    for row in text.split('\n'):
        temp: tuple[str, str] = (row[0:10], row[12:])

        if len(row_groups) > 0:
            last_group = row_groups[-1]
            if last_group[0][0] == temp[0]: last_group.append(temp)
            else: row_groups.append([temp])
        else: row_groups.append([temp])


    return row_groups

def groups_to_text(groups):
    text = ""

    for group in groups:
        text = text + group[0] + ": " + group[1] + "\n"

    return text

def write_to_file(text):
    with open('result.txt', 'w') as file:
        file.write(str(text))

def wrap_with_commands(text):
    return """
    [INST]<<SYS>>Don't explain your results! Don't provide any additional information except answer! Don't extend your answer with any information or text!<</SYS>>
    I provide to you a chunk of the meeting between 2 teams - "Aidbox product team" and "Customer's team". Several people participate this meetine, all of them have own marker SPEAKER_{number} where {number} is unique index for each participant. Each row marked by SPEAKER_{number}, could you by context of conversation to understand which speaker belongs to which team? Answer with the following structure for each unique speaker that is existing in current chunk: SPEAKER_{number}: aidbox team or customer team?
    The meeting itself:\n
    """ + text + "[/INST]"

total = 50

groups = group_text_by_speaker()
pipe = load_llm_in_memory()
current = []

for idx, group in enumerate(groups):
    if len(current) + len(group) > 50:
        print("ITERATION: ", idx + 1, len(current))
        result = execute_pipeline(pipe, wrap_with_commands(groups_to_text(current)))
        current = []

    current = current + group
