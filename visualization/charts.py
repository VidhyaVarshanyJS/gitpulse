import plotly.express as px
import plotly.graph_objects as go
class Charts:
    @staticmethod
    def plot_commit_frequency(metrics_df):
        """Creates a bar chart for commit frequency with proper formatting."""
        if "commit_frequency" not in metrics_df.columns or metrics_df.empty:
            return go.Figure()  # Return an empty figure if no data

        fig = px.bar(
            metrics_df,
            x="repo_name",
            y="commit_frequency",
            title="Commit Frequency by Repository",
            labels={"commit_frequency": "Commits per Day", "repo_name": "Repository"},
            template="plotly_dark",  # Use dark theme to align with the overall design
            text_auto=True,
            color='commit_frequency',
            color_continuous_scale='Blues'  # Gradient color for visual appeal
        )
        fig.update_layout(title_font_size=18, xaxis_title="Repository", yaxis_title="Commits per Day")
        fig.update_traces(textposition='outside', hoverinfo="x+y")
        return fig

    @staticmethod
    def plot_pr_merge_rate(metrics_df):
        """Creates a gauge chart to show PR merge rate."""
        if "pr_merge_rate" not in metrics_df.columns or metrics_df.empty:
            return go.Figure()

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=metrics_df["pr_merge_rate"].iloc[0] * 100,
            title={"text": "PR Merge Rate (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4}, 
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        return fig


    @staticmethod
    def plot_issue_resolution_time(metrics_df):
        """Creates a bar chart for issue resolution time."""
        if "issue_resolution_time" not in metrics_df.columns or metrics_df.empty:
            return go.Figure()

        fig = px.bar(
            metrics_df,
            x="repo_name",
            y="issue_resolution_time",
            title="Issue Resolution Time by Repository",
            labels={"issue_resolution_time": "Days to Resolve Issues", "repo_name": "Repository"},
            template="plotly_dark",
            text_auto=True,
            color='issue_resolution_time',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(xaxis_title="Repository", yaxis_title="Days to Resolve Issues")
        fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, textposition='outside')
        return fig


    # New chart for PR Lead Time
    @staticmethod
    def plot_pr_lead_time(metrics_df):
        if "pr_lead_time" not in metrics_df.columns or metrics_df.empty:
            return go.Figure()

        fig = px.bar(
        metrics_df,
        x="repo_name",
        y="pr_lead_time",  # Adjust for pr_review_time
        title="PR Lead Time by Repository",
        labels={"pr_lead_time": "PR Lead Time (days)", "repo_name": "Repository"},
        template="plotly_dark",
        text_auto=True,
        color='pr_lead_time',
        color_continuous_scale='Cividis'
    )
        fig.update_layout(xaxis_title="Repository", yaxis_title="PR Lead Time (days)")
        fig.update_traces(textposition='outside', hoverinfo="x+y+text")
        return fig


    # New chart for PR Review Time
    @staticmethod
    def plot_pr_review_time(metrics_df):
        if "pr_review_time" not in metrics_df.columns or metrics_df.empty:
            return go.Figure()

        fig = px.bar(
        metrics_df,
        x="repo_name",
        y="pr_lead_time",  # Adjust for pr_review_time
        title="PR Lead Time by Repository",
        labels={"pr_lead_time": "PR Lead Time (days)", "repo_name": "Repository"},
        template="plotly_dark",
        text_auto=True,
        color='pr_lead_time',
        color_continuous_scale='Cividis'
    )
        fig.update_layout(xaxis_title="Repository", yaxis_title="PR Lead Time (days)")
        fig.update_traces(textposition='outside', hoverinfo="x+y+text")
        return fig

