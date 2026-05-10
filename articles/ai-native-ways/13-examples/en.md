---
slug: examples
number: "13"
lang: en
title: "Examples — 12 Walkthroughs"
subtitle: "Code and output for every chapter, end to end"
description: Verify each chapter's claims with actual commands, code, and output. Word minutes to Markdown; 100 Excel files aggregated in 30 seconds; PL/SQL rewritten via parallel operation; AI agents frozen into Python — 12 walkthroughs you can run yourself.
date: 2026.05.02
label: AI Native EX
title_html: <span class="accent">Code</span> and <span class="accent">output</span>.<br>12 chapters, hands on.
prev_slug: one-plus-ai
prev_title: "One Person + AI — The New Unit of Work"
next_slug:
next_title:
---

# Examples — 12 Walkthroughs

This page is a hands-on reference that confirms the claims of every chapter of "AI-Native Ways of Working" with **actual commands, code, and output**. Each example maps to a chapter number.

Read the chapter first, then run the example here. Or run the example, then return to the chapter to re-anchor the meaning.

Each example follows:

- **Setup**: input and required tools
- **Steps**: commands, code, actual output
- **Result**: what you ended up with

---

## Example 01: Convert 12 months of Word minutes to Markdown

→ Confirms Chapter 2 "[Writing Documents](/en/ai-native-ways/markdown/)"

### Setup

- Input: `minutes/2026-{01..12}.docx` (12 files, 360 KB total)
- Tools: `pandoc`, `claude` CLI, `grep`

### Steps

```bash
$ ls minutes/
2026-01.docx  2026-04.docx  2026-07.docx  2026-10.docx
2026-02.docx  2026-05.docx  2026-08.docx  2026-11.docx
2026-03.docx  2026-06.docx  2026-09.docx  2026-12.docx
$ du -sh minutes/
360K    minutes/
```

**Step 1: bulk convert**

```bash
$ mkdir minutes-md
$ for f in minutes/*.docx; do
>   pandoc "$f" -o "minutes-md/$(basename "${f%.docx}").md"
> done
$ du -sh minutes-md/
68K     minutes-md/
```

**4.8 seconds. 360 KB → 68 KB (about one-fifth).**

**Step 2: search for a theme across 12 months**

```bash
$ grep -l "fertilizer price" minutes-md/*.md
minutes-md/2026-03.md
minutes-md/2026-06.md
minutes-md/2026-08.md
minutes-md/2026-11.md

$ grep -A 2 "fertilizer price" minutes-md/2026-08.md
- fertilizer price: trending +12% MoM, revising next month's order plan
- owner: sales
- due: 2026-09-15
```

VBA in Word would take 30 minutes. `grep` does it in 0.1 seconds.

**Step 3: print-quality PDF**

```bash
$ pandoc minutes-md/2026-04.md -o 2026-04.pdf \
  --pdf-engine=xelatex --toc \
  -V mainfont="Hiragino Mincho Pro" \
  -V geometry:margin=2.5cm

$ ls -lh 2026-04.pdf
-rw-r--r-- 1 user staff 142K 2026-04.pdf
```

Typeset PDF, table of contents, 2.5cm margins, 142 KB.

**Step 4: analyze 12-month patterns with Claude**

```bash
$ cat minutes-md/*.md | claude -p \
  "List the five themes most often repeated across these minutes, with frequency"
```

Output:

```
1. Fertilizer price increases (4 times — Mar, Jun, Aug, Nov)
2. Logistics cost renegotiation (3 — Feb, May, Sep)
3. New-hire onboarding online (3 — Jan, Apr, Oct)
4. System migration delays (3 — May, Jul, Dec)
5. Customer complaint standardization (2 — Jun, Nov)
```

### Result

- 360 KB of Word becomes 68 KB of searchable, analyzable Markdown
- 0.1-second theme search with `grep`
- Print-quality PDF in one command
- 5-second pattern extraction across a year

The structural insight "the organization debated the same theme four times" is **impossible to obtain from Word**.

---

## Example 02: Aggregate 100 Excel files in 30 seconds

→ Confirms Chapter 4 "[Holding Data](/en/ai-native-ways/data-formats/)"

### Setup

- Input: `stores/store-{001..100}.xlsx` (50 KB each, 5 MB total)
- Tools: `ssconvert` (from Gnumeric), `pandas`, Claude

### Steps

**Step 1: bulk Excel → CSV**

