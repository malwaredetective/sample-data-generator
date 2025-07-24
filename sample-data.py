import os
import sys
import argparse
import csv
import json
import pyfiglet
from faker import Faker
from faker.providers import internet, phone_number
from progress.bar import ShadyBar
from colorama import Fore, Style
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook

fake = Faker()
fake.add_provider(internet)
fake.add_provider(phone_number)

FIELD_GENERATORS = {
    'name': fake.name,
    'email': fake.email,
    'address': lambda: fake.address().replace('\n', ', '),
    'phone_number': fake.phone_number,
    'ssn': fake.ssn,
    'ip_address': fake.ipv4_public,
}

DATA_FIELDS = list(FIELD_GENERATORS.keys())

def ascii_art():
    """Prints the ASCII art title for the application."""
    title = pyfiglet.figlet_format("sample-data.py", font="standard")
    print(Fore.CYAN + title + Style.RESET_ALL)

def generate_record(fields):
    record = {}
    for field in fields:
        if field in FIELD_GENERATORS:
            record[field] = FIELD_GENERATORS[field]()
        else:
            log_message("[WARNING]", f"The field: '{field}' is not recognized and will be skipped.", Fore.YELLOW)
    return record

def log_message(tag, message, tag_color):
    """
    Prints a formatted log message with a colored tag.
    Args:
        tag (str): The tag (e.g., "[ERROR]", "[SUCCESS]", "[INFO]").
        message (str): The message to print.
        tag_color (str): The color for the tag (e.g., Fore.RED, Fore.GREEN).
    """
    print(f"{tag_color}{tag}{Style.RESET_ALL} {message}")

def prompt_overwrite(filename):
    """Prompt for user input if the file already exists."""
    response = input(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} File '{filename}' already exists. Overwrite? (Y/N): ")
    if not response.strip().lower().startswith('y'):
        log_message("[INFO]", f"This script was cancelled by the user.", Fore.CYAN)
        sys.exit(0)

def write_csv(filename, fields, count):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f, \
             ShadyBar('Generating CSV ...', max=int(count)) as bar:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for _ in range(count):
                writer.writerow(generate_record(fields))
                bar.next()
            bar.finish()
    except Exception as e:
        log_message("[ERROR]", f"Could not write CSV to '{filename}': {e}", Fore.RED)

def write_txt(filename, fields, count):
    try:
        with open(filename, 'w', encoding='utf-8') as f, \
             ShadyBar('Generating TXT ...', max=int(count)) as bar:
            f.write('\t'.join(fields) + '\n')
            for _ in range(count):
                record = generate_record(fields)
                line = '\t'.join(str(record.get(field, '')) for field in fields) + '\n'
                f.write(line)
                bar.next()
            bar.finish()
    except Exception as e:
        log_message("[ERROR]", f"Could not write TXT to '{filename}': {e}", Fore.RED)

def write_json(filename, fields, count):
    records = []
    try:
        with ShadyBar('Generating JSON ...', max=int(count)) as bar:
            for _ in range(count):
                records.append(generate_record(fields))
                bar.next()
            bar.finish()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        log_message("[ERROR]", f"Could not write JSON to '{filename}': {e}", Fore.RED)

def write_pdf(filename, fields, count):
    from contextlib import suppress
    if not fields or count <= 0:
        print("No fields specified or count is zero. Skipping PDF generation.")
        return

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 30
    line_height = 14

    try:
        with ShadyBar('Generating PDF ...', max=int(count)) as bar:
            # Header
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, ' | '.join(fields))
            y -= line_height
            c.setFont("Helvetica", 10)

            for _ in range(count):
                record = generate_record(fields)
                line = ' | '.join(str(record.get(field, '')) for field in fields)
                c.drawString(30, y, line)
                y -= line_height
                if y <= 30:
                    c.showPage()
                    y = height - 30
                    c.setFont("Helvetica", 10)
                bar.next()
            bar.finish()
    except Exception as e:
        log_message("[ERROR]", f"Could not write PDF to '{filename}': {e}", Fore.RED)
    finally:
        with suppress(Exception):
            c.save()

def write_xlsx(filename, fields, count):
    try:
        wb = Workbook()
        ws = wb.active
        ws.append(fields)
        with ShadyBar('Generating XLSX ...', max=int(count)) as bar:
            for _ in range(count):
                record = generate_record(fields)
                ws.append([record.get(field, '') for field in fields])
                bar.next()
            bar.finish()
        wb.save(filename)
    except Exception as e:
        log_message("[ERROR]", f"Could not write XLSX to '{filename}': {e}", Fore.RED)

def main():
    parser = argparse.ArgumentParser(
        description="A Python script that dynamically generates sample data."
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    parser.add_argument("--name", type=str, default="sample", help="The base name of the output file.")
    parser.add_argument("--count", type=int, default=100, help="Number of records to generate.")
    parser.add_argument("--output", type=str, choices=["csv", "json", "pdf", "txt", "xlsx"], default="txt", help="The output file format.")
    parser.add_argument("--fields", type=str, nargs='*', choices=DATA_FIELDS, default=DATA_FIELDS, help="A space-separated list of data types to include within the sample data.")
    args = parser.parse_args()

    filename = f"{args.name}.{args.output}"
    if os.path.exists(filename):
        prompt_overwrite(filename)

    if args.output == "csv":
        write_csv(filename, args.fields, args.count)
    elif args.output == "txt":
        write_txt(filename, args.fields, args.count)
    elif args.output == "json":
        write_json(filename, args.fields, args.count)
    elif args.output == "pdf":
        write_pdf(filename, args.fields, args.count)
    elif args.output == "xlsx":
        write_xlsx(filename, args.fields, args.count)
    else:
        log_message("[ERROR]", f"The output format you selected is not supported.", Fore.RED)
        sys.exit(1)

    file_size_bytes = os.path.getsize(filename)
    file_size_mb = file_size_bytes / (1024 * 1024)
    log_message("[SUCCESS]", f"Created: '{filename}', Size: {file_size_mb:.2f} MB", Fore.GREEN)

if __name__ == "__main__":
    ascii_art()
    main()