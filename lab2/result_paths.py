from pathlib import Path

BASE = Path(__file__).resolve().parent
RESULT_DIR = BASE / "result"
GRADE3_DIR = RESULT_DIR / "grade3"

for directory in (RESULT_DIR, GRADE3_DIR):
    directory.mkdir(parents=True, exist_ok=True)

RESULTS_CSV = GRADE3_DIR / "results.csv"
SUMMARY_CSV = GRADE3_DIR / "summary.csv"
LOOP_ORDER_CSV = GRADE3_DIR / "loop_order_results.csv"

EXECUTION_TIME_PNG = GRADE3_DIR / "execution_time.png"
SPEEDUP_PNG = GRADE3_DIR / "speedup.png"
