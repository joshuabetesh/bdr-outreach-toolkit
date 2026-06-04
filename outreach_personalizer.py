"""
outreach_personalizer.py
BDR Outreach Personalizer — Joshua Betesh
Generates personalized cold outreach emails from a prospect CSV.
Usage: python outreach_personalizer.py prospects.csv
"""

import csv
import sys
import json
from datetime import datetime


TEMPLATE = """
Subject: {first_name} — quick question re: {company}

Hi {first_name},

I came across {company} while researching companies in the {industry} space —
specifically around partner-led growth and co-sell motions.

I noticed {company} {hook}. That's exactly the wedge we help {industry} 
companies open with cloud marketplace and ecosystem partners.

Worth a 15-minute call this week to see if there's a fit?

Best,
Joshua Betesh
joshuabetesh@gmail.com | (305) 747-4271
linkedin.com/in/joshua-betesh-79bb38332
""".strip()


HOOKS = {
      "SaaS": "is scaling its partner channel",
      "Healthcare": "has a growing network of technology integrations",
      "Real Estate": "works with multiple enterprise platform vendors",
      "default": "is building out its go-to-market partnerships",
}


def load_prospects(filepath: str) -> list[dict]:
      """Load prospects from a CSV file."""
      prospects = []
      with open(filepath, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                              prospects.append(row)
                      print(f"[+] Loaded {len(prospects)} prospects from {filepath}")
            return prospects


def personalize(prospect: dict) -> str:
      """Generate a personalized email for one prospect."""
    industry = prospect.get("industry", "default")
    hook = HOOKS.get(industry, HOOKS["default"])
    return TEMPLATE.format(
              first_name=prospect.get("first_name", "there"),
              company=prospect.get("company", "your company"),
              industry=industry,
              hook=hook,
    )


def run(filepath: str):
      prospects = load_prospects(filepath)
    output = []
    for p in prospects:
              email = personalize(p)
              output.append({
                  "prospect": f"{p.get('first_name')} {p.get('last_name')}",
                  "company": p.get("company"),
                  "email": email,
              })
              print(f"\n{'='*60}")
              print(f"To: {p.get('first_name')} {p.get('last_name')} @ {p.get('company')}")
              print(f"{'='*60}")
              print(email)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"outreach_{timestamp}.json"
    with open(outfile, "w") as f:
              json.dump(output, f, indent=2)
          print(f"\n[+] Saved {len(output)} emails to {outfile}")


if __name__ == "__main__":
      if len(sys.argv) < 2:
                print("Usage: python outreach_personalizer.py <prospects.csv>")
                print("\nExpected CSV columns: first_name, last_name, company, industry, title")
                sys.exit(1)
            run(sys.argv[1])
