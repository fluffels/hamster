GIT Workflow
============

There are two main branches: master and develop.
Each has a specific function: master stores the last release (including any hotfixes), and develop stores the most recent development work.
The only times you may commit to master is if you are releasing a new version of the project, or if you are releasing a hotfix.
The only time you may commit to develop is if you are *completing* a feature, or *resolving* an issue.

At various times there will also be temporary topic branches.
These are for implementing a feature, or fixing an issue.
They will be deleted, so they may have dirty commit histories.

The workflow also has two directions: upstream and downstream.

Upstream looks like this:
```
feature > develop > master
hotfix > master
```
It is used for getting new features into a release.
You must exclusively use ```git merge --squash --no-commit downstream-branch-name``` for this direction.

Downstream looks like this:
```
master > develop > feature
```
It is used for getting hotfixes and global changes into develop and the various feature branches, respectively.
You must use git rebase for this direction, except if this would require merging a change more than once or twice.
In that case, you may use git merge, since this will likely only happen to topic branches, and they will be deleted in any case.

Topic Branches
--------------
This is for downstream development, then merging upstream.
Replace branch names as necessary with correct downstream and upstream.

```
#!bash
# Clone repo.
git clone git@bitbucket.org:fluffels/hamster.git 

# Create feature branch.
git checkout -b my_new_feature

# Work and commit some stuff.
git commit

# Rebase to pull in changes. *Don't* merge.
git rebase develop

# Switch back to develop branch.
git checkout develop

# Now merge.
# Take note of --squash, it makes sure we don't have a lot of commits per feature.
git merge --squash --no-commit my_new_feature

# Get rid of the branch, it's not needed anymore.
# But make sure you merged everything! Once it's gone, it's gone forever.
git branch -D my_new_feature
```

Where to store branches?
------------------------

Some people say you only want to put feature branches on your local machine, i.e. they should be invisible to other contributors.
I say that's silly because it's a nice backup to have.
Therefore, make sure feature branches are tracking branches and not local ones.

This leads to a problem when you rebase a topic branch: git will ask you to merge the origin version.
In that case it's totally fine to ```git push -f```, overwriting the remote's commit history.
These are topic branches and will be deleted, so it doesn't matter if we do bad things to their commits.

Summary Pic
-----------

![Git Branching Model](http://nvie.com/img/2009/12/Screen-shot-2009-12-24-at-11.32.03.png)

References
----------

* [Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/).
* [Merge vs. Rebase](http://stackoverflow.com/questions/457927/git-workflow-and-rebase-vs-merge-questions).
* [Rebase Workflow](http://www.randyfay.com/node/91).
* [Avoiding Git Disasters](http://randyfay.com/node/89)

