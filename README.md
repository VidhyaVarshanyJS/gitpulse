# GitPulse: Developer Performance Analytics Platform

<div align="center">
  <img src="gitpulse.png" alt="GitPulse Logo" width="200" height="200">
</div>

## 🚀 Project Overview

GitPulse is an advanced GitHub repository analytics platform that transforms raw development data into actionable insights. By combining sophisticated data collection, natural language processing, and interactive visualizations, GitPulse empowers development teams to understand and optimize their performance.

## ✨ Key Features

### 📊 Comprehensive Metrics Tracking
- **Commit Analysis**
  - Frequency tracking
  - Time-based distribution
  - Developer contribution insights

- **Pull Request Metrics**
  - Merge rates
  - Lead time calculations
  - Review complexity analysis

- **Issue Management**
  - Resolution time tracking
  - Priority-based insights
  - Bottleneck identification

### 🤖 Intelligent Query Interface
- **Natural Language Processing**
  - Powered by Groq's LLaMA model
  - Two-tier query support:
    1. Precise metric queries
    2. Contextual project information retrieval

### 📈 Advanced Visualization
- **Interactive Plotly Dashboards**
  - Real-time performance charts
  - Customizable metric views
  - Trend analysis graphics

### 🔄 Multi-Repository Support
- Seamless repository switching
- Consolidated performance tracking
- Comparative analytics

## 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, PyGithub |
| **NLP** | Groq LLaMA Model |
| **Frontend** | Streamlit |
| **Visualization** | Plotly |
| **Data Processing** | Pandas, NumPy |

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- GitHub API Token
- Groq API Credentials

### Quick Start
```bash
# Clone the repository
git clone https://github.com/vidhyavarshanyjs/gitpulse.git
cd gitpulse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GITHUB_TOKEN='your_github_token'
export GROQ_API_KEY='your_groq_api_key'

# Launch the application
streamlit run app.py
```

## 🚀 Usage Examples

### Metric Queries
- "What's our commit frequency this month?"
- "Show PR merge rates for Team A"
- "Compare issue resolution times across repositories"

### Contextual Queries
- "Summarize our team's development performance"
- "Identify potential workflow bottlenecks"
- "Generate developer productivity report"

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md] file for details.

## 🙌 Acknowledgments
- GitHub API
- Groq for NLP capabilities
- Streamlit Community
- Open-source contributors

---

**GitPulse: Transforming Data into Developer Insights** 📊🚀

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=vidhyavarshanyjs/gitpulse&type=Date)](https://star-history.com/#vidhyavarshanyjs/gitpulse&Date)
