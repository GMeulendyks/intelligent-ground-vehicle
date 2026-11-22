# Table of Contents

[Workflow](#workflow)<br/>
[Concepts](#concepts)<br/>
[Commands](#commands)<br/>

<br/>
<br/>

# Workflow

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

**STATUS**
```
git status
```
Displays the current status of the repository including current branch, staged changes, unstaged changes.

<br/>

**LOG**
```
git log
```
Display the commits that exist on the current branch.

<br/>

**FETCH**
```
git fetch --all --prune
```
Synchronize all local branches with remote branches.

<br/>

**PULL**
```
git pull
```
Pulls the latest code for the current branch.

<br/>

**ADD**
```
git add .
```
Stages all changes for commit. Individual files and folders can also be specified rather than "."

<br/>

**COMMIT**
```
git commit -m "COMMIT MESSAGE"
```
Commit the changes

<br/>

**PUSH**
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

**CHECKOUT:**
```
git checkout develop
```
Change the current branch to a different branch.

```
git checkout -b my-cool-branch-name
```
Create a new feature branch named "my-cool-branch-name"

<br/>
<br/>
