from src.models import CostRates, DriverAssumptions, ExperimentInput


def get_default_experiment() -> ExperimentInput:
    return ExperimentInput(
        experiment_name="Recommendation UI Test",
        baseline_daily_users=100_000,
        treatment_lift_pct=0.08,
        requests_per_user=12,
        experiment_duration_days=30,
    )


def get_default_drivers() -> DriverAssumptions:
    return DriverAssumptions(
        lambda_invocations_per_request=1,
        avg_lambda_duration_ms=250,
        lambda_memory_mb=512,
        dynamodb_reads_per_request=2,
        dynamodb_writes_per_request=0.2,
        log_events_per_request=3,
        avg_log_size_kb=2,
    )


def get_default_rates() -> CostRates:
    return CostRates(
        lambda_requests_per_1m=0.20,
        lambda_compute_per_gb_second=0.000016667,
        dynamodb_reads_per_1m=0.125,
        dynamodb_writes_per_1m=0.625,
        cloudwatch_logs_per_gb=0.50,
    )