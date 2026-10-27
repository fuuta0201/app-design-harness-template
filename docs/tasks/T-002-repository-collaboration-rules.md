# T-002: task配置とGitHub協業規約を更新する

| 項目 | 内容 |
| --- | --- |
| Status | done |
| Phase | P0 |
| Linked specs | `HR-009`〜`HR-012` |
| Depends on | `T-000` |
| Owner review | required — repository標準、文章規約、GitHub外部設定を決めるため |
| Plan approval | approved |

## 目的

task正本を `docs/tasks/` に集約し、日本語でのGit／GitHub協業、why中心のcode comment、再利用可能なPR作成、merge後branch自動削除をハーネス標準として定義する。

## Source context

- `docs/PROJECT.md`: `HR-009`〜`HR-012`
- ユーザーが指定したrepository構成、言語、comment、PR、branch設定
- `gh repo edit --help`: `--delete-branch-on-merge` が利用可能

## Scope

### In scope

- rootの `tasks/` 全体を `docs/tasks/` へ移し、全参照、validator、testsを同期する。
- `git` と `gh` の利用方針、commit／code comment／PR／documentationの日本語規約を定義する。
- code commentをwhy中心の1〜2行に限定する規約を定義する。
- 日本語PR本文を作成・検証し、`gh pr create` へ渡すrepo-local Skillを追加する。
- PR templateを概要、commit別実装内容、test内容、review観点へ更新する。
- project初期化時に、remoteと権限がある場合だけ `gh repo edit --delete-branch-on-merge` を実行する手順と証拠欄を定義する。
- validatorと回帰testで新しい構成と必須Skillを検証する。

### Non-goals

- このtask内でのcommit、push、PR作成、remote repository設定変更。
- branch protection、merge方式、CI provider、release方式の決め打ち。
- 既存application codeへのcomment一括変更。

## Implementation plan

1. rootの `tasks/` を `docs/tasks/` へ移し、README、AGENTS、PROJECT、Skills、PR template、validator、testsの参照を一括更新する。
2. `AGENTS.md` と開発Skillへ、`git`／`gh`利用、日本語成果物、why中心commentの規約を追加する。
3. `skill-creator` の形式で日本語の `pull-request-workflow` SkillとUI metadataを作成し、PR作成時の必須手順、情報収集、本文構造、`gh pr create`前の承認境界を定義する。
4. PR templateを、概要、commitごとの実装内容、test内容、review観点を中心とした日本語templateへ更新する。
5. project初期化taskへ、remote／権限確認後に `gh repo edit --delete-branch-on-merge` を実行し、結果を記録する手順を追加する。
6. validatorとtestsを `docs/tasks/`、新Skill、PR templateの不変条件へ更新する。
7. 機械検証と、実装会話を継承しない独立reviewを行う。

### Expected changes

- rootの `tasks/` → `docs/tasks/`
- `AGENTS.md`, `README.md`, `docs/PROJECT.md`
- `.agents/skills/app-development-harness/`
- `.agents/skills/pull-request-workflow/`
- `.github/pull_request_template.md`
- `scripts/check_harness.py`, `scripts/test_check_harness.py`

### Red / Green / Refactor / Verify

- Red: 旧 `tasks/` path、PR Skill欠落、索引／filename不整合を拒否する回帰testを追加する。
- Green: 最小のpath移行、規約、Skill、template、validator更新を行う。
- Refactor: 重複するPR規約と承認境界をSkillへ集約する。
- Verify: unit tests、template validation、Python compile、3 Skillsのquick validation、execpolicy、独立review。

### Risks and recovery

- Risk: path変更後に古い参照が残り、task discoveryまたはvalidatorが壊れる。
- Recovery / rollback: 検索で旧path残存を検出し、移行単位全体を元のroot pathへ戻せるよう変更を一つのtaskに閉じる。
- Risk: branch自動削除を権限やremote未確認で実行する。
- Recovery / rollback: template作成時は手順だけを定義し、実project初期化時も別の外部操作承認後に実行する。

## Approval gate

- Plan presented: yes
- Approved by: project owner
- Approved at: 2026-10-27
- Approval covers: T-002に記載したrepository-local構成、規約、Skill、template、validatorの変更と検証
- Separate approval still required for: commit、push、PR作成、remote repository設定変更、deploy、破壊操作、scope拡張

承認前は上記plan artifact以外を変更しません。承認後は、このtaskで合意したscope内を追加確認なしで実装・検証・独立reviewまで進めます。

## Acceptance criteria

- [x] task関連fileがすべて `docs/tasks/` にあり、rootに旧directoryが残らない。
- [x] 全てのtask参照、validator、testsが `docs/tasks/` を正本として扱う。
- [x] `git` と `gh` の許可用途、外部変更前の承認境界が明文化される。
- [x] commit、code comment、PR、documentationの日本語規約が定義される。
- [x] code commentはwhatではなくwhyを1〜2行で書く規約が定義される。
- [x] PR Skillと日本語PR templateが、概要、commit別実装内容、test内容、review観点を必須化する。
- [x] project初期化時の `gh repo edit --delete-branch-on-merge` 手順が、権限／remote確認と結果記録を含む。
- [x] 機械検証と独立reviewがpassする。

## Verification

| command / review | result | evidence / limitations |
| --- | --- | --- |
| `python3 -m unittest scripts/test_check_harness.py` | pass | 23 tests |
| `python3 scripts/check_harness.py --mode template` | pass | `docs/tasks/`、PR template、Skill必須fileを含む |
| `python3 -m py_compile scripts/check_harness.py scripts/test_check_harness.py` | pass | syntax compile |
| `python3 /Users/satofuta/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/app-development-harness` | pass | Skill structure |
| `python3 /Users/satofuta/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/independent-change-review` | pass | Skill structure |
| `python3 /Users/satofuta/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/pull-request-workflow` | pass | Skill structure |
| `git diff --check` | pass | tracked差分のwhitespace errorなし。未追跡の必須fileはvalidatorが検査 |
| `codex execpolicy check --rules .codex/rules/project.rules -- gh pr create --title test --body test` | pass | `prompt`判定。PRは未作成 |
| `codex execpolicy check --rules .codex/rules/project.rules -- gh repo edit --delete-branch-on-merge` | pass | `prompt`判定。repository設定は未変更 |
| independent review | pass | 会話文脈なしのagentが全差分と23 testsを確認 |

## Independent review

- Reviewer context: fresh / no implementation conversation
- Verdict: pass
- Findings: findingなし。`docs/tasks/`の許可外file拒否追加後もregressionなし。
- Re-review: 2026-10-27 pass

## Owner review

- Required: yes
- Reason: repository構成、協業規約、GitHub外部設定の標準化はowner判断を要する。
- Result: approved

## Decisions and discoveries

- `gh repo edit --delete-branch-on-merge` は現在のlocal `gh` CLIで利用できる。
- branch自動削除の有効化はremote変更なので、template作成時には実行せず、project初期化時に別承認を得て行う。

## Handoff

- Completed: task移動、規約、PR Skill／template、project初期化手順、validator／tests、機械検証、独立review、owner review。
- Remaining: none。
- Next action: `T-001` または新しいproject taskへ進む。
- Do not touch: remote GitHub state、push、PR、deploy。
