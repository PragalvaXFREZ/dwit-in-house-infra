# 🛠️ Git & GitHub Reference Guide

A clean, comprehensive cheat sheet covering everything from daily Git basics to remote workflows and advanced power-tools.

---

## 📌 The Basics: Daily Workflow

Use these commands to manage your local workspace, track files, and save your progress.

* **`git init`**
  * Initializes a brand new local Git repository (creates the hidden `.git` folder).
* **`git status`**
  * Shows the current state of your working directory and staging area (tracked vs. untracked files).
* **`git add <filename>`**
  * Moves a specific file's changes into the staging area, preparing it to be saved.
* **`git add -p`**
  * **Interactive Staging:** Review and stage changes interactively, piece by piece (hunks).
* **`git commit`**
  * Saves your staged snapshot into history. *Always write clear, descriptive commit messages!*
* **`git diff <filename>`**
  * Shows modifications made in your working directory that haven't been staged yet.
* **`git diff <revision> <filename>`**
  * Compares the differences in a specific file between two separate historical snapshots or branches.
* **`git log`**
  * Displays a flattened, linear timeline of your project's commit history.
* **`git log --all --graph --decorate`**
  * Renders a text-based visual map of your repository history as a **Directed Acyclic Graph (DAG)**.
* **`git checkout <revision>`**
  * Updates the `HEAD` pointer to point to a specific commit or branch (updates your files to match).
* **`git help <command>`**
  * Opens the official reference manual pages for any specified Git command.

---

## 🌿 Branching & Merging

Isolate your features, experiment safely, and integrate code changes back into your main line.

* **`git branch`**
  * Lists all local branches in the current repository.
* **`git branch <name>`**
  * Creates a new branch with the specified name at your current commit position.
* **`git switch <name>`**
  * Changes your active working context to the specified branch.
* **`git checkout -b <name>`**
  * Shortcut command that creates a new branch and immediately switches to it.
* **`git merge <revision>`**
  * Integrates the history of the target branch or commit into your current active branch.
* **`git mergetool`**
  * Launches a graphical merge conflict resolution tool to resolve structural code overlaps.
* **`git rebase`**
  * Re-applies a sequence of commits from your current branch onto a completely new base commit.

---

## 📡 Remotes & GitHub Integration

Connect your local workspace to collaboration platforms like GitHub to back up and share your code.

### Connecting for the First Time
```bash
# 1. Link your local repo to GitHub
git remote add origin <repository-url>

# 2. Push and link your local main branch to the remote main branch
git push -u origin main
```

### Daily Remote Commands
* **`git remote`**
  * Lists all configured remote repository nicknames (usually `origin`).
* **`git remote add <name> <url>`**
  * Establishes a connection between your local repository and a remote server URL.
* **`git push <remote> <local-branch>:<remote-branch>`**
  * Sends your local commit objects to the remote server and updates its corresponding references.
* **`git branch --set-upstream-to=<remote>/<remote-branch>`**
  * Maps your current local branch to a specific remote branch for simple, automated pushes/pulls.
* **`git fetch`**
  * Downloads history, objects, and references from a remote repository without altering your local files.
* **`git pull`**
  * Fetches tracking updates from the remote and immediately merges them into your active branch (`git fetch` + `git merge`).
* **`git clone <url>`**
  * Downloads an entire existing repository from a remote URL down to your local computer.
* **`git clone --depth=1`**
  * **Shallow Clone:** Downloads only the single latest snapshot, skipping the entire historical timeline to save space and time.

### Forks and Pull Requests
A **fork** is your own copy of someone else's repository on GitHub. You can push to it even when you cannot push to the original.

1. Click **Fork** on the repository page. Clone the fork, not the original.
2. Make a branch, commit, and `git push -u origin <branch>` to your fork.
3. Open a **pull request** from your fork's branch to the original repository. The owner reviews and decides whether to merge.
4. To pick up later changes from the original, add it as a second remote and pull from it:

```bash
git remote add upstream <original-repository-url>
git pull upstream main
```

---

## ⏪ Undoing Changes & Time Travel

Accidents happen. Use these tools to unstage files, edit commit history, or revert problematic updates.

> ⚠️ **Warning:** Be cautious when using commands that rewrite or discard history if your commits have already been pushed to a shared remote repository.

* **`git commit --amend`**
  * Modifies your absolute last commit (add forgotten files or fix a typo in the commit message).
* **`git reset <file>`**
  * Removes a file from the staging area while leaving its physical modifications completely untouched in your working directory.
* **`git restore <file>`**
  * Completely discards local uncommitted changes inside your working directory, resetting the file back to its last saved state.
* **`git revert <revision>`**
  * Creates a brand new commit that explicitly reverses the exact changes introduced by a previous commit, maintaining a clean history.

---

## 🚀 Advanced Git Power-Tools

Deep-dive commands for debugging, performance tracking, and complex multi-workspace environments.

* **`git blame <file>`**
  * Annotates every line of a file to display the commit author and timestamp of the last modification.
* **`git stash`**
  * Temporarily saves modified, tracked files onto a hidden internal stack so you can switch contexts with a completely clean workspace.
* **`git bisect`**
  * Uses binary search across your history to track down exactly which commit introduced a bug or regression.
* **`git worktree`**
  * Allows you to check out multiple branches of the same repository simultaneously into completely separate folders.
* **`git rebase -i`**
  * Opens an interactive session to squash, reword, reorder, or drop past commits in your local timeline.

---

## ⚙️ Configuration & Project Control

* **`git config`**
  * Used to fully customize your Git environment (e.g., global usernames, emails, aliases, and color themes).
* **`.gitignore`**
  * A configuration text file placed in the root of your project specifying exact patterns of files (like `.DS_Store`, `node_modules/`, or system logs) that Git should permanently ignore.
