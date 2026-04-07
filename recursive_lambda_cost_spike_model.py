# recursive_lambda_cost_spike_model.py

"""
Recursive Lambda Cost Spike Model

Purpose:
Estimate the cost impact of a normal Lambda workload versus a recursive
or runaway invocation spike.

This script helps you understand:
1. Request cost
2. Compute cost
3. Total Lambda cost
4. Unit economics (cost per invocation)
5. How much a recursive spike increases cost
"""

# -----------------------------
# Lambda pricing assumptions
# -----------------------------
REQUEST_PRICE_PER_MILLION = 0.20
COMPUTE_PRICE_PER_GB_SECOND = 0.0000166667


def calculate_gb_seconds(invocations: int, avg_duration_ms: float, memory_mb: int) -> float:
    """
    Convert Lambda usage into GB-seconds.

    Formula:
    GB-seconds = invocations × duration_seconds × memory_GB
    """
    duration_seconds = avg_duration_ms / 1000
    memory_gb = memory_mb / 1024
    gb_seconds = invocations * duration_seconds * memory_gb
    return gb_seconds


def calculate_request_cost(invocations: int) -> float:
    """
    Calculate Lambda request cost.

    Formula:
    (invocations / 1,000,000) × request price
    """
    return (invocations / 1_000_000) * REQUEST_PRICE_PER_MILLION


def calculate_compute_cost(gb_seconds: float) -> float:
    """
    Calculate Lambda compute cost.

    Formula:
    GB-seconds × compute price per GB-second
    """
    return gb_seconds * COMPUTE_PRICE_PER_GB_SECOND


def calculate_unit_economics(total_cost: float, invocations: int) -> tuple:
    """
    Calculate cost per invocation and cost per 1,000 invocations.
    """
    if invocations == 0:
        return 0.0, 0.0

    cost_per_invocation = total_cost / invocations
    cost_per_1000_invocations = cost_per_invocation * 1000
    return cost_per_invocation, cost_per_1000_invocations


def calculate_total_cost(invocations: int, avg_duration_ms: float, memory_mb: int) -> dict:
    """
    Return a cost breakdown for a given Lambda workload.
    """
    gb_seconds = calculate_gb_seconds(invocations, avg_duration_ms, memory_mb)
    request_cost = calculate_request_cost(invocations)
    compute_cost = calculate_compute_cost(gb_seconds)
    total_cost = request_cost + compute_cost
    cost_per_invocation, cost_per_1000_invocations = calculate_unit_economics(total_cost, invocations)

    return {
        "invocations": invocations,
        "avg_duration_ms": avg_duration_ms,
        "memory_mb": memory_mb,
        "gb_seconds": gb_seconds,
        "request_cost": request_cost,
        "compute_cost": compute_cost,
        "total_cost": total_cost,
        "cost_per_invocation": cost_per_invocation,
        "cost_per_1000_invocations": cost_per_1000_invocations,
    }


def print_cost_summary(title: str, result: dict) -> None:
    """
    Print a clean summary of Lambda cost results.
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(f"Invocations                : {result['invocations']:,}")
    print(f"Avg Duration (ms)          : {result['avg_duration_ms']:,}")
    print(f"Memory (MB)                : {result['memory_mb']:,}")
    print(f"GB-Seconds                 : {result['gb_seconds']:,.4f}")
    print(f"Request Cost ($)           : {result['request_cost']:,.6f}")
    print(f"Compute Cost ($)           : {result['compute_cost']:,.6f}")
    print(f"Total Cost ($)             : {result['total_cost']:,.6f}")
    print(f"Cost per Invocation ($)    : {result['cost_per_invocation']:,.10f}")
    print(f"Cost per 1,000 Invocations : {result['cost_per_1000_invocations']:,.6f}")


def print_spike_comparison(normal_result: dict, spike_result: dict) -> None:
    """
    Compare normal Lambda workload to recursive spike workload.
    """
    extra_invocations = spike_result["invocations"] - normal_result["invocations"]
    extra_cost = spike_result["total_cost"] - normal_result["total_cost"]

    if normal_result["total_cost"] > 0:
        percent_increase = (extra_cost / normal_result["total_cost"]) * 100
    else:
        percent_increase = 0

    print("\n" + "-" * 60)
    print("SPIKE IMPACT ANALYSIS")
    print("-" * 60)
    print(f"Extra Invocations          : {extra_invocations:,}")
    print(f"Extra Cost ($)             : {extra_cost:,.6f}")
    print(f"Cost Increase (%)          : {percent_increase:,.2f}%")


def main():
    print("\nRecursive Lambda Cost Spike Model")
    print("Compare a normal Lambda workload vs a recursive spike scenario.\n")

    # Normal workload inputs
    print("Enter NORMAL workload assumptions:")
    normal_invocations = int(input("Normal number of invocations: "))
    avg_duration_ms = float(input("Average duration per invocation (ms): "))
    memory_mb = int(input("Memory size (MB): "))

    # Recursive spike inputs
    print("\nEnter RECURSIVE SPIKE assumptions:")
    spike_invocations = int(input("Spike number of invocations: "))

    # Calculate both scenarios
    normal_result = calculate_total_cost(normal_invocations, avg_duration_ms, memory_mb)
    spike_result = calculate_total_cost(spike_invocations, avg_duration_ms, memory_mb)

    # Print results
    print_cost_summary("NORMAL WORKLOAD COST SUMMARY", normal_result)
    print_cost_summary("RECURSIVE SPIKE COST SUMMARY", spike_result)
    print_spike_comparison(normal_result, spike_result)

    # Explanation
    print("\n" + "-" * 60)
    print("FORMULA EXPLANATION")
    print("-" * 60)
    print("1. Request cost depends on how many times the Lambda function runs.")
    print("2. Compute cost depends on:")
    print("   - invocation count")
    print("   - execution duration")
    print("   - memory allocated")
    print("3. Unit economics shows how much one invocation costs on average.")
    print("4. A recursive spike increases invocations quickly, which increases")
    print("   request cost, compute cost, and total financial impact.")


if __name__ == "__main__":
    main()