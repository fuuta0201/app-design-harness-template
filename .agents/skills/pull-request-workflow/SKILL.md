---
name: pull-request-workflow
description: GitHub Pull Requestを日本語で準備・検証・作成する。PRの作成、更新、本文生成を依頼されたときに使用し、概要、commitごとの実装内容、test内容、review観点を必ず含める。local Gitだけの操作やPRを伴わないcode reviewには使用しない。
---

# Pull Request作成

GitHub上の操作には `gh` を使い、PRのtitle、body、commentを日本語で作成する。実際のPR作成・更新は外部状態を変えるため、実行直前に対象repository、base／head、title、公開内容を提示し、明示承認を得る。

## 事前確認

1. `AGENTS.md`、`docs/PROJECT.md`、対象の `docs/tasks/<ID>-<slug>.md` を読む。
2. `git status --short`、`git branch --show-current`、`git remote -v` で対象と未commit変更を確認する。
3. base branchを確認し、`git log --oneline <base>..<head>` と `git diff --stat <base>...<head>` でPRへ含まれるcommitと差分を確定する。
4. taskのacceptance criteria、verification、独立review、owner review、残存riskを確認する。予定や未実行checkを成功として書かない。
5. 未commit変更、pushされていないcommit、base不明、失敗中の必須checkがあれば、PRへ含むかを明示して解消または報告する。

## 日本語PR本文

`.github/pull_request_template.md` に従い、最低限次を含める。

### 概要

- 利用者または保守者から見た結果を書く。
- 関連task／spec IDとscopeを短く示す。

### 実装内容

- PRに含まれる各commitを順番に列挙する。
- `短縮hash 日本語のcommit件名: 変更理由と主要な結果` の形で簡潔に説明する。
- commitにない変更や将来予定を混ぜない。

### テスト内容

- 実行した完全なcommandと観測結果を書く。
- 未実行、失敗、環境制約、手動確認を区別する。

### レビュー観点

- reviewerに確認してほしい仕様、境界、risk、意図的な非対象を列挙する。
- 独立reviewのverdictと残存findingがあれば記載する。

必要な場合だけ、影響範囲、rollback、関連linkを追加する。task fileの長い証拠を複製せず、参照先を示す。

## 作成手順

1. titleとbody draftを日本語で提示する。
2. repository、base、head、draft状態、実行予定commandを提示し、PR作成の明示承認を得る。
3. 承認後に `gh pr create --base <base> --head <head> --title <日本語title> --body-file <body-file>` を実行する。
4. `gh pr view --json url,title,body,baseRefName,headRefName` で公開結果を確認する。
5. PR URLと観測結果をtask fileへ記録する。本文修正やcommentにも `gh pr edit`／`gh pr comment` を使い、日本語で記載する。

既存PRを更新する場合も、差分と公開内容を提示してから `gh` を実行する。PR作成の依頼はcommit、push、merge、repository設定変更までを自動では許可しない。
