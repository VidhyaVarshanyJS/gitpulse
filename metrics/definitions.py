class MetricsDefinitions:
    @staticmethod
    def calculate_commit_frequency(commits):
        """Calculate the commit frequency (total number of commits per day)."""
        total_days = (commits[-1].commit.author.date - commits[0].commit.author.date).days
        return len(commits) / total_days if total_days > 0 else 0

    @staticmethod
    def calculate_pr_merge_rate(pull_requests):
        """Calculate the pull request merge rate."""
        merged_prs = [pr for pr in pull_requests if pr.merged]
        return len(merged_prs) / len(pull_requests) if pull_requests else 0

    @staticmethod
    def calculate_issue_resolution_time(issues):
        """Calculate the average issue resolution time in days."""
        resolution_times = [(issue.closed_at - issue.created_at).days for issue in issues if issue.state == 'closed']
        return sum(resolution_times) / len(resolution_times) if resolution_times else 0

    @staticmethod
    def calculate_active_days(commits):
        """Calculate the number of active days."""
        unique_days = set(commit.commit.author.date.date() for commit in commits)
        return len(unique_days)

    @staticmethod
    def calculate_pr_lead_time(pull_requests):
        """Calculate the average time taken for PRs to be merged."""
        lead_times = [(pr.merged_at - pr.created_at).days for pr in pull_requests if pr.merged]
        return sum(lead_times) / len(lead_times) if lead_times else 0

    @staticmethod
    def calculate_issue_reopen_rate(issues):
        """Calculate the percentage of issues that were reopened."""
        reopened_issues = [issue for issue in issues if issue.reactions['+1'] > 0]  # Simulating reopened as having reactions
        return len(reopened_issues) / len(issues) if issues else 0

    @staticmethod
    def calculate_pr_review_time(pull_requests):
        """Calculate the average PR review time in days."""
        review_times = [(review.submitted_at - pr.created_at).days for pr in pull_requests for review in pr.get_reviews()]
        return sum(review_times) / len(review_times) if review_times else 0

    @staticmethod
    def calculate_bus_factor(contributors_count):
        """Estimate the bus factor, assuming it's the number of contributors divided by a factor."""
        return max(1, contributors_count // 100)  # Example logic
