import sys
import os
import json
import argparse
from fast_mail_parser import parse_email, ParseError


def process_eml_file(eml_file):
    with open(eml_file, "r") as f:
        message_payload = f.read()

    try:
        email = parse_email(message_payload)
    except ParseError as e:
        print(f"Failed to parse email {eml_file}: ", e)
        return

    json_filename = os.path.splitext(eml_file)[0] + ".json"
    with open(json_filename, "w") as f:
        json.dump(
            {
                "subject": email.subject,
                "text_plain": email.text_plain[0] if email.text_plain else "",
                "text_html": email.text_html,
                "date": email.date,
                "headers": email.headers,
            },
            f,
            indent=4,
        )
    print(f"Processed {eml_file} -> {json_filename}")


def main(eml_files):
    for eml_file in eml_files:
        process_eml_file(eml_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert EML files to JSON format.")
    parser.add_argument(
        "eml_files", metavar="F", type=str, nargs="+", help="EML files to process"
    )
    args = parser.parse_args()
    main(args.eml_files)
