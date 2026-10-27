# Tasks

`docs/PROJECT.md` に定義された仕様とroadmapを、実装・検証できる単位へ分割して管理します。

## Ownership

- `docs/PROJECT.md`: 背景、目標、要件、設計、phase、意思決定、task索引の正本。
- `docs/tasks/<ID>-<slug>.md`: 1タスクのscope、計画、承認、受け入れ条件、検証証拠、review、handoffの正本。
- `docs/tasks/TEMPLATE.md`: 新規taskを作るときの雛形。実行対象ではありません。

タスク内容を `PROJECT.md` へ複製しません。`PROJECT.md` の索引行とtask fileのID、status、owner review区分は一致させます。

## Lifecycle

`planned → ready → in_progress → in_review → done`

- `planned`: 仕様または依存関係が未確定。
- `ready`: scope、非目標、計画、受け入れ条件、検証、必要権限が明確。
- `in_progress`: 計画がオーナー承認され、自動実装中。
- `in_review`: 実装と機械検証が完了し、独立review中または必要なowner review待ち。
- `blocked`: 理由と解除条件をtask fileへ記録する。
- `done`: 受け入れ条件、検証、独立review、必要なowner判断、正本更新が完了。

中央索引で `in_progress` にするtaskは1件だけです。並行作業は同じtask内のsubtaskとして、担当範囲と統合条件を記録します。

## Plan → Auto implementation

1. Codexはread-onlyの事前調査を行い、task fileへ実装計画を記載する。
2. scope、変更予定ファイル、検証、risk、外部操作をオーナーへ提示して停止する。
3. オーナーの明示的なOKをtask fileのApproval gateへ記録し、summaryの`Plan approval`とstatusを更新する。承認者・日時・scopeはApproval gateだけを正本とし、summaryへ複製しない。
4. 承認されたscope内は追加確認を挟まず、実装、test、修正、独立reviewまで自動で進める。
5. scope拡張、仕様判断、資格情報、破壊操作、課金、外部状態変更が必要になった場合だけ停止する。

CodexのUIでPlan modeを使える場合は `/plan` で開始します。`.codex/config.toml` はPlan modeを切り替えるものではなく、承認後のtool実行境界を設定します。

`Plan approval` は機械検証のため `pending`、`approved`、`rejected` のいずれかを使用します。`in_progress`、`in_review`、`done` は `approved` の場合だけ有効です。

`done` にする場合は、acceptance criteriaをすべてcheckし、Verificationのresultを `pass`、`passed`、`success`、`not_applicable` のいずれかにします。独立reviewのVerdictは `pass` または `pass_with_non_blocking_findings`、owner reviewのResultは区分に応じて `approved` または `not_required` とします。
