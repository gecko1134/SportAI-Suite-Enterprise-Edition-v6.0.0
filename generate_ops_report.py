from pathlib import Path
from modules.ops_report_pdf import generate_pdf

if __name__ == "__main__":
    out = generate_pdf(Path(__file__).resolve().parents[1])
    print(f"Ops report generated at: {out}")
