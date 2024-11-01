import streamlit as st
import plotly.express as px
from data_collection.github_api import GitHubDataCollector
from data_collection.data_storage import store_data_to_csv
from metrics.calculator import MetricsCalculator
from visualization.dashboard import Dashboard
from query_interface.nlp_processor import NLPProcessor
from query_interface.response_generator import ResponseGenerator
import matplotlib.pyplot as plt


# Cache the result of GitHub API calls to avoid repeated calls
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_repositories_and_stats(username):
    data_collector = GitHubDataCollector()
    repos = data_collector.get_user_repositories(username)
    dev_stats = data_collector.get_user_info(username)
    return repos, dev_stats

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_repository_data(repo_name):
    data_collector = GitHubDataCollector()
    repo_data = data_collector.get_repo_data(repo_name)
    return repo_data

@st.cache_data(ttl=3600)  # Cache for 1 hour
def calculate_repository_metrics(_repo_data):
    calculator = MetricsCalculator(repo_data)
    metrics_df = calculator.calculate_metrics()
    return metrics_df

# Initialize session state variables if they are not already
if 'repositories' not in st.session_state:
    st.session_state.repositories = []
if 'selected_repo' not in st.session_state:
    st.session_state.selected_repo = None
if 'repo_data' not in st.session_state:
    st.session_state.repo_data = None
if 'metrics_df' not in st.session_state:
    st.session_state.metrics_df = None
if 'dev_stats' not in st.session_state:
    st.session_state.dev_stats = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'previous_usernames' not in st.session_state:
    st.session_state.previous_usernames = []

# App Title with a centered header
# Redesigned App Title with modern theme
st.markdown("""
    <style>
    .title {
        font-family: 'Roboto', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        font-size: 3em;
        background: linear-gradient(135deg, #00b3ff, #1f77b4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.9);  /* Added opacity for clarity */
        letter-spacing: 0.05em;
        text-align: center;
        padding: 10px 0;
        animation: glow 1.5s infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 10px rgba(0, 179, 255, 0.8), 0 0 20px rgba(31, 119, 180, 0.8), 0 0 30px rgba(0, 179, 255, 0.8);
        }
        to {
            text-shadow: 0 0 20px rgba(0, 179, 255, 1), 0 0 30px rgba(31, 119, 180, 1), 0 0 40px rgba(0, 179, 255, 1);
        }
    }
    </style>
    <h1 class="title">GitHub Developer Performance Dashboard</h1>
""", unsafe_allow_html=True)



