import math
import pandas as pd
import os
from tabulate import tabulate


# All data aggregation and output function
def convert_size(size_bytes):
    """Convert a byte count into a human-readable size string.

    Example:
        1536 -> ``"1.5 KB"``

    Args:
        size_bytes: Size value in bytes.

    Returns:
        Human-readable size with units.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def df_table(df, max_rows: int = 10):
    """
    Display a formatted preview of a DataFrame as a readable table.

    This function prints the first few rows of a DataFrame in a clean,
    grid-styled table format using the `tabulate` library. It helps users
    quickly inspect data in the console without displaying the full dataset.

    Example:
        === Filesystem Report (showing first 2 of 2 rows) ===
        +----------+---------------+-------------+
        | Filer    | Filesystem    | Total Used  |
        +----------+---------------+-------------+
        | filerA   | /home/project1| 1.0 MB      |
        | filerB   | /home/project2| 5.0 MB      |
        +----------+---------------+-------------+

    """
    df = df.head(max_rows)
    print(f"\n=== Filesystem Report (showing first {len(df)} of {len(df)} rows) ===")
    print(tabulate(df, headers='keys', 
            tablefmt='fancy_grid',
            numalign="center",
            stralign="center",
            showindex=False,
            maxcolwidths=[None, 20, None, None, 20, 25, 20, None, None, None, None]))

def data_to_file(out_name, data):
    """Materialize aggregated data into CSV and JSON outputs.

    The input ``data`` is expected to be a list with rows in the following
    order (matching the producer in ``all_data``):
        [filesystem, filer, mountpoint, extracted_path,
         accessed_gt_1_year, accessed_gt_1_month, accessed_1_31_days,
         owners, total_used_human_readable]

    This function expands the rows into a tabular structure, computes
    two additional sums, and writes both ``<out_name>.csv`` and
    ``<out_name>.json``.

    Args:
        out_name: Base output file name (without extension).
        data: Aggregated rows as described above.
    """
    file_systems = []
    filers = []
    mountpoints = []
    extracted_paths = []
    accessed_1year = []
    accessed_1month = []
    accessed_1_31days = []
    sum_under_12months = []
    total_sum = []
    users = []
    total_used_human = []

    try:
        for row in data:
            file_systems.append(row[0])
            filers.append(row[1])
            mountpoints.append(row[2])
            extracted_paths.append(row[3])
            accessed_1year.append(row[4])
            accessed_1month.append(row[5])
            accessed_1_31days.append(row[6])
            sum_under_12months.append(int(row[5]) + int(row[6]))
            total_sum.append(int(row[4]) + int(row[5]) + int(row[6]))
            users.append(row[7])
            total_used_human.append(row[8])

        df = pd.DataFrame(
            list(
                zip(
                    filers,
                    file_systems,
                    total_used_human,
                    mountpoints,
                    extracted_paths,
                    users,
                    accessed_1year,
                    accessed_1month,
                    accessed_1_31days,
                    sum_under_12months,
                    total_sum,
                )
            ),
            columns=[
                "Filer",
                "Filesystem",
                "Total Used",
                "Mountpoint",
                "Extract - Path",
                "Owner/s",
                "accessed_>1 year",
                "accessed_>1 month",
                "accessed_1-31 days",
                "Sum under 12months",
                "Sum",
            ],
        )
        # Ensure output folder exists
        os.makedirs("output", exist_ok=True)

        base_name = os.path.basename(out_name)
        out_path = os.path.join("output", base_name)

        df.to_csv(out_path + ".csv", index=False)
        df.to_json(out_path + ".json", orient="records", indent=2)

        print("CSV and JSON file created in output/ directory")

        return df
    except Exception as e:  # pragma: no cover
        print(e)