```bash
$ for f in stores/*.xlsx; do
>   ssconvert "$f" "${f%.xlsx}.csv" 2>/dev/null
> done
$ ls stores/*.csv | wc -l
100
$ du -sh stores/*.csv | awk '{sum+=$1} END {print sum"K"}'
1180K
```

5.4 MB → 1.18 MB (**one-quarter**). Formatting metadata was four times the data.

**Step 2: aggregation code from Claude**

```
You: 100 CSVs (date, item, qty, price). Write Python to compute monthly
     sales totals per item to a CSV.
```

Returned `aggregate.py` (15 lines):

```python
import pandas as pd, glob

dfs = [pd.read_csv(f) for f in glob.glob("stores/*.csv")]
df = pd.concat(dfs)
df["amount"] = df["qty"] * df["price"]
df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
summary = df.groupby(["month", "item"])["amount"].sum().reset_index()
summary.to_csv("summary.csv", index=False)
print(summary.head(10).to_string(index=False))
```

**Step 3: run**

```bash
$ time python3 aggregate.py
   month       item    amount
 2026-04   Cabbage   2156400
 2026-04     Onion   1842300
 2026-04    Carrot    987600
 2026-04    Tomato   3245100
 2026-04     Chive    654200
 ...

real    0m1.847s
```

**1.8 seconds for 100 files**.

**Step 4: chart from Claude**

```
You: From summary.csv, plot monthly trends of the top 5 items in
     matplotlib, with a calm professional palette.
```

Run the returned Python; `chart.png` (1280×720, 78 KB) appears with a polished palette.

**Step 5: cron automation**

```bash
$ crontab -e
0 1 1 * * cd /home/user/aggregate && python3 aggregate.py && \
          python3 chart.py | mail -s "monthly summary" boss@example.com
```

Manual 4 hours → automated zero.

### Result

