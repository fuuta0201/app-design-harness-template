# T-000: 再利用可能な開発ハーネス基盤を定義する

| 項目 | 内容 |
| --- | --- |
| Status | done |
| Phase | P0 |
| Linked specs | `HR-001`〜`HR-008` |
| Depends on | - |
| Template role | maintenance |
| Owner review | required — 今後の標準workflowを決めるため |
| Plan approval | approved |

## 目的

参照プロジェクトで実証した流れを、技術スタック非依存かつ仕様駆動のテンプレートへ抽象化する。

## Source context

- `docs/PROJECT.md`: `HR-001`〜`HR-008`
- 参照thread: ユーザーが指定したサイトリニューアルtask

## Scope

### In scope

- `AGENTS.md`、`docs/PROJECT.md`、`docs/tasks/`、repo-local Skills、`.codex/`、validator、PR template。

### Non-goals

- application scaffold、framework／hosting選定、dependencies、CI、外部サービス、公開。

## Implementation plan

1. 参照プロジェクトの工程とreview gateを抽象化する。
2. project正本とtask詳細を分離する。
3. Plan承認後の自動実装境界をCodex設定と規約へ反映する。
4. validator、回帰test、独立reviewで整合性を確認する。

### Expected changes

- repository harness files only

### Red / Green / Refactor / Verify

- Red: 構造欠落、未登録資料、task不整合を再現するvalidator test。
- Green: 必須構造とtask整合性を検査する最小実装。
- Refactor: stack固有の前提と重複contextを除去する。
- Verify: unit test、template validation、Skill validation、独立review。

### Risks and recovery

- Risk: 規約が重くなり、通常開発の速度を落とす。
- Recovery / rollback: Git差分から個別規約を縮小し、実証されたgateだけを残す。

## Approval gate

- Plan presented: yes
- Approved by: project owner
- Approved at: 2026-10-25 / revised 2026-10-26
- Approval covers: repository-local harness artifactsの作成と今回指定の再構成
- Separate approval still required for: commit、push、外部公開

## Acceptance criteria

- [x] `docs/PROJECT.md` がproject contextとspecの正本として維持される。
- [x] task詳細が `docs/tasks/` へ分離される。
- [x] Skillが日本語で保守できる。
- [x] Plan承認後の自動実装と停止条件が定義される。
- [x] `.codex` の共通設定とrulesが提供される。
- [x] 修正後の機械検証がpassする。
- [x] 独立reviewがpassする。
- [x] owner reviewが完了する。

## Verification

| command / review | result | evidence / limitations |
| --- | --- | --- |
| `python3 -m unittest scripts/test_check_harness.py` | pass | 23 tests |
| `python3 scripts/check_harness.py --mode template` | pass | task index／file整合を含む |
| `python3 -m py_compile scripts/check_harness.py scripts/test_check_harness.py` | pass | syntax compile |
| `python3 /Users/satofuta/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/app-development-harness` | pass | Skill structure |
| `python3 /Users/satofuta/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/independent-change-review` | pass | Skill structure |
| `git diff --check` | pass | tracked差分。未追跡の必須artifactはharness validatorで末尾空白を検査 |
| `codex execpolicy check --rules .codex/rules/project.rules -- <command>` | pass | Codex CLI 0.164.0。下記8 commandはすべて`prompt` |
| independent review | pass | 会話文脈なしのagentが全差分と23 testsを再確認 |

Execpolicy command matrix:

- `git -C . push`
- `gh --repo foo/bar pr merge 1`
- `npm --silent publish`
- `/bin/zsh -lc 'git push'`
- `env git push`
- `/usr/bin/env npm publish`
- `command git push`
- `sudo git push`

## Independent review

- Reviewer context: fresh / no implementation conversation
- Verdict: pass
- Findings: 迂回可能なrules、plan approval、task ID、done gate、承認証拠重複の各指摘を修正。最終再reviewではfindingなし。
- Re-review: 2026-10-27 pass
- Completion-state review: 2026-10-30 pass。owner承認記録、`done`同期、回帰test fixture更新にfindingなし。

## Owner review

- Required: yes
- Reason: workflow、task分割、Codex権限境界を今後の標準として採用する判断が必要。
- Result: approved
- Approved at: 2026-10-30
- Decision: 標準workflowとして採用する。

## Decisions and discoveries

- `PROJECT.md` は正本のまま維持し、実行計画・証拠はtask fileが所有する。
- Plan modeは会話モードであり、`.codex/config.toml` のapproval policyとは別に扱う。

## Handoff

- Completed: requested restructuring implementation、機械検証、独立review、owner review。
- Remaining: none。
- Next action: 実プロジェクトで利用を開始する場合は `T-001` の計画を提示する。
- Do not touch: application scaffold、deployment、remote Git state。
