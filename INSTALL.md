# Install the live GitHub profile updater

1. Copy `scripts/update_profile.py`, `.github/workflows/refresh-profile.yml`, and `ROADMAP.md` into the root of `SudhaMondal/SudhaMondal`.
2. In your existing `README.md`, replace the four sections **Featured Projects**, **GitHub Stats**, **Recent GitHub Activity**, and **Roadmap** with the matching block in `README_DYNAMIC_SECTIONS.md`.
3. In the repository, open **Settings → Actions → General → Workflow permissions** and allow read and write permissions. The workflow also declares `contents: write`.
4. Open **Actions → Refresh GitHub Profile → Run workflow** once to test it.

The workflow refreshes every six hours and when the updater, roadmap, or README is changed. Featured projects are the six most recently pushed public repositories you own, excluding forks, archived repositories, and this profile repository. Recent activity is drawn from GitHub's public events feed (GitHub may only expose a limited recent history).

The stats and streak images are remote live cards; their displayed values are controlled by those services and may be cached. Private contribution counts are not included in this setup.

**Roadmap:** edit `ROADMAP.md` when your goals or progress change; the README will sync it on the next workflow run.
