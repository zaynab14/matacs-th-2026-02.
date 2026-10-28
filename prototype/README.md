# Optional prototype

This small script reads the fictional proposal summaries from the original brief PDF at runtime and runs the extraction prompt in `../PROMPTS.md` once for each proposal. It stores extracted JSON locally under `run-output/`. The proposal text and API key are not included in the repository.

The script extracts evidence only. It does not apply mandatory gates, calculate weighted scores, or rank bidders; those remain rule-based and human-reviewed in the design.

## Run on Windows

1. Install Python 3.10 or newer.
2. From this folder, create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your own `OPENAI_API_KEY`. Keep `.env` out of GitHub. You may change `OPENAI_MODEL` to a model available to your API account.
4. Run the script with the original brief PDF path:

   ```powershell
   python run.py --brief "C:\path\to\MATACS-TH-2026-02_Candidate_Brief.pdf"
   ```

The script makes five API requests, one per proposal, so an API key is needed to run it. Review the extracted evidence before relying on it.
