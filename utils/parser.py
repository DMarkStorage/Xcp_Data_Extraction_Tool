import re
from typing import List


def get_fileSystem(file):
    """Extract raw filesystem lines from an input report file.

    Scans the file for lines beginning with ``scan`` and returns the text after
    the first occurrence of ``"scan "`` on those lines.

    Args:
        file: Path to the input text report.

    Returns:
        A list of raw filesystem strings found after ``"scan "``.
    """
    file_systems: List[str] = []
    with open(file) as file_handle:
        for line in file_handle:
            pattern = "^scan"
            for _match in re.findall(pattern, line):
                token = "scan "
                _before, _sep, after = line.partition(token)
                file_systems.append(after)
        return file_systems



def get_filer(data):
    """Extract filer identifiers from raw filesystem strings.

    Splits each record on the first colon and returns the leading segment.

    Args:
        data: Raw filesystem strings.

    Returns:
        Filer/controller identifiers.
    """
    filers: List[str] = []
    try:
        for item in data:
            delimiter = ":"
            before, _sep, _after = item.partition(delimiter)
            filers.append(before)
        return filers
    except Exception as e:  # pragma: no cover - mimic original behavior
        print("Error in mountpoint", e)


def get_mountpoint(data):
    """Convert export paths to mountpoints.

    For each record, replaces the first occurrence of ``/export/`` with
    ``/home/`` after the initial colon.

    Args:
        data: Raw filesystem strings.

    Returns:
        Mountpoint strings.
    """
    mountpoints: List[str] = []
    try:
        for item in data:
            delimiter = ":"
            _before, _sep, after = item.partition(delimiter)
            old_prefix = "/export/"
            new_prefix = "/home/"
            mountpoint = after.replace(old_prefix, new_prefix)
            mountpoints.append(mountpoint)
        return mountpoints
    except Exception as e:  # pragma: no cover
        print("Error in mountpoint", e)

def get_extract_path(data):
    """Extract path components following ``/export/``.

    Args:
        data: Raw filesystem strings.

    Returns:
        Extracted path segments following the first ``/export/``.
    """
    extracted_paths: List[str] = []
    try:
        for item in data:
            token = "/export/"
            _before, _sep, after = item.partition(token)
            extracted_paths.append(after)
        return extracted_paths
    except Exception as e:  # pragma: no cover
        print("Error in Extract Path", e)



def get_access(file):
    """Parse access metrics from the input report.

    Looks for lines starting with ``Accessed,`` and splits the trailing portion
    into a list (comma-separated). Only lines where the 10th character is a
    digit are considered (consistent with expected report format).

    Args:
        file: Path to the input text report.

    Returns:
        Per-filesystem access triplets, e.g. ``['12', '3', '4']``.
    """
    access: List[list] = []
    with open(file) as file_handle:
        for line in file_handle:
            pattern = "^Accessed,"
            for _match in re.findall(pattern, line):
                token = "Accessed,"
                digit_check = line[9:10]
                if digit_check.isnumeric():
                    _before, _sep, after = line.partition(token)
                    access_raw = after.strip()
                    access_list = access_raw.split(",")
                    access.append(access_list)
        return access

def get_user(file):
    """Extract owner/user strings from the report.

    Finds lines beginning with ``Top File Owners,``, strips that prefix,
    and collects the remainder unless it is purely numeric.

    Args:
        file: Path to the input text report.

    Returns:
        Owner/username strings.
    """
    users: List[str] = []
    with open(file) as file_handle:
        for line in file_handle:
            marker = "Top File Owners,"
            if marker in line:
                replaced = line.replace(marker, "")
                users_clean = replaced.strip()
                user_fields = users_clean.split(",")
                all_numeric = all(map(str.isnumeric, user_fields))
                if not all_numeric:
                    users.append(users_clean)
    return users

def get_used(file):
    """Collect total space used values from the report.

    Args:
        file: Path to the input text report.

    Returns:
        Raw values (strings) corresponding to ``Total space used,`` lines.
    """
    used: List[str] = []
    with open(file) as file_handle:
        for line in file_handle:
            marker = "Total space used,"
            if marker in line:
                replaced = line.replace(marker, "")
                used.append(replaced)
    return used