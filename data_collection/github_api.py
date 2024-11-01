import os
from github import Github
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class GitHubDataCollector:
    def __init__(self):
        # Load the GitHub access token from the .env file
        access_token = os.getenv("GITHUB_TOKEN")
        if not access_token:
            raise ValueError("GitHub access token is not set in the .env file.")
        self.g = Github(access_token)

    def get_user_repositories(self, username):
        """Fetches all repositories for a given GitHub user."""
        try:
            user = self.g.get_user(username)
            repos = [repo.full_name for repo in user.get_repos()]
            return repos
        except Exception as e:
            raise ValueError(f"Failed to fetch user repositories: {e}")

    def get_user_languages(self, username):
        """Fetches and aggregates the most used languages for a given GitHub user."""
        try:
            user = self.g.get_user(username)
            repos = user.get_repos()
            language_data = {}

            # Aggregate languages across all repositories
            for repo in repos:
                languages = repo.get_languages()
                for lang, bytes_used in languages.items():
                    if lang in language_data:
                        language_data[lang] += bytes_used
                    else:
                        language_data[lang] = bytes_used

            # Sort the languages by usage
            sorted_languages = sorted(language_data.items(), key=lambda x: x[1], reverse=True)
            return sorted_languages
        except Exception as e:
            raise ValueError(f"Failed to fetch user languages: {e}")

    def get_user_info(self, username):
        """Fetches detailed information for a given GitHub username, including languages."""
        try:
            user = self.g.get_user(username)
            contributions = self.get_contributions(user)
            starred_repos_count = user.get_starred().totalCount
            organizations = [org.login for org in user.get_orgs()]
            languages = self.get_user_languages(username)

            user_info = {
                "avatar_url": user.avatar_url,
                "name": user.name,
                "bio": user.bio,
                "company": user.company,
                "location": user.location,
                "email": user.email,
                "public_repos": user.public_repos,
                "public_gists": user.public_gists,
                "followers": user.followers,
                "following": user.following,
                "starred_repos": starred_repos_count,
                "contributions": contributions,
                "organizations": organizations,
                "created_at": user.created_at.strftime("%Y-%m-%d"),
                "languages": languages,  # Add languages here
            }
            return user_info
        except Exception as e:
            raise ValueError(f"Failed to fetch user information: {e}")
    
    def get_contributions(self, user):
        """Fetches the number of contributions in the past year (assuming it can be retrieved)."""
        try:
            # GitHub API doesn't directly provide contribution data, this would typically require scraping.
            # We use a workaround here by summing up PRs, commits, and issues.
            commits_count = sum(1 for _ in user.get_events() if _.type == "PushEvent")
            issues_count = user.get_issues().totalCount
            pull_requests_count = sum(1 for _ in user.get_events() if _.type == "PullRequestEvent")
            
            total_contributions = commits_count + issues_count + pull_requests_count
            return total_contributions
        except Exception:
            return "Unavailable"

    def get_repo_data(self, repo_url):
        """Collects data for a single repository including commits, PRs, issues, reviews, and additional metadata."""
        repo_name = self.extract_repo_name(repo_url)
        if not repo_name:
            raise ValueError("Invalid GitHub repository URL. Please provide a valid URL.")

        try:
            repo = self.g.get_repo(repo_name)
        except Exception as e:
            raise ValueError(f"Failed to fetch repository data: {e}")

        repo_data = {
            "repo_name": repo.full_name,
            "stargazers_count": repo.stargazers_count,
            "forks_count": repo.forks_count,
            "open_issues_count": repo.open_issues_count,
            "watchers_count": repo.subscribers_count,
            "language": repo.language,
            "created_at": repo.created_at,
            "updated_at": repo.updated_at,
            "pushed_at": repo.pushed_at,
            "size": repo.size,
            "contributors_count": repo.get_contributors().totalCount,
            "labels": [label.name for label in repo.get_labels()],
            "topics": repo.get_topics(),
            "commits": list(repo.get_commits()),  # Convert to list
            "pull_requests": list(repo.get_pulls(state='all')),  # Convert to list
            "issues": list(repo.get_issues(state='all')),  # Convert to list
            "reviews": [review for pr in repo.get_pulls(state='all') for review in pr.get_reviews()]
        }
        return repo_data

    def extract_repo_name(self, repo_url):
        """Extracts the owner/repository from a GitHub URL."""
        try:
            parsed_url = urlparse(repo_url)
            path_parts = parsed_url.path.strip('/').split('/')
            if len(path_parts) == 2:
                # Expecting format like /owner/repository
                owner, repo = path_parts
                return f"{owner}/{repo}"
            else:
                return None
        except Exception:
            return None