- xlsx 5.4 MB → CSV 1.2 MB (one-quarter)
- Aggregation 4 hours → 1.8 seconds (8000x)
- Script is Git-versionable (Excel pivots aren't)
- Zero manual work from month two onward

---

## Example 03: Build a 20-page client proposal in 2 hours

→ Confirms Chapter 3 "[Designing](/en/ai-native-ways/design/)"

### Setup

- Tools: `pandoc`, `mmdc`, Claude
- Target: inventory management system proposal

### Steps

**Step 1: folder layout**

```bash
$ mkdir -p proposal-2026/{diagrams,mockups,assets}
```

**Step 2: Mermaid → SVG**

```bash
$ cat > proposal-2026/diagrams/architecture.mmd <<'EOF'
graph TD
  A[Field Terminal] -->|WebAPI| B[FastAPI]
  B --> C[(PostgreSQL)]
  B --> D[Admin Dashboard]
  D -.->|Alert| E[Field Terminal]
EOF

$ mmdc -i proposal-2026/diagrams/architecture.mmd \
       -o proposal-2026/diagrams/architecture.svg
✓ Generating single mermaid chart

$ ls -lh proposal-2026/diagrams/architecture.svg
-rw-r--r-- 1 user staff 4.2K architecture.svg
```

**Step 3: UI mockup via Claude Design**

```
You: Inventory dashboard UI. Product list, search, stock alerts,
     graphs. Calm Linear-style palette.
```

Save returned HTML+CSS as `mockups/dashboard.html`. 18 KB of working code.

**Step 4: assemble PDF**

```bash
$ pandoc proposal-2026/ja.md -o proposal-2026/proposal.pdf \
  --pdf-engine=xelatex --toc \
  -V mainfont="Hiragino Mincho Pro" \
  -V geometry:margin=2cm \
  --resource-path=proposal-2026

$ ls -lh proposal-2026/proposal.pdf
-rw-r--r-- 1 user staff 312K proposal.pdf
```

312 KB PDF: cover, ToC, architecture diagram, screen mockups, all integrated.

### Result

- Architecture (4.2 KB SVG) + UI mock (18 KB HTML) + PDF (312 KB)
- All sources are text/code, Git-versionable
- Client revisions take 30 seconds
- **Equivalent to a consulting proposal billed at 200K USD**

---

## Example 04: Extract amounts from 100 invoice PDFs

→ Confirms Chapter 1 "[Writing Logic](/en/ai-native-ways/python/)"

### Setup

- Input: `invoices/*.pdf` (100 files, mixed formats)
- Tools: `pdfplumber`, Claude

### Steps

**Step 1: code from Claude**

```
You: Extract "total amount" from each PDF in invoices/, output
     CSV (filename, amount). Assume Japanese PDFs.
```

Returned `extract.py` (20 lines):

```python
import pdfplumber, csv, re, glob

results = []
for path in glob.glob("invoices/*.pdf"):
    with pdfplumber.open(path) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    m = re.search(r"合計\s*[¥￥]?\s*([\d,]+)\s*円?", text)
    amount = int(m.group(1).replace(",", "")) if m else None
    results.append({"filename": path, "amount": amount})

with open("amounts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["filename", "amount"])
    w.writeheader()
    w.writerows(results)

print(f"total: {sum(r['amount'] or 0 for r in results):,} yen")
```

**Step 2: run**

```bash
$ time python3 extract.py
total: 12,345,678 yen

real    0m28.4s

$ head -5 amounts.csv
filename,amount
invoices/001.pdf,135200
invoices/002.pdf,89400
invoices/003.pdf,247800
invoices/004.pdf,
```

**100 PDFs in 28 seconds.** `004.pdf` failed.

**Step 3: pipe error to Claude**

```bash
$ python3 extract.py 2>&1 | claude -p \
    "Multiple None values. Fix the regex for varied invoice formats"
```

Returned fix:

```python
patterns = [
    r"合計\s*[¥￥]?\s*([\d,]+)\s*円?",
    r"ご請求金額\s*[¥￥]?\s*([\d,]+)",
    r"合計金額\s*[¥￥]?\s*([\d,]+)",
    r"Total\s*[¥￥]?\s*([\d,]+)",
]
amount = None
for pat in patterns:
    m = re.search(pat, text)
    if m:
        amount = int(m.group(1).replace(",", ""))
        break
```

Re-run:

```bash
$ python3 extract.py
total: 12,945,200 yen

$ awk -F, 'NR>1 && $2=="" {n++} END {print "missing:", n}' amounts.csv
missing: 0
```

**All 100 succeed.**

### Result

- 4 hours of manual work → 28 seconds + 5-minute fix
- Reuse next month with the same script
- Git-reviewable
- The next step (anomaly detection) follows the same flow

---

## Example 05: Monthly report cycle in 30 minutes

→ Confirms Chapter 5 "[Changing Paperwork](/en/ai-native-ways/office-replacement/)"

### Setup

- Input: `sales-2026-04.xlsx` from sales team
- Output: PDF emailed to boss
- Tools: `ssconvert`, `pandas`, Claude, `pandoc`, SMTP

### Steps

**Step 1: Excel → CSV → Markdown table**

```bash
$ ssconvert sales-2026-04.xlsx sales-2026-04.csv
$ python3 aggregate.py
| Store | Revenue (yen) |
|---|---:|
| Osaka HQ | 18,420,000 |
| Kobe | 12,150,000 |
| Kyoto | 9,830,000 |
| Nara | 6,470,000 |
```

**Step 2: analysis from Claude**

```bash
$ cat summary.md | claude -p \
    "Three notable trends from this monthly revenue, in polished business prose"
```

Output:

```
1. Osaka HQ posts +15% MoM, marking three consecutive months of growth.
   Urban foot-traffic recovery appears to be the driver.
2. Kobe maintains a steady +8%, while Nara has -3% for the third month.
   Trade-area analysis is needed.
3. All-store total +9.2% MoM, +12% YoY — exceeding the +8% plan.
```

**Step 3: assemble Markdown report**

```markdown
# Monthly Revenue Report — April 2026

## Summary
[Claude analysis]

## Per-Store Revenue
[summary.md table]

## Focus for Next Month
- Continue measures sustaining Osaka/Kobe growth
- Trade-area analysis for Nara by mid-May
```

**Step 4: PDF and HTML simultaneously**

```bash
$ pandoc report-2026-04.md -o report-2026-04.pdf \
    --pdf-engine=xelatex \
    -V mainfont="Hiragino Mincho Pro" --toc

$ pandoc report-2026-04.md -o report-2026-04.html --standalone --toc

$ ls -lh report-2026-04.*
-rw-r--r-- 1 user staff 142K report-2026-04.pdf
-rw-r--r-- 1 user staff  18K report-2026-04.html
```

**One Markdown produces PDF (for boss) and HTML (for wiki) at once.**

**Step 5: cron + send.py**

```cron
0 9 1 * * cd ~/monthly && ./run.sh
```

Drop next month's xlsx into `~/monthly/`. **Auto-emails the boss on the 1st at 9 AM.**

### Result

- 3 hours → 30 min (first run) → 5 min thereafter
- One Markdown → PDF + HTML simultaneously
- Past reports searchable and Git-diffable
- **45 hours/month freed**

---

## Example 06: Replace a PL/SQL stored procedure via parallel operation

→ Confirms Chapter 6 "[Working with Business Systems](/en/ai-native-ways/business-systems/)"

### Setup

- Old: Oracle `calc_monthly_billing` (PL/SQL, 500 lines, 20 years)
- New: PostgreSQL + Python (`psycopg`)
- Parallel operation: 3 months

### Steps

**Step 1: extract code and business knowledge**

```bash
$ sqlplus -S user/pass @export_proc.sql > calc_monthly_billing.sql
$ wc -l calc_monthly_billing.sql
523 calc_monthly_billing.sql

$ cat calc_monthly_billing.sql | claude -p \
    "Output (1) Markdown business spec and (2) Python (psycopg) translation"
```

Returned spec (excerpt):

```markdown
# calc_monthly_billing — Business Spec

## Rules (extracted from code)
1. Closing day: 23:59 on the 10th
2. Obon extension: July billing extended to 5th of following month (L.142-148)
3. Large-account exception: 100K+ accounts close early (L.215-228)
4. Holiday handling: weekends/holidays roll back to prior business day (L.301-322)
5. Tax rate switch: 10% from 2024-04, 8% before (L.401-415)
6. Rounding: per-customer choice of floor/ceil/round
7. Recalculation lock: past 3 months unmodifiable (L.450-468)
```

**Seven undocumented rules surface.**

**Step 2: 12 months of expected outputs**

```bash
$ sqlplus -S user/pass <<EOF > expected.csv
SELECT customer_id, billing_month, amount, calculated_at
FROM monthly_billing
WHERE billing_month >= TO_DATE('2025-04', 'YYYY-MM');
EOF
$ wc -l expected.csv
49,837 expected.csv
```

**Step 3: parallel run and compare**

```bash
$ python3 verify.py
[INFO] Running new calc_monthly_billing.py...
[INFO] Loaded expected.csv: 49836 rows
[INFO] Loaded actual.csv: 49836 rows
[INFO] Matching: 49829
[INFO] Diffs: 7
  (12345, 2025-07): old=1,256,400, new=1,256,400 (calculated_at differs by 1.2s)
  (54321, 2025-08): old=789,200, new=789,400 (DIFF: 200 yen)
  ...
```

**Step 4: pipe diffs to Claude**

```bash
$ python3 verify.py 2>&1 | claude -p "Identify cause vs PL/SQL"
```

Response:

```
Cause: Rounding rule (Rule 6) implementation incomplete.
PL/SQL reads customers.rounding_method ('floor'/'ceil'/'round'),
but Python uses 'round' for everyone.
Fix:
def round_amount(amount, method):
    if method == 'floor': return int(amount)
    if method == 'ceil':  return int(amount + 0.99)
    return round(amount)
```

After applying: `Diffs: 0`.

**Step 5: cron parallel operation in production**

```cron
# Old batch (kept)
0 1 1 * * sqlplus user/pass @run_old_billing.sql

# New batch (parallel)
0 2 1 * * python3 calc_monthly_billing.py

# Auto-compare
0 3 1 * * python3 compare.py | mail -s "billing diff" admin@example.com
```

**Step 6: 3 months later, kill the old**

```bash
$ tail -3 ~/billing-diff.log
2026-04-01 03:00:01 [INFO] Diffs: 0
2026-05-01 03:00:01 [INFO] Diffs: 0
2026-06-01 03:00:01 [INFO] Diffs: 0
```

Three months of zero diffs. Stop the old batch; don't renew Oracle license. **40M yen/year disappears.**

### Result

- 20-year-old PL/SQL becomes Markdown spec + 120 lines of Python + PostgreSQL in 3 months
- 7 hidden business rules now documented
- Oracle EE renewal canceled, 40M yen/year saved
- Zero SI vendor outsourcing fees (estimate had been 30M yen)

---

## Example 07: Personal blog worldwide in 30 minutes

→ Confirms Chapter 7 "[Building for the Web](/en/ai-native-ways/web/)"

### Setup

- Tools: Python, `markdown-it-py`, `Jinja2`, Cloudflare account, Git

### Steps

**Step 1: minimal layout**

```bash
$ mkdir myblog && cd myblog
$ mkdir -p src/posts templates html
```

**Step 2: build script from Claude**

```
You: Read src/posts/*.md, fill templates/post.html, write to
     html/posts/{slug}/index.html. Use markdown-it-py + Jinja2.
```

Returned `build.py` (45 lines):

```python
from pathlib import Path
import markdown_it, jinja2, frontmatter

md = markdown_it.MarkdownIt()
env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

posts = []
for src in sorted(Path("src/posts").glob("*.md")):
    post = frontmatter.load(src)
    body = md.render(post.content)
    out = Path(f"html/posts/{post['slug']}/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(env.get_template("post.html").render(
        title=post["title"], date=post["date"], body=body
    ))
    posts.append(post)

Path("html/index.html").write_text(
    env.get_template("index.html").render(posts=posts)
)
print(f"Built: {len(posts)} posts")
```

**Step 3: write a post and build**

```bash
$ uv add markdown-it-py Jinja2 python-frontmatter
$ python3 build.py
Built: 1 posts
$ time python3 build.py
real    0m0.183s
```

**Build time 0.18 seconds.** Next.js: 30 sec to 3 min.

**Step 4: deploy to Cloudflare Pages**

```bash
$ git init && git add -A && git commit -m "init"
$ git push -u origin main
```

Connect repo on Cloudflare Pages, set build command `python3 build.py`, output `html/`. **Live worldwide in 5 minutes.**

**Step 5: measure speed**

```bash
$ for region in tokyo singapore london nyc sydney; do
>   echo -n "$region: "
>   curl -w "%{time_total}\n" -o /dev/null -s \
>        https://myblog.pages.dev/posts/ai-native-ways/
> done
tokyo: 0.038
singapore: 0.052
london: 0.061
nyc: 0.043
sydney: 0.071
```

**Under 70ms anywhere.** WordPress + WP Engine averages 800ms+.

### Result

- 0.18-second builds (>100x Next.js)
- Cost: $0/month (vs WP Engine $30–200/month)
- 50ms worldwide
- 3 dependencies, zero `node_modules`

---

## Example 08: Photo-sort CLI on PyPI

→ Confirms Chapter 8 "[Building Apps](/en/ai-native-ways/apps/)"

### Setup

- Tools: Python, PyPI account, Claude

### Steps

**Step 1: structure from Claude**

```
You: CLI in Python that sorts jpg/jpeg by EXIF capture date.
     pyproject.toml + src layout + entry_point.
```

Returned tree:

```
photo-sort/
├── pyproject.toml
├── README.md
└── src/photo_sort/
    ├── __init__.py
    └── cli.py
```

**Step 2: review the code**

```python
# src/photo_sort/cli.py
import sys, shutil, os, argparse
from PIL import Image
from PIL.ExifTags import TAGS

def main():
    parser = argparse.ArgumentParser(description="Sort photos by capture date")
    parser.add_argument("folder")
    args = parser.parse_args()

    moved = 0
    for f in sorted(os.listdir(args.folder)):
        if not f.lower().endswith(('.jpg', '.jpeg')):
            continue
        path = os.path.join(args.folder, f)
        img = Image.open(path)
        exif = img._getexif() or {}
        date = next((v for t, v in exif.items() if TAGS.get(t) == 'DateTimeOriginal'), None)
        if not date: continue
        ymd = date[:10].replace(':', '-')
        target = os.path.join(args.folder, ymd)
        os.makedirs(target, exist_ok=True)
        shutil.move(path, os.path.join(target, f))
        moved += 1
    print(f"Moved {moved} photos")

if __name__ == "__main__":
    main()
```

**Step 3: local test**

```bash
$ uv tool install --editable .
$ photo-sort ~/Pictures/2026/
Moved 247 photos
$ ls ~/Pictures/2026/
2026-04-01/  2026-04-08/  2026-04-15/  2026-04-22/
```

**Step 4: upload to PyPI**

```bash
$ uv tool install build twine
$ python3 -m build
Successfully built photo-sort-0.1.0.tar.gz and photo_sort-0.1.0-py3-none-any.whl

$ twine upload dist/*
View at: https://pypi.org/project/photo-sort/0.1.0/
```

**5 minutes; live on PyPI.**

**Step 5: anyone can use it**

```bash
$ uv tool install photo-sort
Successfully installed photo-sort-0.1.0 Pillow-10.4.0
$ photo-sort ~/Pictures/
Moved 184 photos
```

### Result

- CLI to PyPI: 1 hour
- Distribution: `uv tool install photo-sort` (or `pip install photo-sort`)
- Cost: zero
- iOS App equivalent: 1 week + $99/year

---

## Example 09: Research-grade home garden sensing on ESP32

→ Confirms Chapter 9 "[Building Embedded](/en/ai-native-ways/embedded/)"

### Setup

- Hardware: ESP32 ($6) + DHT22 ($4) + soil moisture sensor ($3) + SSD1306 OLED ($5) + jumpers. **Total: $18**
- Tools: PC, MicroPython firmware, `ampy`

### Steps

**Step 1: validate logic on PC first**

```python
# detect.py
def should_water(temps, moistures):
    if len(temps) < 24: return False
    avg_temp = sum(temps[-24:]) / 24
    avg_moisture = sum(moistures[-24:]) / 24
    return avg_moisture < 30 and avg_temp > 25
```

```bash
$ python3 -c "from detect import should_water; ..." # 0.1 sec to validate
water: True
```

**Step 2: MicroPython translation from Claude**

```
You: Translate this Python to ESP32 MicroPython. DHT22 (GPIO4),
     soil moisture (ADC GPIO34), OLED (I2C SCL=22 SDA=21).
     Measure every 10 minutes.
```

Returned `main.py` (50 lines, with `detect.py` reused):

```python
from machine import Pin, ADC, I2C
import dht, time, ssd1306
from detect import should_water

dht22 = dht.DHT22(Pin(4))
adc = ADC(Pin(34))
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

temps, moistures = [], []
while True:
    dht22.measure()
    temps.append(dht22.temperature())
    moistures.append(adc.read() / 4095 * 100)
    if len(temps) > 144: temps.pop(0)
    if len(moistures) > 144: moistures.pop(0)
    advice = "Water!" if should_water(temps, moistures) else "OK"
    oled.fill(0)
    oled.text(f"Temp: {temps[-1]}C", 0, 0)
    oled.text(f"Moist: {moistures[-1]:.0f}%", 0, 16)
    oled.text(advice, 0, 32)
    oled.show()
    time.sleep(600)
```

**Step 3: transfer to ESP32**

```bash
$ ampy --port /dev/ttyUSB0 put detect.py
$ ampy --port /dev/ttyUSB0 put main.py
```

OLED display:

```
Temp: 28C
Moist: 25%
Water!
```

**Step 4: cloud aggregation**

5 lines added for HTTP POST. After a month:

```bash
$ cat data.csv | claude -p \
  "From this month's data, suggest optimal watering times"
```

```
Optimal watering: 6:00–7:00 AM
- Soil moisture retention is highest from morning watering
- Average maintains >35% even 14 hours later
- After 10:00 AM, moisture drops below 30% within 5 hours

Recommended schedule:
- Tue/Thu/Sat 6:30 AM, 5-minute timer
- On days >30°C, additional 18:00 watering, 3 minutes
```

**Agricultural-research-level insight from a $18 sensor.**

### Result

- $18 in parts → research-grade environmental monitoring
- PC validation cuts hardware-debugging time by 90%
- "Optimal watering schedule" from a month of data
- No IoT vendor contract (would be tens of dollars/month)

---

## Example 10: Replace AI agent with Python + cron

→ Confirms Chapter 10 "[Knowing What to Hand to AI](/en/ai-native-ways/ai-delegation/)"

### Setup

- Old: AI agent SaaS ($200/month, autonomous)
- New: Python + cron + Claude API
- Tools: Python, `anthropic` SDK, Slack Webhook

### Steps

**Step 1: code from Claude**

```
You: Fetch unread emails via IMAP, classify "urgent/normal/ignore"
     via Claude API, post summary of urgent ones to Slack.
     Configuration in env vars.
```

Returned `process.py` (60 lines).

**Step 2: run**

```bash
$ uv add anthropic requests
$ export ANTHROPIC_API_KEY=sk-ant-...
$ export SLACK_WEBHOOK=https://hooks.slack.com/...

$ python3 process.py
processed 8 mails, alerts: 1
```

Slack message:

```
🚨 Urgent: Vendor A delivery delay
classification: urgent
summary: 1,200 units due 5/3 may slip to 5/10
recommended action: contact sales lead, secure alternative source
```

**Step 3: cron every 15 minutes**

```cron
*/15 * * * * cd ~/email-agent && /usr/bin/python3 process.py >> ~/email-agent.log 2>&1
```

**Step 4: cost after one month**

```bash
$ awk '/processed/ {sum+=$2} END {print sum}' ~/email-agent.log
2847
```

2,847 emails classified. Anthropic dashboard:

```
April 2026:
Total tokens: 1,847,253
Total cost: $4.62
```

**$4.62/month vs $200/month — 43x cheaper.**

### Result

- 43x cost reduction
- Data stays on your server
- Logic frozen in code (reproducible, verifiable)
- Zero autonomous-mode risk (no prompt-injection takeover)

---

## Example 11: Launch a SaaS in 1 month, solo

→ Confirms Chapter 12 "[One Person + AI](/en/ai-native-ways/one-plus-ai/)"

### Setup

- Product: Markdown meeting-notes analysis SaaS
- Price: $20/month
- Tools: Python, PostgreSQL, Stripe, Hetzner VPS ($5/month)

### Timeline

**Day 1: spec in Markdown**

```bash
$ cat > spec.md <<EOF
# Markdown Meeting Notes SaaS

## Problem
Meeting notes scatter across Word; can't search or analyze

## Features
1. Markdown notes upload
2. Claude summarization and action extraction
3. Pattern analysis across 12 months
4. $20/month, 14-day free trial
EOF
```

**Day 2-3: schema + API**

```bash
$ cat spec.md | claude -p "PostgreSQL schema + FastAPI endpoints with Pydantic, async, pytest"
```

Returns: `schema.sql` (50 lines DDL), `main.py` (250 lines), `tests/` (100 lines).

**Day 4-7: frontend**

```
You: Notes upload, analysis view, dashboard. Linear-style calm UI, pure CSS.
```

5 templates + 800 lines of CSS.

**Day 8-10: Stripe billing**

```python
import stripe, os
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

def create_checkout_session(user_email):
    return stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": "price_1AbC...", "quantity": 1}],
        customer_email=user_email,
        success_url="https://app.example.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://app.example.com/cancel",
    ).url
```

**Day 11-15: tests**

```bash
$ pytest tests/ -v
========== 9 passed ==========
```

**Day 16-20: deploy to VPS**

```bash
$ ssh root@my-vps  # Hetzner CX21, $5/month
$ docker compose up -d
$ curl https://minutes.example.com/health
{"status": "ok", "db": "connected"}
```

Caddy auto-provisions HTTPS.

**Day 21-25: legal + landing page**

Lawyer review of Claude-drafted ToS/privacy policy: $500.

**Day 26-30: launch**

Submit to Product Hunt, Hacker News, Twitter.

**Day 30 stats**:

```bash
$ curl -s https://minutes.example.com/admin/stats | jq
{
  "users": 312,
  "trial_active": 184,
  "subscriptions": 41,
  "monthly_revenue_usd": 820
}
```

**41 paying customers, $820/month revenue.** First month total cost: VPS $5 + Claude $50 + Stripe fees + lawyer $500 = **$600**.

### Result

- 0 → revenue in one month
- All features built solo (auth, billing, webhooks, analysis, dashboard, legal, marketing)
- 10 years ago: 5-person team, 6 months
- **A unicorn now starts from one person**

---

## In summary

Common across all 12 walkthroughs: **use AI as a generator and freeze results into code, commands, and files**.

- Word → Markdown (Example 01)
- Excel → CSV + Python (Example 02)
- Proposal → text + code (Example 03)
- Manual work → Python (Examples 04, 05)
- Legacy → parallel rewrite (Example 06)
- Web → minimal stack (Example 07)
- Apps → from CLI up (Example 08)
- Embedded → Python design (Example 09)
- AI agents → Python (Example 10)
- One person + AI → real business (Example 11)

Each runs in **2 to 30 minutes**. Don't try to read everything first; **pick one that interests you and run it**. That is how AI-native work begins.

---

## Related

- [Prologue: Office for paperwork, Java/C# for business systems — but AI runs on Python and text](/en/ai-native-ways/prologue/)
- [Chapter 12: One Person + AI — The New Unit of Work](/en/ai-native-ways/one-plus-ai/)
