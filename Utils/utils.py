import data_mapping as dm
import os
from datetime import datetime


# def get_data(file_path, field_names=None):
#     """
#     Reads a pipe-delimited file and returns a dictionary with field names as keys,
#     stripping leading/trailing spaces from values. Also constructs a fund table
#     under the key 'WS-FUND-TABLE'.
#     """
#     if not field_names:
#         field_names = dm.mapping_order_for_delimited_file

#     data_list = []
#     with open(file_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             line = line.strip()
#             if not line:
#                 continue
#             values = line.split('|')
#             record = {field: values[i].strip() if i < len(values) else None for i, field in enumerate(field_names)}
#             data_list.append(record)

#     # Process first (and usually only) record
#     data = get_data_dict(data_list[0])

#     # Extract NUMBER-OF-FUNDS
#     num_of_funds = int(data.get("NUMBER-OF-FUNDS", "0") or 0)
#     if num_of_funds > 0:
#         # Locate index of NUMBER-OF-FUNDS field
#         num_index = field_names.index("NUMBER-OF-FUNDS")

#         # Each fund has two entries: number and name
#         start_index = num_index + 4  # skip RETURN_BY_MMDD, EARLIEST-FMO, EARLIEST-RATE
#         # funds occupy 2 * num_of_funds fields after NUMBER-OF-FUNDS
#         fund_entries = values[start_index : start_index + (num_of_funds * 2)]

#         # Build fund list as pairs
#         fund_pairs = [
#             (fund_entries[i], fund_entries[i + 1]) 
#             for i in range(0, len(fund_entries), 2)
#         ]

#         # Build 5-column table (2 records per row)
#         ws_fund_table = []
#         for i in range(0, len(fund_pairs), 2):
#             left = fund_pairs[i]
#             right = fund_pairs[i + 1] if i + 1 < len(fund_pairs) else ("", "")
#             ws_fund_table.append([
#                 "____", left[0].strip(), left[1].strip(), "","____", right[0].strip(), right[1].strip()
#             ])
#         data["WS-FUND-TABLE"] = ws_fund_table
#     else:
#         data["WS-FUND-TABLE"] = []

#     return data

# def get_data_dict(data):
#     """Normalize dictionary keys to uppercase."""
#     if data is None:
#         raise ValueError("Data dictionary is required for PDF generation.")
#     raw_data = {k.upper(): v for k, v in data.items()}
#     return raw_data


def get_data(file_path, field_names=None):
    """
    Reads a pipe-delimited file and returns a list of data dictionaries (one per record),
    stripping spaces and building the WS-FUND-TABLE for each policy.
    """
    if not field_names:
        field_names = dm.mapping_order_for_delimited_file  # from your mapping config

    all_data = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            values = line.split('|')
            record = {
                field: values[i].strip() if i < len(values) else ""
                for i, field in enumerate(field_names)
            }

            # Normalize and process fund data
            data = get_data_dict(record)

            num_of_funds = int(data.get("NUMBER-OF-FUNDS", "0") or 0)
            ws_fund_table = []

            if num_of_funds > 0:
                # Locate NUMBER-OF-FUNDS field index
                num_index = field_names.index("NUMBER-OF-FUNDS")

                # Each fund has two entries: number and name
                start_index = num_index + 4  # skip RETURN_BY_MMDD, EARLIEST-FMO, EARLIEST-RATE
                fund_entries = values[start_index : start_index + (num_of_funds * 2)]

                # Create fund pairs (fund_code, fund_name)
                fund_pairs = [
                    (fund_entries[i].strip(), fund_entries[i + 1].strip())
                    for i in range(0, len(fund_entries), 2)
                ]

                # Build 5-column WS-FUND-TABLE (2 pairs per row)
                for i in range(0, len(fund_pairs), 2):
                    left = fund_pairs[i]
                    right = fund_pairs[i + 1] if i + 1 < len(fund_pairs) else ("", "")
                    ws_fund_table.append([
                        "____", left[0], left[1], "",
                        "____", right[0], right[1]
                    ])

            data["WS-FUND-TABLE"] = ws_fund_table
            all_data.append(data)

    return all_data


def get_data_dict(data):
    """Normalize dictionary keys to uppercase."""
    if data is None:
        raise ValueError("Data dictionary is required for PDF generation.")
    return {k.upper(): v for k, v in data.items()}




def get_unique_filename(data):
    output_dir = "Resource\\Output"

    # ✅ Handle case where a string (filename) is passed instead of a dict
    if isinstance(data, str):
        filename = data
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        base = os.path.join(output_dir, os.path.splitext(os.path.basename(filename))[0])
        ext = os.path.splitext(filename)[1] or ".pdf"
        counter = 1
        new_filename = f"{base}{ext}"

        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1

        return new_filename

    # ✅ Normal case: data is a dictionary
    ind = data.get('LETTER-IND', "")
    policy_number = data.get('CONTRACT-NUMBER', "")
    copy_ind = data.get('COPY-IND', "")

    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Determine letter indicator
    if ind == "FM":
        letter_ind = "FMO"
    elif ind == "GR":
        letter_ind = "GIRO"
    else:
        letter_ind = ""

    filename = f"{letter_ind}_{copy_ind}_{policy_number}_{current_timestamp}.pdf"

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




