from dataclasses import dataclass


@dataclass
class ExperimentInput:
    experiment_name: str
    baseline_daily_users: float
    treatment_lift_pct: float
    requests_per_user: float
    experiment_duration_days: int

    @property
    def additional_daily_users(self) -> float:
        return self.baseline_daily_users * self.treatment_lift_pct

    @property
    def additional_daily_requests(self) -> float:
        return self.additional_daily_users * self.requests_per_user


@dataclass
class DriverAssumptions:
    lambda_invocations_per_request: float
    avg_lambda_duration_ms: float
    lambda_memory_mb: float
    dynamodb_reads_per_request: float
    dynamodb_writes_per_request: float
    log_events_per_request: float
    avg_log_size_kb: float


@dataclass
class CostRates:
    lambda_requests_per_1m: float
    lambda_compute_per_gb_second: float
    dynamodb_reads_per_1m: float
    dynamodb_writes_per_1m: float
    cloudwatch_logs_per_gb: float