# T-{{TASK_ID}}: {{TITLE}}

| 項目 | 内容 |
| --- | --- |
| Status | planned |
| Phase | {{PHASE_ID}} |
| Linked specs | {{SPEC_IDS}} |
| Depends on | {{DEPENDENCIES}} |
| Owner review | required / not_required — {{REASON}} |
| Plan approval | pending |

## 目的

{{このtaskが達成する観測可能な結果}}

## Source context

- `docs/PROJECT.md` の参照節／spec ID: {{SOURCE}}
- 関連task／補助資料: {{RELATED}}

## Scope

### In scope

- {{IN_SCOPE}}

### Non-goals

- {{NON_GOAL}}

## Implementation plan

1. {{STEP}}

### Expected changes

- {{PATH_OR_COMPONENT}}

### Red / Green / Refactor / Verify

- Red: {{FAILING_TEST_OR_CHECK}}
- Green: {{MINIMUM_IMPLEMENTATION}}
- Refactor: {{SAFE_REFINEMENT}}
- Verify: {{FOCUSED_AND_INTEGRATED_CHECKS}}

### Risks and recovery

- Risk: {{RISK}}
- Recovery / rollback: {{RECOVERY}}

## Approval gate

- Plan presented: no
- Approved by: pending
- Approved at: pending
- Approval covers: pending
- Separate approval still required for: commit、push、deploy、外部サービス変更、破壊操作、scope拡張

承認前はapplication code、test、dependency、configurationを変更しません。承認後は、このtaskで合意したscope内を追加確認なしで実装・検証・独立reviewまで進めます。

## Acceptance criteria

- [ ] {{OBSERVABLE_CRITERION}}

## Verification

| command / review | result | evidence / limitations |
| --- | --- | --- |
| `{{COMMAND}}` | not_run | {{DETAIL}} |

`done` ではresultを `pass`、`passed`、`success`、`not_applicable` のいずれかにします。

## Independent review

- Reviewer context: fresh / no implementation conversation
- Verdict: not_run
- 完了値: `pass` または `pass_with_non_blocking_findings`
- Findings: pending
- Re-review: pending

## Owner review

- Required: yes / no
- Reason: {{HUMAN_JUDGMENT_OR_TEST_COVERAGE}}
- Result: pending
- 完了値: Requiredがyesなら `approved`、noなら `not_required`

## Decisions and discoveries

- {{MATERIAL_DECISION_OR_DISCOVERY}}

## Handoff

- Completed:
- Remaining:
- Next action:
- Do not touch:
