import data_mapping as dm
import os

def get_data(file_path, field_names=None):
    """
    Reads a pipe-delimited file and returns a list of dictionaries with field names as keys,
    stripping leading/trailing spaces from values.
    """
    if not field_names:
        field_names = dm.mapping_order_for_delimited_file
        
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = line.split('|')
            record = {field: values[i].strip() if i < len(values) else None for i, field in enumerate(field_names)}
            data_list.append(record)
    return data_list


def get_unique_filename(filename):
    output_dir = "Resource\Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    base = os.path.join(output_dir, os.path.splitext(os.path.basename(filename))[0])
    ext = os.path.splitext(filename)[1]
    counter = 1
    new_filename = f"{base}{ext}"
    while os.path.exists(new_filename):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename



def fixed_width(value, length, align='left'):
    """Truncate or pad a value to the exact fixed width.

    Args:
        value: value to format (None -> blank)
        length: integer length in characters
        align: 'left' or 'right' (padding side)
    Returns:
        fixed-width string of exactly `length` characters
    """
    if value is None:
        s = ''
    else:
        s = str(value)
    # remove newlines
    s = s.replace('\n', ' ').replace('\r', ' ')
    if len(s) > length:
        return s[:length]
    if align == 'right':
        return s.rjust(length)
    return s.ljust(length)

def get_raw_data(data):
    if data is None:
        raise ValueError("Data dictionary is required for PDF generation.")

    raw_data = {k.upper(): v for k, v in data.items()}
    return raw_data


