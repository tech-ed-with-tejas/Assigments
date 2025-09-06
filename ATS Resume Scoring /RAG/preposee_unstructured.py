from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json, convert_to_dict
from pathlib import Path
import json
import glob
# Input/Output paths
pdf_path = glob.glob("data/*.pdf") # Take the first PDF in data/
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Partition with useful options

for i in pdf_path:
    name = i.split("/")[-1].split(".")[0]
    elements = partition_pdf(
        filename=i,
        strategy="hi_res",
        infer_table_structure=True,  # Enable table extraction (empty list)
        extract_image_block_types=[]  # Disable image extraction (empty list)
    )

    as_dict = convert_to_dict(elements)
    with open(output_dir / f"{name}.json", "w", encoding="utf-8") as f:
        json.dump(as_dict, f, ensure_ascii=False, indent=2)

# # Option C: Save one JSON per element (optional granular output)
# per_element_dir = output_dir / "elements"
# per_element_dir.mkdir(exist_ok=True)
# for idx, el in enumerate(elements, start=1):
#     with open(per_element_dir / f"{idx:04d}.json", "w", encoding="utf-8") as f:
#         json.dump(el.to_dict(), f, ensure_ascii=False, indent=2)

# print(f"Wrote JSON to: {single_json_path}")
