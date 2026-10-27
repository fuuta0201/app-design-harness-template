# T-001: プロジェクト制御文書を初期化する

| 項目 | 内容 |
| --- | --- |
| Status | ready |
| Phase | P0 |
| Linked specs | `G-001`, `HR-001`〜`HR-012` |
| Depends on | `T-000` |
| Owner review | required — 背景、目標、scopeの事業判断が必要 |
| Plan approval | pending |

## 目的

`{{PROJECT_NAME}}` の開発を開始できるよう、`docs/PROJECT.md` 全体を確認済み事実、仮説、未決定、要確認のいずれかで初期化する。

## Source context

- `docs/PROJECT.md` 全体
- 利用者が提供する企画、既存資産、制約、運用情報

## Scope

### In scope

- `docs/PROJECT.md` の全placeholder初期化。
- 後続task候補と依存順の作成。
- remote repositoryがある場合のmerge済みbranch自動削除設定。

### Non-goals

- application実装、dependency導入、外部サービス変更、技術候補の最終決定。

## Implementation plan

1. repositoryと既存資産をread-onlyで調査する。
2. 確認済み、仮説、未決定、要確認を分離する。
3. goal、success、scope、users、requirements、constraintsを記載する。
4. 後続のtechnology、architecture、design、delivery欄には決定を捏造せず、選定基準とownerを記載する。
5. 次のready taskを作り、`PROJECT.md` の索引へ登録する。
6. `git remote -v`、`gh auth status`、repository権限を確認し、別の外部操作承認後に `gh repo edit --delete-branch-on-merge` を実行する。実行不能なら理由と解除条件を記録する。

### Expected changes

- `docs/PROJECT.md`
- `docs/tasks/` の後続task files

### Red / Green / Refactor / Verify

- Red: project modeでplaceholder残存を検出する。
- Green: 全placeholderを根拠ある値または明示的な未決定へ置換する。
- Refactor: 重複表現を除き、詳細はtaskへ分離する。
- Verify: `python3 scripts/check_harness.py --mode project`

### Risks and recovery

- Risk: 不明事項を推測で確定する。
- Recovery / rollback: 推測を仮説へ戻し、確認方法とownerを明記する。

## Approval gate

- Plan presented: no
- Approved by: pending
- Approved at: pending
- Approval covers: pending
- Separate approval still required for: implementation、dependency導入、`gh repo edit`を含む外部操作

## Acceptance criteria

- [ ] `docs/PROJECT.md` と実行対象taskにplaceholderが残らない。
- [ ] 未確定事項が仮説／未決定／要確認として区別される。
- [ ] goalとsuccess measureがsolutionではなくoutcomeとして記載される。
- [ ] scopeとnon-goalが区別される。
- [ ] 次のready taskが索引と `docs/tasks/` の両方に存在する。
- [ ] remote、認証、権限がある場合はmerge済みbranchの自動削除が有効で、ない場合は理由と解除条件が記録される。

## Verification

| command / review | result | evidence / limitations |
| --- | --- | --- |
| `python3 scripts/check_harness.py --mode project` | not_run | project初期化後に実行 |
| `gh repo view --json nameWithOwner,deleteBranchOnMerge` | not_run | remote設定を行う場合に結果を確認 |

## Independent review

- Reviewer context: fresh / no implementation conversation
- Verdict: not_run
- Findings: pending
- Re-review: pending

## Owner review

- Required: yes
- Reason: 背景、目標、scope、成功条件は事業判断を含む。
- Result: pending

## Decisions and discoveries

- 未記録。

## Handoff

- Completed: none。
- Remaining: 全scope。
- Next action: read-only調査とplan提示。
- Do not touch: application code、dependencies、deployment。
