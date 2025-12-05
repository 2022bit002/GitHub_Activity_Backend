import sys
import json
import urllib.request
import urllib.error


def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        req = urllib.request.Request(url, headers={'User-Agent':'python-cli-app'})

        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"Error : Unable to fetch the data(Status code: {response.status})")
                return
            data = response.read()
            events = json.loads(data)

            if not events:
                print(f"NO recent activity found for the user : {username}")
                return
            
            print(f"Recent activity for {username}:")
            print("-"*40)

            for event in events[:10]:
                event_type = event.get('type')
                repo_name = event.get('repo',{}).get('name')
                payload = event.get('payload',{})

                action = ""

                if event_type == "PushEvent":

                    commit_count = payload.get('size',0)
                    action = f"Pushed {commit_count} commits to"

                elif event_type == "IssuesEvent":

                    issue_action = payload.get('action', 'interacted with')
                    action = f"{issue_action.capitalize()} as issue in"

                elif event_type == 'WatchEvent':

                    action = "Starred"

                elif event_type == "CreateEvent":
                    ref_type = payload.get('ref_type', 'item')
                    action = f"Created {ref_type} in"
                    
                elif event_type == "PullRequestEvent":
                    pr_action = payload.get('action', 'interacted with')
                    action = f"{pr_action.capitalize()} a PR in"

                else:
                    # Fallback for other event types
                    action = f"{event_type.replace('Event', '')} in"

                print(f"- {action} {repo_name}")


                




    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        else:
            print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}")
    except json.JSONDecodeError:
        print("Error: Failed to parse response from GitHub.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Check if username argument is provided
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
    else:
        for i in range(len(sys.argv)):
            print(f"This is the {i} argument in the argv {sys.argv[i]}")
        username = sys.argv[1]
        fetch_github_activity(username)




