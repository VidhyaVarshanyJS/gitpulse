import os
from groq import Groq
import pandas as pd

class NLPProcessor:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def process_query(self, query: str, metrics_df: pd.DataFrame) -> str:
        """
        Processes the user's query using Groq API and returns the result.
        
        :param query: User's natural language question.
        :param metrics_df: DataFrame containing repository metrics.
        :return: NLP-generated response to the user's query.
        """
        try:
            # Include repository information as part of the query context
            repo_insights = "This repository has the following metrics: "
            for col in metrics_df.columns:
                repo_insights += f"{col}: {metrics_df[col].values[0]}. "

            # Formatting the query with more repository/project insights
            formatted_query = f"You are a helpful assistant. Provide a response based on these repository metrics: {repo_insights}. Question: {query}"

            # Sending the query to Groq's API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": formatted_query,
                    }
                ],
                model="llama3-8b-8192",
            )

            # Extracting and returning the response from Groq
            response = chat_completion.choices[0].message.content
            return response

        except Exception as e:
            return f"An error occurred while processing the query: {e}"
