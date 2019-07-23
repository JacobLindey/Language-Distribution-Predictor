"""
    Saves data from ldp simulator to various output media.

    ./data/data_saver.py
    ldp.data.data_server

    author: Jacob Lindey
    created: 7-22-2019
    updated: 7-22-2019
"""

def export_to_file(file_location: str, data: dict):
    """
        Saves data from ldp simulator to various output files.

        Args:
            file_location (str): a file location without a file extension. All
                files saved will have this name with different file extensions.
            data (dict, pandas.DataFrame): The data to be exported. Keys
                will be used to label output in some cases.
    """
    # Open files
    txt_file = open(file_location + ".txt", 'w+')
    csv_file = open(file_location + ".csv", 'w+')

    # Write files
    for k, d in data.items():

        # Data headers
        txt_file.write(k + ':\n')
        csv_file.write(k + '\n')

        # Data bodies
        txt_file.write(d.to_string())
        csv_file.write(d.to_csv())

        # Data Seperators
        txt_file.write('\n\n')
        csv_file.write('\n')

    # Close files
    txt_file.close()
    csv_file.close()
