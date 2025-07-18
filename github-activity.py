import requests
import argparse
import sys

# Return argument after parsing
def parse_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    parser.add_argument("user", type=str, 
                        help="Get the github user activity of given user")
    
    return parser.parse_args()


def fetch_user_information(user: str) -> list:

    # Get user information
    response = requests.get(f"https://api.github.com/users/{user}/events")
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    elif response.status_code == 404:
        print("Invalid user.")
        sys.exit()
    else:
        print(f"Error code: {response.status_code}")
        sys.exit()


def display_user_data(user_data) -> None:

    for item in user_data:
        event_type = item.get("type")
        repo = item.get("repo", {}).get("name", "unknown repo")
        payload = item.get("payload", {})

        match event_type:
            case "PushEvent":
                commit_count = payload.get("size", 0)
                print(f"- Pushed {commit_count} commit{'s' if commit_count != 1 else ''} to {repo}")

            case "PullRequestEvent":
                action = payload.get("action")
                if action == "opened":
                    print(f"- Opened a new pull request in {repo}")
                elif action == "closed":
                    merged = payload.get("pull_request", {}).get("merged", False)
                    if merged:
                        print(f"- Merged a pull request in {repo}")
                    else:
                        print(f"- Closed a pull request in {repo}")

            case "IssuesEvent":
                action = payload.get("action")
                if action == "opened":
                    print(f"- Opened a new issue in {repo}")
                elif action == "closed":
                    print(f"- Closed an issue in {repo}")

            case "IssueCommentEvent":
                print(f"- Commented on an issue in {repo}")

            case "WatchEvent":
                print(f"- Starred {repo}")

            case "ForkEvent":
                forkee = payload.get("forkee", {}).get("full_name", "unknown/fork")
                print(f"- Forked {repo} to {forkee}")

            case "CreateEvent":
                ref_type = payload.get("ref_type")
                ref = payload.get("ref")
                if ref_type == "repository":
                    print(f"- Created new repository {repo}")
                else:
                    print(f"- Created new {ref_type} '{ref}' in {repo}")

            case "DeleteEvent":
                ref_type = payload.get("ref_type")
                ref = payload.get("ref")
                print(f"- Deleted {ref_type} '{ref}' from {repo}")

            case "ReleaseEvent":
                tag = payload.get("release", {}).get("tag_name", "")
                print(f"- Published release {tag} in {repo}")

            case "PublicEvent":
                print(f"- Made {repo} public")


def main():
    
    args = parse_arguments()

    if args.user:
        user_data = fetch_user_information(user=args.user)
        display_user_data(user_data)

if __name__ == "__main__":
    main()