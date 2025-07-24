# sample-data-generator 📝
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**sample-data.py** is a flexible Python script powered by [Faker](https://faker.readthedocs.io/) to quickly generate realistic sample datasets in various formats.
- CSV
- TXT
- JSON
- PDF
- SQL
- XLSX
- XML

## ⚡ Quickstart Guide

### 1. Clone the Repository

```bash
git clone https://github.com/malwaredetective/sample-data-generator.git
cd sample-data-generator
```

### 2. Set Up a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate    # (Windows: venv\Scripts\activate)
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the script to generate your sample data!
```bash
python3 sample-data.py --name <basefilename> --count <num_records> --output <format> --fields <field1> <field2>
```

```
(venv) khub@KHUB-PC:/mnt/c/Users/Khub/source/repos/sample-data-generator$ python3 sample-data.py --name contacts --count 5000 --output json --fields name email phone_number address
                           _                _       _
 ___  __ _ _ __ ___  _ __ | | ___        __| | __ _| |_ __ _   _ __  _   _
/ __|/ _` | '_ ` _ \| '_ \| |/ _ \_____ / _` |/ _` | __/ _` | | '_ \| | | |
\__ \ (_| | | | | | | |_) | |  __/_____| (_| | (_| | || (_| |_| |_) | |_| |
|___/\__,_|_| |_| |_| .__/|_|\___|      \__,_|\__,_|\__\__,_(_) .__/ \__, |
                    |_|                                       |_|    |___/

Generating JSON ... |████████████████████████████████| 5000/5000

[SUCCESS] Created: 'contacts.json', Size: 0.86 MB
```

## 📚 Usage 
Use the following commands to generate data.

```bash
python3 ./sample-data.py --help
```

| Command | Description | Default |
| --- | --- | --- |
| `--name [STRING]` | The base name of the output file. | `sample` |
| `--count [INT]` | The number of records to generate. | `100` | 
| `--output [STRING]` | The output file format. | `TXT` |
| `--fields [STRING]` | A space-separated list of data types to include within the sample data. | `name, email, address, password, phone_number, ssn, ip_address` |

## 🚀 Examples

### Generate a CSV file with 5000 records of names, addresses, phone numbers and social security numbers:

```bash
python3 sample-data.py --name customers --count 5000 --output csv --fields name address phone_number ssn
```

### Generate an SQL database with 250 records of names, passwords and email addresses:

```bash
python3 sample-data.py --name employee_database --count 250 --output sql --fields name password email
```


