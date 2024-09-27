import json
import os
import argparse


def single_email2latex(latex_from, latex_to, latex_subject, latex_date, latex_content):
    latex_content = latex_content.strip()
    latex_content = latex_content.replace("\r", "")
    latex_content = latex_content.replace("\n", "\\\\")
    latex_content = latex_content.replace("_", "\\_")

    return (
        "\\begin{tabularx}{\\linewidth}{rX}\n"
        "\t\\hline\n"
        "\t\\rowcolor{dark_color}\n"
        f"\t\\texttt{{From}} & {latex_from} \\\\\n"
        "\t\\hline\n"
        "\t\\rowcolor{light_color}\n"
        f"\t\\texttt{{To}} & {latex_to} \\\\\n"
        "\t\\hline\n"
        "\t\\rowcolor{dark_color}\n"
        f"\t\\texttt{{Date}} & {latex_date} \\\\\n"
        "\t\\hline\n"
        "\t\\rowcolor{light_color}\n"
        f"\t\\texttt{{Subject}} & {latex_subject} \\\\\n"
        "\t\\hline\n"
        "\\end{tabularx}\n"
        "\\vspace{0.5em}\n"
        "{\\centering\\par\\noindent\\rule{0.9\\textwidth}{0.5pt}\\\\[0.5em]}\n\n"
        f"{latex_content}\n\n"
        "\\par\\noindent\\rule{\\textwidth}{1.5pt}\\\\[1.5em]\n"
    )


def parse_email_from_to(text):
    # Take only the text between <> and remove the rest
    if "<" in text or ">" in text:
        text = text.split("<")[1].split(">")[0]
    return text


def mail2latex(emails, light_color="eef7ff", dark_color="d3ebff"):
    latex = (
        "\\documentclass[12pt]{article}\n"
        "\\usepackage[dvipsnames]{xcolor}\n"
        "\\usepackage{tabularx, colortbl, makecell}\n"
        "\\usepackage[left=2cm, right=2cm, top=2cm, bottom=2cm]{geometry}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T1]{fontenc}\n"
        f"\\definecolor{{light_color}}{{HTML}}{{{light_color}}}\n"
        f"\\definecolor{{dark_color}}{{HTML}}{{{dark_color}}}\n"
        "\\setlength{\\parindent}{0cm}\n\n"
        "\\begin{document}\n\n"
    )

    for e in emails:
        latex_from = parse_email_from_to(e["headers"].get("From", ""))
        latex_to = parse_email_from_to(e["headers"].get("To", ""))
        latex_subject = e["headers"].get("Subject", "")
        latex_date = e["headers"].get("Date", "")
        latex_content = e.get("text_plain", "")

        latex += single_email2latex(
            latex_from, latex_to, latex_subject, latex_date, latex_content
        )

    latex += "\\end{document}"
    return latex


# Remove all the lines that begin with ">"
def parse_email_content(email_content):
    email_content = email_content.split("\n")
    email_content = [i for i in email_content if not i.startswith(">")]
    return "\n".join(email_content)


def main(
    input_files, output_file="output.tex", light_color="eef7ff", dark_color="d3ebff"
):
    emails = []

    for i in input_files:
        print(i)
        with open(i, "r") as f:
            emails.append(json.load(f))
        emails[-1]["text_plain"] = parse_email_content(emails[-1]["text_plain"])

    latex = mail2latex(emails, light_color, dark_color)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(latex)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert EML emails to LaTeX format.")
    parser.add_argument(
        "input_files", metavar="F", type=str, nargs="+", help="JSON files to process"
    )
    parser.add_argument(
        "--output_file", metavar="O", type=str, default="output.tex", help="Output file"
    )
    parser.add_argument(
        "--light_color",
        metavar="LC",
        type=str,
        default="eef7ff",
        help="Light color for the table",
    )
    parser.add_argument(
        "--dark_color",
        metavar="DC",
        type=str,
        default="d3ebff",
        help="Dark color for the table",
    )
    args = parser.parse_args()
    main(args.input_files, args.output_file, args.light_color, args.dark_color)
