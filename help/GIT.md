# Table of Contents

[General Workflow](#general-workflow)<br/>
[Concepts](#concepts)<br/>
[Commands](#commands)<br/>

<br/>
<br/>

# General Workflow

The typical workflow is:
1. Open the terminal and enter the folder that is a git repository.
1. Synchronize the local develop branch with the remote develop branch.
    1. `git fetch --all --prune`
    1. `git checkout develop`
    1. `git pull`
1. Create a new branch to start making changes.
    1. `git checkout -b my-cool-branch-name`
1. Make code changes
1. Stage the changes
    1. `git add .`
1. Commit the changes
    1. `git commit -m "My cool commit message"`
1. Rebase changes on the latest remote develop branch
    1. `git fetch --all --prune`
    1. `git rebase -i origin/develop`
        1. `git rebase --abort` Undo anything that was done during a rebase.
    1. Resolve all merge conflicts.
1. Push your changes
    1. `git push`
1. Create a pull request on github to merge my-cool-branch-name into develop.
1. Get the pull request reviewed by others.
1. Merge the pull request
1. Update the local branches
    1. `git fetch --all --prune`
    1. `git checkout develop`
    1. `git pull`

<br/>
<br/>

# Concepts

| Concept       | Description                                                |
|---------------|------------------------------------------------------------|
| Commit        | A change made to code.                                     |
| Branch        | An isolated place to work on code.                         |
| Remote Branch | A branch on GitHub.                                        |
| Local Branch  | A branch on the current machine.                           |
| Rebase        | Apply commits on the current branch to a different branch. |

<br/>
<br/>

# Commands

**ADD:**
```
git add .
```
Stages all changes for commit. Individual files and folders can also be specified rather than "."

<br/>

**APPLY:**
```
git apply ~/Downloads/patch.diff
```
Apply the changes stored in `~/Downloads/patch.diff` to this git repository.

<br/>

**BRANCH:**:

```
git branch -a
```
List all existing remote branches and local branches.

```
git branch -D branch-name
```
Delete the branch named `branch-name`.

<br/>

**CHECKOUT:**
```
git checkout branch-name
```
Change the current branch to a different branch.

```
git checkout -b my-cool-branch-name
```
Create a new feature branch named "my-cool-branch-name"

<br/>

**COMMIT:**
```
git commit -m "COMMIT MESSAGE"
```
Commit the changes

<br/>

**DIFF:**
```
git diff > ~/Downloads/patch.diff"
```
Store unstaged changes into a file in `~/Downloads/patch.diff`

<br/>

**FETCH:**
```
git fetch --all --prune
```
Synchronize all local branches with remote branches.

<br/>

**LOG:**
```
git log
```
Display the commits that exist on the current branch.

<br/>

**PULL:**
```
git pull
```
Pulls the latest code for the current branch.

<br/>

**PUSH:**
```
git push
```
Update the branch on github with the changes that have been committed locally.

<br/>

**REBASE:**
```
git rebase -i origin/develop
```
Rebase the remote develop branch.
- `d` to drop a commit.
- `r` to rename a commit message.
- `f` to fixup a commit (combine it with the commit above).

```
git rebase --abort
```
Undo the current rebase and put the current branch back into a stable state.

<br/>

**RESTORE:**
```
git restore ./*
```
Undo all unstaged changes.

<br/>

**RESET:**
```
git reset --hard origin/branch-name*
```
Completely reset the branch to the remote branch `branch-name`.

<br/>

**STASH:**
```
git stash
```
Store unstaged changes at the top of git's stack.

```
git stash list
```
Show what's on git's stack.

```
git stash pop
```
Apply the changes stored in the top of git's stack.

```
git stash drop 1
```
Remove the changes stored at the 1st index of git's stack.

<br/>

**STATUS:**
```
git status
```
Displays the current status of the repository including current branch, staged changes, unstaged changes.

<br/>
<br/>
