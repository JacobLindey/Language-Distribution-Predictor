"""
    Saves data from ldp simulator to various output media.

    ./data/data_saver.py
    ldp.data.data_server

    author: Jacob Lindey
    created: 7-22-2019
    updated: 7-22-2019
"""

def save_to_file(file_location: str, data: dict):
    file = open(file_location, 'w+')
    for k, d in data.items():
        file.write(k + ':\n')
        file.write(d.to_string())
        file.write('\n\n')
    file.close()
