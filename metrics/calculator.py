from metrics.definitions import MetricsDefinitions
import pandas as pd
class MetricsCalculator:
    def __init__(self, repo_data):
        self.repo_data = repo_data

    def calculate_metrics(self):
        """Calculates performance metrics for the given repository data."""
        commits = list(self.repo_data['commits'])
        pull_requests = list(self.repo_data['pull_requests'])
        issues = list(self.repo_data['issues'])

        metrics = {
            "repo_name": self.repo_data['repo_name'],
            "commit_frequency": MetricsDefinitions.calculate_commit_frequency(commits),
            "pr_merge_rate": MetricsDefinitions.calculate_pr_merge_rate(pull_requests),
            "issue_resolution_time": MetricsDefinitions.calculate_issue_resolution_time(issues),
            "active_days": MetricsDefinitions.calculate_active_days(commits),
            "pr_lead_time": MetricsDefinitions.calculate_pr_lead_time(pull_requests),
            "issue_reopen_rate": MetricsDefinitions.calculate_issue_reopen_rate(issues),
            "pr_review_time": MetricsDefinitions.calculate_pr_review_time(pull_requests),
            "bus_factor": MetricsDefinitions.calculate_bus_factor(self.repo_data['contributors_count']),
        }
        return pd.DataFrame([metrics])
