import json
from collections import defaultdict
from typing import Dict, Any
import glob
import os

def structure_unstructured_to_txt(input_path: str, output_txt_path: str) -> None:
    """
    Reads an Unstructured JSON file, groups elements by page,
    organizes them by titles with narrative text, tables, code, and formulas,
    and saves the structured output as a formatted text file.

    Args:
        input_path (str): Path to the input JSON file.
        output_txt_path (str): Path where the formatted text will be saved.
    """
    # Load input JSON
    with open(input_path, "r", encoding="utf-8") as f:
        elements = json.load(f)

    # Element types to include
    valid_types = {"Title", "NarrativeText", "Table", "CodeSnippet", "Formula"}

    # Group elements by page
    pages = defaultdict(list)
    for el in elements:
        if el.get("type") not in valid_types:
            continue  # Skip unrecognized elements

        page_number = el.get("metadata", {}).get("page_number", "Unknown")
        pages[page_number].append(el)

    # Build structured output for text
    output_lines = []

    for page, items in sorted(pages.items()):
        output_lines.append(f"\n=== Page {page} ===")
        section = {"title": None, "content": []}

        for el in items:
            etype = el["type"]
            text = el.get("text", "").strip()

            if not text:
                continue

            if etype == "Title":
                # Save current section if it exists
                if section["title"] or section["content"]:
                    output_lines.append(f" {section['title'] if section['title'] else ''}")
                    for c in section["content"]:
                        output_lines.append(f"-  {c['text']}")
                    output_lines.append("")  # blank line

                # Start a new section
                section = {"title": text, "content": []}
            else:
                section["content"].append({
                    "type": etype,
                    "text": text
                })

        # Save the last section for this page
        if section["title"] or section["content"]:
            output_lines.append(f"{section['title'] if section['title'] else ''}")
            for c in section["content"]:
                output_lines.append(f"-  {c['text']}")
            output_lines.append("")  # blank line

    # Write formatted text to file
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"Formatted text saved to: {output_txt_path}")

    # Example usage: process all JSON files in ./outputs and save to ./clead_data
if __name__ == "__main__":
    input_dir = "./outputs"
    output_dir = "./clead_data"
    os.makedirs(output_dir, exist_ok=True)

    for input_file in glob.glob(os.path.join(input_dir, "*.json")):
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}-structured.txt")
        structure_unstructured_to_txt(input_file, output_file)
