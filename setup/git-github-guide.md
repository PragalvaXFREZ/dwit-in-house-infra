# Git & GitHub Guide

**Author:** Sulav Singh

---

## 1. Git Basics

### What is Git?

Git is a **version control system** used to track changes in files and manage different versions of a project.

### What is GitHub?

GitHub is a platform that hosts Git repositories online and allows developers to collaborate on projects.

---

## 2. Fork a Repository

A **fork** creates a copy of another GitHub repository under your own GitHub account.

It allows you to work on the project without directly modifying the original repository.

---

## 3. Clone a Repository

Cloning downloads a repository from GitHub to your local computer.

```bash
git clone <repository-url>
```

Move into the repository:

```bash
cd repository-name
```

---

## 4. Git Remotes

Check the remote repositories connected to your local repository:

```bash
git remote -v
```

Usually:

* **origin** → your fork
* **upstream** → the original repository

Add the original repository as upstream:

```bash
git remote add upstream <original-repository-url>
```

---

## 5. Check Repository Status

```bash
git status
```

This shows:

* Current branch
* Modified files
* Untracked files
* Staged files
* Other changes that need attention

---

## 6. Branches

A branch is a separate line of development used to work on a feature or change without directly affecting another branch.

### View branches

```bash
git branch
```

### Create and switch to a new branch

```bash
git switch -c branch-name
```

### Switch to an existing branch

```bash
git switch branch-name
```

---

## 7. View Changes

### View unstaged changes

```bash
git diff
```

### View staged changes

```bash
git diff --staged
```

---

## 8. Stage Changes

Add a specific file:

```bash
git add filename
```

Add all changed files:

```bash
git add .
```

`git add` moves changes to the **staging area** so they can be included in the next commit.

---

## 9. Commit Changes

Create a commit:

```bash
git commit -m "commit message"
```

Example:

```bash
git commit -m "added git github guide"
```

### Commit with sign-off

```bash
git commit -s -m "added git github guide"
```

The `-s` option adds a **Signed-off-by** line to the commit.

---

## 10. Push Changes

Push your branch to your fork:

```bash
git push origin branch-name
```

Example:

```bash
git push origin git-guide
```

The first time you push a new branch, you can also use:

```bash
git push -u origin branch-name
```

The `-u` option sets the upstream tracking branch.

---

## 11. Pull Changes

Pull changes from a remote repository:

```bash
git pull origin main
```

`git pull` downloads changes and then merges them into the current branch.

---

## 12. Fetch Changes

Fetch changes from the original repository:

```bash
git fetch upstream
```

`git fetch` downloads information about changes but **does not automatically merge them** into your current branch.

---

## 13. Merge Changes

For example, to merge the latest upstream main branch into your current branch:

```bash
git merge upstream/main
```

If there are conflicting changes, Git may report a **merge conflict**.

---

## 14. Keep Your Branch Updated

A common workflow is:

```bash
git fetch upstream
git merge upstream/main
```

This gets the latest changes from the original repository and merges them into your current branch.

---

## 15. Pull Request

A **Pull Request (PR)** is a request to merge changes from one branch into another repository or branch.

For example:

```text
Your fork
    |
    └── git-guide
            |
            ↓
      Pull Request
            |
            ↓
Original repository
    |
    └── main
```

A typical workflow is:

```text
Your fork / git-guide
        ↓
Pull Request
        ↓
Original repository / main
```

A PR allows maintainers to review your changes before merging them.

---

## 16. Merge Conflicts

A merge conflict happens when Git cannot automatically decide which changes to keep.

Git may show something like:

```text
<<<<<<< HEAD
Your changes
=======
Changes from another branch
>>>>>>> main
```

To resolve the conflict:

1. Open the file.
2. Decide which changes should remain.
3. Remove the conflict markers.
4. Save the file.
5. Stage the resolved file.

```bash
git add filename
```

Then commit:

```bash
git commit -m "resolve merge conflict"
```

Finally, push the changes:

```bash
git push origin branch-name
```

---

## 17. Complete GitHub Workflow

A typical workflow when contributing to a repository is:

```text
Fork
  ↓
Clone
  ↓
Create Branch
  ↓
Make Changes
  ↓
git status
  ↓
git add
  ↓
git commit
  ↓
git push
  ↓
Create Pull Request
  ↓
Review
  ↓
Resolve Conflicts if necessary
  ↓
Push Again
  ↓
Merge
```

---

## 18. Difference Between Add, Commit, Push and Pull Request

### `git add`

Stages your changes.

```bash
git add .
```

### `git commit`

Records the staged changes in your local Git repository.

```bash
git commit -m "message"
```

### `git push`

Uploads your local commits to a remote repository.

```bash
git push origin branch-name
```

### Pull Request

Requests that your changes be reviewed and merged into another branch or repository.

---

## 19. Useful Git Commands

### View commit history

```bash
git log --oneline
```

### View all branches

```bash
git branch -a
```

### View remote branches

```bash
git branch -r
```

### Check connected remote repositories

```bash
git remote -v
```

### Unstage a file

```bash
git restore --staged filename
```

### Discard unstaged changes

```bash
git restore filename
```

Be careful with this command because it can remove your uncommitted changes.

---

## 20. Important Terms

### Repository

A project managed using Git.

### Fork

A copy of another GitHub repository under your own GitHub account.

It allows you to work on the project without directly modifying the original repository.

### Clone

A local copy of a remote Git repository on your computer.

### Branch

A separate line of development inside a Git repository.

### Commit

A saved checkpoint containing changes made to the repository.

### Remote

A reference to a repository hosted somewhere else, usually on GitHub.

### Origin

The remote repository that your local repository was originally cloned from.

When working with a fork, `origin` usually refers to your fork.

### Upstream

The remote repository containing the original project.

### Pull Request

A request to merge changes from one branch into another branch.

### Merge Conflict

A situation where Git cannot automatically combine changes from different branches.

---

