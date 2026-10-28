"""Run the PROMPTS.md extraction prompt on proposals found in the brief PDF.

Proposal text is read from the PDF at runtime and is not stored in this repository.
The script extracts evidence only; it does not score or rank bidders.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = PROJECT_ROOT / "PROMPTS.md"
SAMPLE_PAGES = (2, 3)  # PDF page numbers containing the fictional proposals.


def load_prompt_template() -> str:
    content = PROMPT_FILE.read_text(encoding="utf-8")
    match = re.search(r"```text\s*(.*?)\s*```", content, flags=re.DOTALL)
    if not match:
        raise ValueError(f"No text prompt found in {PROMPT_FILE}")
    return match.group(1).strip()


def extract_proposals(brief_path: Path) -> dict[str, str]:
    reader = PdfReader(str(brief_path))
    if len(reader.pages) < max(SAMPLE_PAGES):
        raise ValueError("The brief PDF does not have the expected sample pages.")

    marked_pages = []
    for page_number in SAMPLE_PAGES:
        page_text = reader.pages[page_number - 1].extract_text() or ""
        marked_pages.append(f"[PAGE {page_number}]\n{page_text}")
    source_text = "\n".join(marked_pages)

    pattern = re.compile(
        r"^Proposal\s+([A-E])\s*:\s*(.*?)"
        r"(?=^Proposal\s+[A-E]\s*:|^Questions to answer|\Z)",
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    proposals: dict[str, str] = {}
    for match in pattern.finditer(source_text):
        letter = match.group(1).upper()
        body = match.group(2).strip()
        proposals[letter] = f"Proposal {letter}:\n{body}"

    missing = sorted(set("ABCDE") - proposals.keys())
    if missing:
        raise ValueError(
            "Could not locate all sample proposals in the PDF: " + ", ".join(missing)
        )
    return proposals


def make_prompt(template: str, letter: str, proposal_text: str) -> str:
    return (
        template.replace("[CATEGORY]", "Commercial Solar Installation")
        .replace("[A-E]", letter)
        .replace("[PROPOSAL_TEXT]", proposal_text)
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract cited proposal evidence using PROMPTS.md."
    )
    parser.add_argument(
        "--brief",
        required=True,
        type=Path,
        help="Path to the original candidate brief PDF; it is read locally, not copied.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "run-output",
        help="Where to save extracted JSON files (ignored by Git by default).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional model override; otherwise OPENAI_MODEL or gpt-5.5 is used.",
    )
    args = parser.parse_args()

    load_dotenv(Path(__file__).resolve().parent / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        parser.error("Set OPENAI_API_KEY in prototype/.env before running the API call.")

    model = args.model or os.getenv("OPENAI_MODEL", "gpt-5.5")
    template = load_prompt_template()
    proposals = extract_proposals(args.brief)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    client = OpenAI()

    for letter in "ABCDE":
        prompt = make_prompt(template, letter, proposals[letter])
        response = client.responses.create(model=model, input=prompt)
        try:
            result = json.loads(response.output_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"The model did not return valid JSON for proposal {letter}."
            ) from exc

        if result.get("proposal") != letter:
            raise ValueError(f"Unexpected proposal letter in response for {letter}.")

        output_path = args.output_dir / f"{letter}.json"
        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Saved proposal {letter} extraction to {output_path}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
