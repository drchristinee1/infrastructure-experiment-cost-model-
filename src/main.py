from dataclasses import asdict

from src.calculator import calculate_cost_output, calculate_usage_impact
from src.config import (
    get_default_drivers,
    get_default_experiment,
    get_default_rates,
)
from src.reporter import print_section


def main() -> None:
    experiment = get_default_experiment()
    drivers = get_default_drivers()
    rates = get_default_rates()

    usage = calculate_usage_impact(experiment, drivers)
    costs = calculate_cost_output(usage, rates, experiment)

    experiment_summary = asdict(experiment)
    experiment_summary["additional_daily_users"] = experiment.additional_daily_users
    experiment_summary["additional_daily_requests"] = experiment.additional_daily_requests

    print_section("Experiment Input", experiment_summary)
    print_section("Driver Assumptions", asdict(drivers))
    print_section("Usage Impact", usage)
    print_section("Cost Output", costs)


if __name__ == "__main__":
    main()