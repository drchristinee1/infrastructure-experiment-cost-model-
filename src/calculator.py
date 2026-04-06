from src.models import CostRates, DriverAssumptions, ExperimentInput


def calculate_usage_impact(
    experiment: ExperimentInput,
    drivers: DriverAssumptions,
) -> dict:
    additional_daily_requests = experiment.additional_daily_requests

    additional_lambda_invocations = (
        additional_daily_requests * drivers.lambda_invocations_per_request
    )

    additional_lambda_gb_seconds = (
        additional_lambda_invocations
        * (drivers.avg_lambda_duration_ms / 1000)
        * (drivers.lambda_memory_mb / 1024)
    )

    additional_dynamodb_reads = (
        additional_daily_requests * drivers.dynamodb_reads_per_request
    )

    additional_dynamodb_writes = (
        additional_daily_requests * drivers.dynamodb_writes_per_request
    )

    additional_log_volume_kb = (
        additional_daily_requests
        * drivers.log_events_per_request
        * drivers.avg_log_size_kb
    )

    log_volume_gb = additional_log_volume_kb / 1024 / 1024

    return {
        "additional_daily_requests": additional_daily_requests,
        "additional_lambda_invocations": additional_lambda_invocations,
        "additional_lambda_gb_seconds": additional_lambda_gb_seconds,
        "additional_dynamodb_reads": additional_dynamodb_reads,
        "additional_dynamodb_writes": additional_dynamodb_writes,
        "additional_log_volume_kb": additional_log_volume_kb,
        "log_volume_gb": log_volume_gb,
    }


def calculate_cost_output(
    usage: dict,
    rates: CostRates,
    experiment: ExperimentInput,
) -> dict:
    lambda_request_cost = (
        usage["additional_lambda_invocations"] / 1_000_000
    ) * rates.lambda_requests_per_1m

    lambda_compute_cost = (
        usage["additional_lambda_gb_seconds"]
        * rates.lambda_compute_per_gb_second
    )

    dynamodb_read_cost = (
        usage["additional_dynamodb_reads"] / 1_000_000
    ) * rates.dynamodb_reads_per_1m

    dynamodb_write_cost = (
        usage["additional_dynamodb_writes"] / 1_000_000
    ) * rates.dynamodb_writes_per_1m

    cloudwatch_log_cost = (
        usage["log_volume_gb"] * rates.cloudwatch_logs_per_gb
    )

    total_daily_cost_impact = (
        lambda_request_cost
        + lambda_compute_cost
        + dynamodb_read_cost
        + dynamodb_write_cost
        + cloudwatch_log_cost
    )

    total_monthly_cost_impact = (
        total_daily_cost_impact * experiment.experiment_duration_days
    )

    annualized_cost_impact = total_daily_cost_impact * 365

    return {
        "lambda_request_cost": lambda_request_cost,
        "lambda_compute_cost": lambda_compute_cost,
        "dynamodb_read_cost": dynamodb_read_cost,
        "dynamodb_write_cost": dynamodb_write_cost,
        "cloudwatch_log_cost": cloudwatch_log_cost,
        "total_daily_cost_impact": total_daily_cost_impact,
        "total_monthly_cost_impact": total_monthly_cost_impact,
        "annualized_cost_impact": annualized_cost_impact,
    }