this file contains the commands used in github

+------------------------------------------+------------------------------------------------------------+----------------------------------------------------------+
| COMMAND                                  | FUNCTION                                                   | EXAMPLE                                                  |
+------------------------------------------+------------------------------------------------------------+----------------------------------------------------------+
| git --version                            | Checks if Git is installed and shows its version           | git --version                                            |
| git config --global user.name "Name"     | Sets your Git username                                     | git config --global user.name "Nishan"                   |
| git config --global user.email "email"   | Sets your Git email                                        | git config --global user.email "you@example.com"         |
| git init                                 | Creates a new Git repository in the current folder         | git init                                                 |
| git clone <URL>                          | Downloads a GitHub repository to your computer             | git clone <URL>                                          |
| git status                               | Shows the current status of files                          | git status                                               |
| git add <file>                           | Adds a specific file to the staging area                   | git add App.jsx                                          |
| git add .                                | Adds all changed files to the staging area                 | git add .                                                |
| git commit -m "message"                  | Saves staged changes with a message                        | git commit -m "Added navbar"                             |
| git log                                  | Shows previous commits                                     | git log                                                  |
| git log --oneline                        | Shows commits in a shorter format                          | git log --oneline                                        |
| git branch                               | Shows existing branches                                    | git branch                                               |
| git branch <name>                        | Creates a new branch                                       | git branch feature-navbar                                |
| git switch <name>                        | Switches to another branch                                 | git switch feature-navbar                                |
| git switch -c <name>                     | Creates and switches to a new branch                       | git switch -c feature-navbar                             |
| git checkout <name>                      | Older command for switching branches                       | git checkout main                                        |
| git merge <branch>                       | Combines another branch into the current branch            | git merge feature-navbar                                 |
| git remote -v                            | Shows connected remote repositories                        | git remote -v                                            |
| git remote add origin <URL>              | Connects local repository to GitHub                        | git remote add origin <URL>                              |
| git push                                 | Uploads commits to GitHub                                  | git push                                                 |
| git push -u origin main                  | Pushes main and sets upstream                              | git push -u origin main                                  |
| git pull                                 | Downloads and merges changes from GitHub                   | git pull                                                 |
| git fetch                                | Downloads remote changes without merging                   | git fetch                                                |
| git diff                                 | Shows unstaged changes                                     | git diff                                                 |
| git restore <file>                       | Discards unstaged changes in a file                        | git restore App.jsx                                      |
| git reset <file>                         | Removes a file from staging                                | git reset App.jsx                                        |
| git reset --soft HEAD~1                  | Undoes last commit and keeps changes staged                | git reset --soft HEAD~1                                  |
| git stash                                | Temporarily saves uncommitted changes                      | git stash                                                |
| git stash pop                            | Restores previously stashed changes                        | git stash pop                                            |
| git rm <file>                            | Removes a file and stages its deletion                     | git rm oldfile.txt                                       |
| git mv <old> <new>                       | Renames or moves a file                                    | git mv old.js new.js                                     |
| git tag <name>                           | Creates a tag for a specific version                       | git tag v1.0                                             |
| git show                                 | Shows details of a commit                                  | git show                                                 |
+------------------------------------------+------------------------------------------------------------+----------------------------------------------------------+
