# Git Instructions and What They Mean

Git is a version control system. It tracks changes to your files, lets you
go back to older versions, and lets many people work on the same project
without overwriting each other.

## Common Git Commands

| Command | What it means |
|---|---|
| `git init` | Turns the current folder into a new Git repository. |
| `git clone <url>` | Downloads a copy of a remote repository to your computer. |
| `git status` | Shows which files are changed, new, or staged. |
| `git add <file>` | Moves changes to the staging area (prepares them for a commit). |
| `git add .` | Stages all changed files in the current folder. |
| `git commit -m "message"` | Saves the staged changes as a snapshot with a message. |
| `git log` | Shows the history of commits. |
| `git branch` | Lists branches, or creates one if you give a name. |
| `git checkout -b <name>` | Creates a new branch and switches to it. |
| `git pull` | Fetches the latest changes from the remote and merges them. |
| `git push` | Uploads your local commits to the remote repository (GitHub). |
| `git merge <branch>` | Combines another branch into your current one. |
| `git diff` | Shows the exact line-by-line changes you made. |

## Basic Workflow

1. Edit your files.
2. `git add .` to stage the changes.
3. `git commit -m "describe what you did"` to save them locally.
4. `git push` to send them to GitHub.

## Key Terms

- **Repository (repo):** A project folder tracked by Git.
- **Commit:** A saved snapshot of your project at a point in time.
- **Branch:** A separate line of work, so you can experiment safely.
- **Remote:** The online copy of the repo (for example, on GitHub).
- **Origin:** The default name for the remote you cloned from.
- **Staging area:** A waiting area where changes sit before being committed.
- **Pull request (PR):** A request to merge your branch into another branch.

## Setup and Terminal Commands

| Command | What it means |
|---|---|
| `mkdir project` | Makes a new folder named project. |
| `ls` | Lists the files and folders in the current directory. |
| `cd project` | Moves you into the project folder. |
| `git remote -v` | Shows the remote repositories linked to your project, with their fetch and push URLs. |
| `git remote setup stream` | Not a valid Git command. You probably mean `git remote add upstream <url>`, which links the original repo you forked from under the name upstream. |
| `git --version` | Shows which version of Git is installed. It's also a quick way to check that Git is installed. |
| `git config --global user.name "Your name"` | Sets the name attached to all your commits on this computer. |
| `git config --global user.email "Your email"` | Sets the email attached to all your commits. Use the same email as your GitHub account. |
| `git commit -m "Initial commit"` | Saves your staged changes as a snapshot, with the message "Initial commit". This is usually the first commit in a new repo. |
| `git branch -M main` | Renames (and force-renames if needed) your current branch to main. |
| `git remote add origin <GitHub Repository-URL>` | Links your local project to a GitHub repo and names that link origin. |
| `git remote add v` | Incomplete. `git remote add` needs a name and a URL, like `git remote add v <url>`. It is probably a typo, so you can leave it out. |
| `git pull origin` | Downloads the latest changes from origin and merges them into your current branch. It is usually written as `git pull origin main`. |
| `git push -u origin "Your Name"` | Pushes a branch to origin and sets it as the default upstream for future git push and git pull. Branch names can't contain spaces, so replace "Your Name" with a branch name like main or add-kohinoor-doc. |
| `git add` | Stages changes so they are included in the next commit. It needs a target, such as `git add file.md` or `git add .` for everything. |
| `git commit -s -m "Your name"` | Commits with a Signed-off-by: Name <email> line added to the message. The -s means you certify you have the right to submit the work. The -m text should describe the change, for example "Add Kohinoor.md", not just your name. |