# Sidebar for GitHub Username Input and Repository Fetching
with st.sidebar:
    st.markdown("""
        <style>
        .sidebar-header {
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            font-size: 1.5em;
            color: #1f77b4;
            margin-bottom: 20px;
        }
        .sidebar-dropdown {
            font-family: 'Roboto', sans-serif;
            font-size: 1em;
            color: #555;
            background-color: #f0f0f0;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .sidebar-text-input {
            font-family: 'Roboto', sans-serif;
            font-size: 1em;
            color: #555;
            background-color: #f0f0f0;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .sidebar-button {
            font-family: 'Roboto', sans-serif;
            font-size: 1em;
            font-weight: 700;
            color: #fff;
            background-color: #1f77b4;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
            text-align: center;
            margin-top: 10px;
            cursor: pointer;
        }
        .sidebar-button:hover {
            background-color: #00b3ff;
        }
        .sidebar-error {
            font-family: 'Roboto', sans-serif;
            font-size: 0.9em;
            color: #ff6347;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3 class='sidebar-header'>GitHub User & Repositories</h3>", unsafe_allow_html=True)

     # Dropdown for previously entered usernames
    username = st.selectbox("Select or Enter GitHub Username", options=['vidhyavarshanyjs'] + st.session_state.previous_usernames, index=0)

    # Input field for new username
    new_username = st.text_input("Or enter a new GitHub Username", value=st.session_state.username if username == '' else '')
    # Determine which username to use: either from the dropdown or the text input
    selected_username = new_username if new_username else username

    # Button to fetch repositories and developer stats
    if st.button("Fetch Repositories and User Stats", key='fetch_button'):
        if selected_username:
            try:
                # Fetch user repositories and developer stats (cached)
                repos, dev_stats = fetch_repositories_and_stats(selected_username)

                st.session_state.repositories = repos
                st.session_state.dev_stats = dev_stats
                st.session_state.selected_repo = None
                st.session_state.repo_data = None
                st.session_state.metrics_df = None

                # Update session state and previous usernames
                st.session_state.username = selected_username
                if selected_username not in st.session_state.previous_usernames:
                    st.session_state.previous_usernames.append(selected_username)
            except ValueError as e:
                st.error(f"Error fetching repositories or user stats: {e}")
        else:
            st.error("Please enter a GitHub username.")


# Custom CSS for tabs
st.markdown("""
    <style>
    .stTabs [role="tablist"] {
        background-color: #1f77b4;  /* Updated tab background color */
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs button[role="tab"] {
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        font-size: 16px;
        color: #1f77b4;  /* Updated tab text color */
        background-color: #e0ecf8;  /* Updated tab background color */
        margin-right: 10px;
        border-radius: 10px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out;
        border: none;  /* Ensure there is no border */
    }

    .stTabs button[role="tab"]:hover {
        background-color: #e0ecf8;  /* Slightly darker background on hover */
    }

    .stTabs button[role="tab"][aria-selected="true"] {
        background-color: ; /* Highlighted tab color */
        color: white;
        box-shadow: 0px 4px 15px rgba(0, 179, 255, 0.5);
        font-size: 18px;
    }

    .stTabs button[role="tab"]:focus {
        outline: none;
    }
    </style>
""", unsafe_allow_html=True)

# Define the tab layout
tab1, tab2, tab3, tab4 = st.tabs(["👨‍💻 Developer Stats", "📊 Repository Stats", "💬 NLP Query Interface","🤔 About"])

# --- Tab 1: Developer Stats ---

with tab1:
    st.header("Developer Information")

    if st.session_state.dev_stats:
        dev_stats = st.session_state.dev_stats

        # Create a column layout for the avatar and profile info
        col1, col2 = st.columns([1, 2])

        with col1:
             # Display the avatar in a circular frame
            st.markdown(
                f"""
                <style>
                .avatar {{
                    width: 180px;
                    height: 180px;
                    border-radius: 50%;
                    object-fit: cover;
                    border: 4px solid #00b3ff;
                    margin-top:30px;
                    margin-bottom: 20px;
                    box-shadow: 0px 4px 15px rgba(0, 179, 255, 0.7);
                }}
                </style>
                <img src="{dev_stats['avatar_url']}" class="avatar"/>
                """,
                unsafe_allow_html=True
            )

        with col2:
                  # Profile Information
    
            st.markdown("""
            <style>
                .profile-info-container {
                    background-color: #e0ecf8; /* Light background color matching the theme */
                    padding: 20px; /* Padding around the content inside the container */
                    border: 2px solid #1f77b4; /* Border style and color */
                    border-radius: 10px; /* Rounded corners for the container */
                    margin: 0 auto; /* Center the content inside the column */
                    text-align: center; /* Center-align the text */
                    max-width: 600px; /* Optional: Adjust the max-width of the content */
                }
                # .{
                #     color: #1f77b4;
                #     font-family: 'Roboto', sans-serif;
                #     font-weight: 900;
                #     letter-spacing: 0.03em;
                #     margin: 0;  /* Remove default margin for h2 */
                # }
                p{
                    color: #1f77b4;
                    font-family: 'Roboto', sans-serif;
                }
            </style>
            """, unsafe_allow_html=True)

            # Displaying developer profile with the centralized layout
            st.markdown(f"""
                <div class="profile-info-container">
                    <h2 style="color: #1f77b4">{dev_stats['name']}</h2>
                    <p>{'🗒️ ' + dev_stats['bio'] if dev_stats['bio'] else ''}</p>
                    <p>{'📍 ' + dev_stats['location'] if dev_stats['location'] else ''}</p>
                    <p>{'🏢 ' + dev_stats['company'] if dev_stats['company'] else ''}</p>
                    <p>{'📧 ' + dev_stats['email'] if dev_stats['email'] else 'No email available'}</p>
                </div>
            """, unsafe_allow_html=True)

        # Dark-themed grid for developer statistics
        st.subheader("Developer Statistics")

        stats_grid = f"""
        <style>
        .stat-grid {{
            display: grid; 
            grid-template-columns: repeat(2, 1fr); 
            gap: 15px; 
            margin-top: 20px;
        }}
        .stat-item {{
            background-color: #333; 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center; 
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            color: #fff;
            font-size: 16px;
        }}
        .stat-item strong {{
            font-size: 24px;
            color: #1f77b4;
        }}
        </style>
        <div class='stat-grid'>
            <div class='stat-item'><strong>{dev_stats['public_repos']}</strong><br>Public Repositories</div>
            <div class='stat-item'><strong>{dev_stats['public_gists']}</strong><br>Public Gists</div>
            <div class='stat-item'><strong>{dev_stats['followers']}</strong><br>Followers</div>
            <div class='stat-item'><strong>{dev_stats['following']}</strong><br>Following</div>
            <div class='stat-item'><strong>{dev_stats['starred_repos']}</strong><br>Starred Repositories</div>
            <div class='stat-item'><strong>{", ".join(dev_stats['organizations']) if dev_stats['organizations'] else "None"}</strong><br>Organizations</div>
            <div class='stat-item'><strong>{dev_stats['created_at']}</strong><br>Joined GitHub</div>
        </div>
        """
        st.markdown(stats_grid, unsafe_allow_html=True)

        # Spacer before pie chart
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Display most used languages with a well-styled pie chart using Plotly
        if 'languages' in dev_stats and dev_stats['languages']:
            st.subheader("Most Used Languages")
            
            # Extract language names and corresponding byte counts
            language_names, language_bytes = zip(*dev_stats['languages'])

            # Create a DataFrame for Plotly
            data = {
                "Language": language_names,
                "Bytes": language_bytes
            }

            # Create a Plotly pie chart
            fig = px.pie(data, 
                        names="Language", 
                        values="Bytes", 
                        title="Most Used Languages",
                        color_discrete_sequence=px.colors.qualitative.Plotly)  # Changed color scheme

            # Update layout to make it look cleaner
            fig.update_traces(textinfo='percent+label', pull=[0.05] * len(language_bytes))
            fig.update_layout(showlegend=True, legend_title="Languages", title_x=0.5)

            # Display the pie chart in Streamlit
            st.plotly_chart(fig)
        else:
            st.write("No language data available.")
    else:
        st.write("Please fetch developer stats.")


# --- Tab 2: Repository Stats ---
with tab2:
    st.header("Repository Information")

    if st.session_state.repositories:
        # Dropdown to select repository
        selected_repo = st.selectbox("Select a repository", options=st.session_state.repositories)
        st.session_state.selected_repo = selected_repo

        if st.button("Fetch Metrics"):
            try:
                # Fetch repository data and metrics (cached)
                repo_data = fetch_repository_data(st.session_state.selected_repo)
                st.session_state.repo_data = repo_data

                # Calculate repository metrics (cached)
                metrics_df = calculate_repository_metrics(repo_data)
                st.session_state.metrics_df = metrics_df

                # Store the calculated metrics to a CSV file
                store_data_to_csv(st.session_state.username, st.session_state.selected_repo, metrics_df)

            except ValueError as e:
                st.error(f"Error fetching data for the selected repository: {e}")

    if st.session_state.repo_data:
        st.subheader("Repository Information Overview")
        st.write({
            "Name": st.session_state.repo_data["repo_name"],
            "URL": f"github.com/{st.session_state.selected_repo}",
            "Stars": st.session_state.repo_data["stargazers_count"],
            "Forks": st.session_state.repo_data["forks_count"],
            "Open Issues": st.session_state.repo_data["open_issues_count"],
            "Watchers": st.session_state.repo_data["watchers_count"],
            "Language": st.session_state.repo_data["language"],
            "Created At":  st.session_state.repo_data["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
            "Updated At": st.session_state.repo_data["updated_at"].strftime("%Y-%m-%d %H:%M:%S"),
            "Last Pushed At": st.session_state.repo_data["pushed_at"].strftime("%Y-%m-%d %H:%M:%S"),
            "Repository Size (KB)": st.session_state.repo_data["size"],
            "Contributors": st.session_state.repo_data["contributors_count"]
        })

    if st.session_state.metrics_df is not None:
        st.subheader("Repository Metrics Overview")
        dashboard = Dashboard(st.session_state.metrics_df)
        dashboard.display()
    else:
        st.write("Please select a repository and fetch metrics.")

# --- Tab 3: NLP Query Interface ---
# --- Tab 3: NLP Query Interface ---
with tab3:
    st.header("Natural Language Query Interface")

    st.markdown("""
    <style>
    .query-box {
        background-color: #1f1f1f;
        color: #f9f9f9;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        border: none;
        width: 100%;
    }
    .query-box:focus {
        outline: none;
        border: 2px solid #1f77b4;
    }
    .chat-bubble-user {
        background-color: #1f77b4;
        color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-bubble-bot {
        background-color: #2c2c2c;
        color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    .loading {
        font-size: 14px;
        color: #1f77b4;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.metrics_df is not None:
        st.write("Ask questions about the repository's metrics:")

        # Input box with custom styling
        query = st.text_input(
            "Enter your query", 
            key="query_input", 
            placeholder="E.g., 'How many commits?' or 'Show PR merge rate'", 
            help="Ask anything related to repository metrics or project insights"
        )

        if st.button("Ask"):
            if query:
                with st.spinner('Processing your query...'):
                    nlp_processor = NLPProcessor()
                    response = nlp_processor.process_query(query, st.session_state.metrics_df)
                    response_generator = ResponseGenerator()

                    # Display the conversation with chat bubbles
                    st.markdown(f'<div class="chat-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-bubble-user">{query}</div>', unsafe_allow_html=True)
                    bot_response = response_generator.display_response(response)
                    st.markdown(f'<div class="chat-bubble-bot">{bot_response}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Please enter a query.")
    else:
        st.write("Please fetch repository metrics before asking a question.")
# --- Tab 4: About ---
with tab4:
    st.header("About This App")

    st.markdown("""
    This application provides insightful data about GitHub developers, their repositories, and developer statistics. 

    #### Key Features:
    - **Developer Stats**: View detailed information about GitHub developers, including their public repositories, followers, and more.
    - **Repository Metrics**: Analyze repository data and metrics like stars, forks, issues, and contributions.
    - **NLP Query Interface**: Interact with repository data using natural language queries.

    #### Technologies Used:
    - **Streamlit**: A framework to create interactive web applications in Python.
    - **GitHub API**: Collects developer and repository data.
    - **Plotly**: Used for data visualization.
    - **NLP**: Provides natural language query capabilities.

    #### Future Enhancements:
    - Additional metrics and deeper analysis.
    - More interactive and customizable visualizations.
    - Broader integration with different version control platforms.
    """)
    
# This app is developed to assist developers in monitoring their open-source contributions and performance on GitHub.
