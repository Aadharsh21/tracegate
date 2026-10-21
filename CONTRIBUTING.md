# Contributing to tracegate

These are the working rules for this repository. They follow the **GitHub Flow** branching model:
`main` is always releasable, and every change reaches it through a pull request.

## Branches

| Branch | Purpose | Lifetime |
| --- | --- | --- |
| `main` | Always passes CI. No direct pushes once CI exists. | Long-running |
| `feature/<short-name>` | One feature or fix, tied to one issue | Deleted after merge |
| `ci/<short-name>` | Changes to the GitHub Actions workflows | Deleted after merge |
| `docs/<short-name>` | Documentation only | Deleted after merge |

1. Open (or pick) an issue that describes the change.
2. Branch from an up-to-date `main`:
   `git switch main && git pull && git switch -c feature/<short-name>`
3. Keep the branch short-lived. If `main` moves ahead, rebase your branch onto it
   (`git fetch origin && git rebase origin/main`) and push with `git push --force-with-lease`.
   Never rebase `main` or a branch that someone else has built on.
4. Open a pull request that says `Closes #<issue>` and fill in the template.
5. Merge only when CI is green, using a merge commit so the feature's history stays visible.

## Commits

A good commit contains one logical change and explains why it was made.

- Stage only what belongs together. Use `git add -p` to split unrelated edits in the same file.
- Subject line: imperative mood, 50 characters or less, no trailing period
  (`Add JSON report format`, not `added json stuff.`).
- Leave one blank line, then write a body wrapped at 72 characters that explains *why*.
- Clean up work-in-progress commits before opening a pull request:
  `git commit --fixup <sha>` and then `git rebase -i --autosquash main`.
