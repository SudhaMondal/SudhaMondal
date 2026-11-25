#!/usr/bin/env python3
"""Refresh the profile README's projects, activity, and roadmap from live GitHub data."""
import os
import re
import requests

OWNER = "SudhaMondal"
PROFILE_REPO = "SudhaMondal"
README = "README.md"

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if os.getenv("GITHUB_TOKEN"):
    headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

def api(path):
    response = requests.get(
        f"https://api.github.com{path}", headers=headers, timeout=30
    )
    response.raise_for_status()
    return response.json()

def replace_section(readme, name, content):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(readme):
        raise RuntimeError(f"README is missing markers for {name}")
    replacement = f"{start}\n{content.strip()}\n{end}"
    return pattern.sub(lambda _: replacement, readme, count=1)

def projects():
    repos = api(f"/users/{OWNER}/repos?type=owner&sort=updated&per_page=100")
    repos = [
        r for r in repos
        if not r.get("fork") and not r.get("archived")
        and r["name"].lower() != PROFILE_REPO.lower()
    ]
    repos.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    lines = []
    for repo in repos[:6]:
        description = (repo.get("description") or "A project by Sudha Mondal")
        description = description.replace("|", r"\|").replace("\n", " ")
        language = repo.get("language") or "Not specified"
        updated = (repo.get("pushed_at") or "")[:10] or "date unavailable"
        lines.append(
            f"- **[{repo['name']}]({repo['html_url']})** — {description}  \n"
            f"  `{language}` · Last pushed: {updated}"
        )
    return "\n".join(lines) or "_New public projects will appear here automatically._"

def recent_activity():
    events = api(f"/users/{OWNER}/events/public?per_page=100")
    lines = []
    for event in events:
        kind, payload = event.get("type"), event.get("payload", {})
        repo = event.get("repo", {}).get("name")
        if kind == "PushEvent":
            count = len(payload.get("commits", []))
            branch = (payload.get("ref") or "").replace("refs/heads/", "")
            action = f"Pushed {count} commit(s) to `{branch}`"
        elif kind == "CreateEvent":
            action = f"Created {payload.get('ref_type', 'resource')} `{payload.get('ref') or ''}`"
        elif kind == "ReleaseEvent":
            release = payload.get("release", {}).get("name") or "a release"
            action = f"Published **{release}**"
        elif kind == "PullRequestEvent":
            action = f"{payload.get('action', 'Updated').capitalize()} pull request #{payload.get('number', '')}"
        elif kind == "IssuesEvent":
            number = payload.get("issue", {}).get("number", "")
            action = f"{payload.get('action', 'Updated').capitalize()} issue #{number}"
        elif kind == "WatchEvent":
            action = "Starred this repository"
        elif kind == "ForkEvent":
            action = "Forked this repository"
        else:
            continue
        if repo:
            date = (event.get("created_at") or "")[:10]
            lines.append(f"- {action} in [{repo}](https://github.com/{repo}) · {date}")
        if len(lines) >= 8:
            break
    return "\n".join(lines) or "_No recent public activity to display yet._"

def main():
    with open(README, encoding="utf-8") as file:
        readme = file.read()
    with open("ROADMAP.md", encoding="utf-8") as file:
        roadmap = file.read().strip()
    readme = replace_section(readme, "AUTO_PROJECTS", projects())
    readme = replace_section(readme, "AUTO_ACTIVITY", recent_activity())
    readme = replace_section(readme, "AUTO_ROADMAP", roadmap)
    with open(README, "w", encoding="utf-8") as file:
        file.write(readme)

if __name__ == "__main__":
    main()
