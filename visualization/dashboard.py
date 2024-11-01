import streamlit as st
from visualization.charts import Charts

class Dashboard:
    def __init__(self, metrics_df):
        self.metrics_df = metrics_df

    def display(self):
        """Displays repository metrics with charts on Streamlit."""
        st.plotly_chart(Charts.plot_commit_frequency(self.metrics_df))
        st.plotly_chart(Charts.plot_pr_merge_rate(self.metrics_df))
        st.plotly_chart(Charts.plot_issue_resolution_time(self.metrics_df))
        st.plotly_chart(Charts.plot_pr_lead_time(self.metrics_df))  # New
        st.plotly_chart(Charts.plot_pr_review_time(self.metrics_df))  # New
