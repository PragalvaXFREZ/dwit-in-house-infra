# How to hand in a lab

Every lab goes in as a pull request from your fork. These rules let all of you hand in at the same time without conflicts, and let us merge your work so it stays in the repository.

## 1. Where your files go

Put your files in your own folder. Do not add files anywhere else.

| Course | Your folder | Example |
| --- | --- | --- |
| CI labs | `learning/ci/<your-name>/` | `learning/ci/nishan/lab4/` |
| Linux labs | `learning/linux/<your-name>_lab<N>/` | `learning/linux/sulav_lab1/` |

Use your first name in lowercase, the same name every time.

For the CI labs you can keep one copy of the code and add notes for each lab (`lab1.md`, `lab2.md`, and so on), or make a subfolder per lab (`lab1/`, `lab2/`). Pick one and keep using it.

## 2. What you must not change

- The starter, for example `learning/ci/demo/`. It stays the same for the next student.
- The lab guides (`learning/ci/0*.md`, `learning/ci/README.md`).
- Another student's folder.
- Another student's workflow file.

If a guide is wrong, open a separate pull request for it, or tell your mentor.

## 3. GitHub Actions workflows

GitHub only reads workflows from `.github/workflows/` at the top of the repository. A workflow inside your own folder never runs. So this is the one file you add outside your folder:

```text
.github/workflows/<course>-<your-name>.yml      for example ci-sulav.yml
```

Never name it `ci.yml`. If everyone adds `ci.yml`, the pull requests conflict and only one can be merged.

Give the workflow your name, and make it run only when your files change. Otherwise your check runs on every other student's pull request too.

```yaml
name: CI (sulav)

on:
  push:
    paths:
      - "learning/ci/sulav/**"
      - ".github/workflows/ci-sulav.yml"
  pull_request:
    paths:
      - "learning/ci/sulav/**"
      - ".github/workflows/ci-sulav.yml"
```

## 4. What counts as evidence

- **Real output as a screenshot.** Put the screenshots in a `screenshots/` folder inside your lab folder and link them from your notes. A block of pasted text is not evidence, because an assistant can write it.
- **Your reasons, in your own words.** Do not only say that something worked or failed. Say why. A wrong reason is fine, and we learn from it. A missing reason teaches nothing.
- **Predictions written before you run something.** Commit them before the measurement, so the history shows the order.

If you would rather explain something at length, write it in your blog post and link the post from your notes.

## 5. Pull requests

1. One pull request per lab. Name it `<Course> lab <N>: <your name>`, for example `Linux lab 1: Sulav`.
2. Your mentor reviews it. If you are asked for changes, push new commits to the same branch. Do not open a new pull request.
3. Your mentor may push a small fix to your branch before merging, such as moving a file or renaming a workflow. Pull before you keep working: `git pull`.
4. When it is approved, the mentor merges it with a merge commit, so your own commits stay in the history.
5. Do not start the next lab until the current one is merged. Each lab builds on the one before it.
