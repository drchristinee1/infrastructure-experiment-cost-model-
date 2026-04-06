```markdown
# Infrastructure Experiment Cost Model

A driver-based Python model that estimates the infrastructure cost impact of product experiments.

---

## 🔍 Problem

Most A/B tests optimize for user behavior — but ignore infrastructure cost impact.

This creates blind spots:
- Features scale successfully
- Infrastructure costs silently increase
- Cost-to-serve is not evaluated alongside product lift

---

## 💡 Solution

This model bridges that gap by translating experiment-driven traffic changes into:

- Infrastructure usage (Lambda, DynamoDB, logging)
- Cost impact (daily, monthly, annualized)
- Cost-to-serve visibility

---

## 🧠 Key Idea

Product behavior → Infrastructure demand → Cloud cost

This model makes that relationship explicit and measurable.

---

## ⚙️ What the Model Does

The model starts with experiment assumptions such as:
- Baseline daily users
- Treatment lift (%)
- Requests per user
- Experiment duration

It then translates those assumptions into infrastructure drivers:
- Lambda invocations and compute (GB-seconds)
- DynamoDB reads and writes
- CloudWatch log volume

Finally, it applies pricing assumptions to estimate:
- Daily cost impact
- Monthly cost impact
- Annualized cost impact

---

## 🧩 Architecture

```

Experiment Input
→ Driver Assumptions
→ Usage Impact
→ Cost Rates
→ Cost Output

```

---

## 📁 Project Structure

```

src/
├── models.py        # Data structures (Experiment, Drivers, Rates)
├── config.py        # Default assumptions
├── calculator.py    # Usage + cost calculations
├── reporter.py      # Output formatting
└── main.py          # Entry point

data/                # Sample inputs
docs/                # Architecture explanation
outputs/             # Example outputs

````

---

## ▶️ How to Run

```bash
python -m src.main
````

---

## 📊 Example Insight

An experiment increases traffic by 8%.

This results in:

* Increased Lambda invocations
* Higher compute consumption
* More DynamoDB operations
* Increased logging volume

👉 All translated into projected cost impact before full rollout.

---

## 🧭 FinOps Perspective

This project reflects a core FinOps principle:

> Engineering decisions should be evaluated not only by performance and user impact, but also by their economic impact.

By modeling cost at the experiment level, teams can make more informed decisions before scaling.

---

## 🚀 Future Enhancements

* Control vs Treatment comparison
* ROI layer (revenue vs cost)
* Latency impact modeling
* Scenario analysis (low / expected / high traffic)
* Streamlit dashboard for visualization
* Integration with AWS CUR or CloudWatch metrics

---

````

