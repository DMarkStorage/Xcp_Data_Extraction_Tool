from docopt import docopt
from utils.parser import (
    get_fileSystem,
    get_filer,
    get_mountpoint,
    get_extract_path,
    get_access,
    get_user,
    get_used,
)
from utils.io_util import convert_size, data_to_file, df_table

__version__ = 'Version 1.0'
__revision__ = '1.0'
__deprecated__ = False



def get_args():
    """
    Parse and return command-line arguments.

    Defines and parses the CLI contract for this program using docopt.

    Returns:
        dict: A mapping of CLI option/argument names to their parsed values.
              Expected keys include:
                - '<FILENAME>': str, path to the input file
                - '<OUTPUTNAME>': str, path/name for the output file
                - '-v': bool, if provided, prints a preview of the DataFrame
                - '-n <NUMROWS>': int, number of rows to display when using -v
                - '--help': bool
                - '--version': bool
    """
    usage = """
    Usage:
        extract_data_xcp.py -r <FILENAME> -f <OUTPUTNAME>
        extract_data_xcp.py -r <FILENAME> -f <OUTPUTNAME> -v [-n <NUMROWS>]
        extract_data_xcp.py --version
        extract_data_xcp.py -h | --help

    Options:
        -f <OUTPUTNAME>     Output filename (without extension).
        -v --view           View a preview of the output DataFrame. 
        -n <NUMROWS>        Number of rows to display in preview [default: 10].
        -r <FILENAME>       Input filename to process.
        -h --help           Show this message and exit
        --version           Show program version and exit

    """

    args = docopt(usage)
    # Convert -n to int safely
    args["-n"] = int(args["-n"]) if args.get("-n") else 10
    return args


def all_data(output_name, file_systems, filers, mountpoints, extracted_paths,
             access_list, users_list, total_used):
    """Aggregate parsed data and write it to the output.

    Iterates over aligned collections of filesystem metadata and usage
    information, normalizes/pretty-formats values, and forwards the
    assembled rows to `data_to_file`.

    Args:
        output_name (str): Target output file name/path.
        file_systems (list): Filesystem identifiers/records.
        filers (list): Filer or storage controller identifiers.
        mountpoints (list): Filesystem mount points.
        extracted_paths (list): Extracted/derived paths for each filesystem.
        access_list (list): Per-filesystem access triplets (e.g., [read, write, execute]).
        users_list (list): Users or owners associated with each filesystem.
        total_used (list): Raw total-used byte counts per filesystem (as strings or ints).

    Side Effects:
        Writes aggregated data using `data_to_file(output_name, data)`.
    """
    data = []

    for fs, filer, mountpoint, e_path, access, users, used_raw in zip(
        file_systems, filers, mountpoints, extracted_paths, access_list, users_list, total_used
    ):
        used_raw_str = used_raw.strip()
        used_human = convert_size(int(used_raw_str))

        data.append([
            fs.strip(),
            filer,
            mountpoint.strip(),
            e_path.strip(),
            access[0],
            access[1],
            access[2],
            users,
            used_human
        ])

    return data_to_file(output_name, data)


def main(args):
    """Program entry point.

    Extracts required arguments, invokes parsing utilities, and orchestrates
    aggregation and output generation.

    Args:
        args (dict): Parsed command-line arguments from `get_args()`.
    """
    input_filename = args['-r']
    output_name = args['-f']

    file_systems = get_fileSystem(input_filename)
    filers = get_filer(file_systems)
    mountpoints = get_mountpoint(file_systems)
    extracted_paths = get_extract_path(file_systems)
    access_list = get_access(input_filename)
    users_list = get_user(input_filename)
    total_used = get_used(input_filename)

    data = all_data(
        output_name,
        file_systems,
        filers,
        mountpoints,
        extracted_paths,
        access_list,
        users_list,
        total_used
    )
    if args.get('--view') or args.get('-v'):
        num_rows = args['-n']
        df_table(data, num_rows)

if __name__ == '__main__':
    try:
        ARGS = get_args()
        main(ARGS)
    except Exception as e:
        print(e)
