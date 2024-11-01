import streamlit as st
import pandas as pd

class ResponseGenerator:
    def display_response(self, response: str) -> str:
        """
        Displays the generated response in the Streamlit app.
        
        :param response: The response from the NLP processor.
        :return: The response as a string to be displayed.
        """
        st.markdown("### Response to your query:")

        
        # Example: If the response involves a specific metric, trigger a plot
        if "commits" in response.lower():
            self.plot_metric("Commits Over Time")
        
        # Add logic for other relevant metrics or data visualizations
        return response

    def plot_metric(self, metric_name: str):
        """
        Simulate the display of a metric visualization based on a query.
        
        :param metric_name: The name of the metric to plot.
        """
        st.markdown(f"#### {metric_name} visualization")
        # Example of creating a simple plot (you can replace this with real data)
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [10, 20, 15, 25], label=metric_name)
        ax.set_xlabel('Time')
        ax.set_ylabel(metric_name)
        ax.legend()
        st.pyplot(fig)
