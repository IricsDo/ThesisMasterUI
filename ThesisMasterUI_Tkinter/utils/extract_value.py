import re
import random

def extract_value_from_log(string : str) -> int:
    # Regular expression to match the specific format
    match = re.search(r"<update_process_ui>(\d+)</>", string)
    if match:
        value = int(match.group(1))
        return value
    return -1