# 🗄️ XCP Data Extraction Tool

> Transform complex NetApp XCP scan reports into actionable CSV and JSON insights in seconds.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/xcp-data-extraction)
[![Last Commit](https://img.shields.io/github/last-commit/yourusername/xcp-data-extraction)](https://github.com/yourusername/xcp-data-extraction/commits/main)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yourusername/xcp-data-extraction/graphs/commit-activity)

---

## 📑 Table of Contents

- [🗄️ XCP Data Extraction Tool](#️-xcp-data-extraction-tool)
  - [📑 Table of Contents](#-table-of-contents)
  - [🚀 Project Overview](#-project-overview)
    - [✨ Key Features](#-key-features)
  - [🛠️ Getting Started](#️-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Method 1: Clone from GitHub (Recommended)](#method-1-clone-from-github-recommended)
      - [Method 2: Download ZIP](#method-2-download-zip)
  - [⚙️ Usage Examples](#️-usage-examples)
    - [Quick Start](#quick-start)
      - [JSON-Only Output for API Integration](#json-only-output-for-api-integration)
    - [Command-Line Options](#command-line-options)
    - [Core Functions](#core-functions)
    - [Architecture Overview](#architecture-overview)
  - [🤝 Contributing](#-contributing)
    - [How to Contribute](#how-to-contribute)
    - [Development Setup](#development-setup)
    - [Contribution Guidelines](#contribution-guidelines)
  - [📝 License \& Acknowledgements](#-license--acknowledgements)
    - [License](#license)
    - [Acknowledgements](#acknowledgements)
    - [References](#references)
  - [💬 Contact \& Support](#-contact--support)
    - [Get Help](#get-help)
    - [Connect With Us](#connect-with-us)
    - [Support This Project](#support-this-project)

---

## 🚀 Project Overview

The **XCP Data Extraction Tool** automates the parsing and transformation of verbose NetApp XCP scan reports into clean, structured data formats. Designed for storage administrators and data analysts, this tool eliminates hours of manual report analysis by extracting filesystem metadata, access patterns, ownership information, and storage metrics into Excel-ready CSV files and API-friendly JSON outputs.

### ✨ Key Features

- 📊 **Automated Extraction**: Parse complex XCP logs and extract 7+ critical metadata fields automatically
- 💾 **Dual Format Output**: Generate both CSV (spreadsheet-compatible) and JSON (database-ready) files simultaneously
- 📏 **Human-Readable Metrics**: Convert raw byte counts to GB/TB for intuitive capacity planning
- 🕐 **Access Pattern Analysis**: Categorize files by access age (>1 year, >1 month, recent) for archival decisions
- 🎯 **Compliance Ready**: Extract ownership and usage data for audit trails and chargeback reporting
- ⚡ **Time Savings**: Reduce report analysis time from hours to seconds
- 🔧 **Flexible Integration**: JSON output enables seamless integration with monitoring dashboards and automation workflows


**Sample Input** (Raw XCP Report):
```
Filesystem: /vol/engineering_data
Filer: netapp-prod-01
Total: 5497558138880 bytes
Access >1 year: 1234 files
Users: 45
...
```

**Sample Output** (Generated CSV):

| Filesystem | Filer | Mountpoint | Access >1 Year | Total Used |
|------------|-------|------------|----------------|------------|
| /vol/engineering_data | netapp-prod-01 | /mnt/engineering | 1,234 files | 5.12 TB |
| /vol/archives | netapp-prod-02 | /mnt/archive | 45,678 files | 12.8 TB |

## 🛠️ Getting Started

### Prerequisites

Before running the XCP Data Extraction Tool, ensure you have the following installed:

- **Python 3.6+** (Python 3.8+ recommended)
- **pip** (Python package manager)
- **Access to NetApp XCP scan reports** (`.txt` or `.log` files)

**Check your Python version:**
```bash
python --version
# or
python3 --version
```

### Installation

#### Method 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/DMarkStorage/Xcp_Data_Extraction_Tool.git

# Navigate to the project directory
cd xcp-data-extraction

# Install required dependencies
pip install -r requirements.txt
```

#### Method 2: Download ZIP

1. Download the latest release from [Releases](https://github.com/yourusername/xcp-data-extraction/releases)
2. Extract the ZIP file
3. Navigate to the extracted directory
4. Run: `pip install -r requirements.txt`

**Required Python Packages:**
- `pandas>=1.3.0`
- `docopt>=0.6.2`

---

## ⚙️ Usage Examples

### Quick Start

Run the tool with a single command to extract data from your XCP report:

```bash
python xcp_extractor.py --input /path/to/xcp_scan_report.txt --output filesystem_analysis
```

**What happens:**
1. The tool reads your XCP scan report
2. Extracts filesystem metadata, access patterns, and storage metrics
3. Generates two files:
   - `filesystem_analysis.csv` (Excel-compatible)
   - `filesystem_analysis.json` (API/database-ready)



#### JSON-Only Output for API Integration

```bash
python xcp_extractor.py \
  --input xcp_report.txt \
  --output api_data \
  --format json
```


### Command-Line Options

```bash
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
```

---


### Core Functions

The tool is built around a modular architecture:

```python
def all_data(output_name, file_systems, filers, mountpoints,
             extracted_paths, access_list, users_list, total_used):
    """
    Coordinates extraction and transformation of XCP report data.
    
    Args:
        output_name (str): Base name for output files
        file_systems (list): List of filesystem identifiers
        filers (list): NetApp filer names
        mountpoints (list): NFS mount paths
        extracted_paths (list): Subdirectory paths
        access_list (list): File access frequency data
        users_list (list): User/owner information
        total_used (list): Raw storage consumption in bytes
    
    Returns:
        None: Writes data to CSV and JSON files
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

```

**Key Design Principles:**
- **Separation of Concerns**: Parsing, transformation, and output are handled by distinct modules
- **Data Validation**: Input sanitization prevents malformed data from breaking extraction
- **Human-Readable Conversion**: Automatic byte-to-TB conversion via `convert_size()` function
- **Flexible Output**: `data_to_file()` handles both CSV and JSON serialization

### Architecture Overview

```
                    ┌─────────────────────┐
                    │  XCP Scan Report    │
                    │  (Raw Text Input)   │
                    └──────────┬──────────┘
                            │
                            ▼
                    ┌─────────────────────┐
                    │  Pattern Matching   │
                    │  & Text Parsing     │
                    └──────────┬──────────┘
                            │
                            ▼
                    ┌─────────────────────┐
                    │  Data Extraction    │
                    │  (7 Metadata Fields)│
                    └──────────┬──────────┘
                            │
                            ▼
                    ┌─────────────────────┐
                    │  Transformation     │
                    │  (Bytes → TB)       │
                    └──────────┬──────────┘
                            │
                            ▼
                    ┌─────────────────────┐
                    │  Output Generation  │
                    │  CSV + JSON         │
                    └─────────────────────┘
```
---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and commit: `git commit -m 'Add amazing feature'`
4. **Push to your branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request** with a clear description of your changes

### Development Setup

```bash
# Clone your fork
git clone https://github.com/DMarkStorage/Xcp_Data_Extraction_Tool.git
cd xcp-data-extraction

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

```

### Contribution Guidelines

- Write clear, descriptive commit messages
- Add unit tests for new features
- Update documentation for API changes
- Follow PEP 8 style guidelines for Python code
- Ensure all tests pass before submitting PR

---

## 📝 License & Acknowledgements

### License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Damini Marvin Mark

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

### Acknowledgements

This project was inspired by the challenges faced by storage administrators dealing with verbose NetApp XCP reports. Special thanks to:

- **NetApp** for the XCP tool and comprehensive API documentation
- **The Python Community** for excellent libraries like `pandas` and `docopt`
- **Storage Administrators** who provided feedback on early versions
- **Contributors** who have helped improve this tool

### References

- [NetApp XCP Documentation](https://docs.netapp.com/us-en/xcp/index.html)
- [Docopt - Command-line Interface Description Language](http://docopt.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/reference/io.html)

---

## 💬 Contact & Support

### Get Help

- 🐛 **Found a bug?** [Open an issue](https://github.com/DMarkStorage/Xcp_Data_Extraction_Tool/issues)
- 💡 **Have a feature request?** [Start a discussion]((https://github.com/DMarkStorage/Xcp_Data_Extraction_Tool/discussions)

### Connect With Us
- 🌐 **Website**: [dmarkstorage.io](https://dmarkstorage.io)


### Support This Project

If this tool has saved you time or helped your organization, consider:

- ⭐ **Starring the repository** on GitHub
- 📢 **Sharing it** with colleagues in storage administration
- 🤝 **Contributing** improvements or documentation

---
