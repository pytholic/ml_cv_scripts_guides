import json
import re

char_remov = ['[', ']', ',']

with open('../sample/sample1/transforms.json', 'r') as f:
    data = json.load(f)

    for frame in data['frames']:
        print(frame['transform_matrix'])
        name = re.split('[/.]', frame['file_path'])[-2]
        
        with open(f'../sample/sample1/pose/{name}.txt', 'w') as f_out:
            for line in frame['transform_matrix']:
                _line = str(line)

                for char in char_remov:
                    _line = _line.replace(char, "")

                f_out.write(_line)
                f_out.write("\n")
