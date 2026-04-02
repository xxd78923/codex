#!/bin/bash
set -euo pipefail

GITHUB_TOKEN="${1:?Usage: publish.sh <github_token> <repo_name>}"
REPO_NAME="${2:?Usage: publish.sh <github_token> <repo_name>}"

cd /home/client_2447_7/autoppia/codex_agent

# Create .gitignore
cat > .gitignore <<'GITIGNORE'
__pycache__/
*.pyc
.claude/
.env
*.log
GITIGNORE

# Init git repo if needed
if [ ! -d .git ]; then
    git init
    git branch -M main
fi

# Create GitHub repo (ignore error if exists)
curl -s -X POST "https://api.github.com/user/repos" \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    -d "{\"name\": \"${REPO_NAME}\", \"private\": true}" > /dev/null 2>&1 || true

# Get GitHub username
GH_USER=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")

REMOTE_URL="https://${GITHUB_TOKEN}@github.com/${GH_USER}/${REPO_NAME}.git"

# Set remote
git remote remove origin 2>/dev/null || true
git remote add origin "${REMOTE_URL}"

# Commit and push
git add -A
git commit -m "Deploy SN36 agent" || echo "Nothing new to commit"
git push -u origin main --force

# Get commit SHA
COMMIT_SHA=$(git rev-parse HEAD)
echo ""
echo "=== DEPLOYMENT INFO ==="
echo "GITHUB_URL=https://github.com/${GH_USER}/${REPO_NAME}/tree/${COMMIT_SHA}"
echo ""
echo "Use this as your GITHUB_URL environment variable for the miner."
