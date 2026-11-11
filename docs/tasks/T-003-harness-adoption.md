# T-003: ハーネスの導入経路を整備する

| 項目 | 内容 |
| --- | --- |
| Status | done |
| Phase | P0 |
| Linked specs | `HR-001`, `HR-007`, `HR-008`, `HR-012`, `HR-013` |
| Depends on | `T-000`, `T-002` |
| Template role | maintenance |
| Owner review | required — 公開リポジトリの設定と利用者向け導入体験を確定するため |
| Plan approval | approved |

## 目的

新規・既存プロジェクトの利用者が、ハーネスの元リポジトリへ誤ってpushしたり既存資産を上書きしたりせず、導入後に`T-001`から開発を開始できる状態にする。

## Source context

- `docs/PROJECT.md` の `HR-001`、`HR-007`、`HR-008`、`HR-012`、`HR-013`、セクション11、12、13
- `README.md` の「新しいプロジェクトでの使い方」
- GitHub DocsのTemplate Repository仕様とGitHub CLIの`gh repo create --template`仕様
- 関連task: `T-001`、`T-002`

## Scope

### In scope

- 新規プロジェクトをGitHub Template RepositoryからWeb UIまたは`gh`で生成する手順を`README.md`へ記載する。
- 生成先の`origin`、元テンプレートと分離したGit履歴、テンプレート更新が自動同期されないことを明記する。
- 生成後のtemplate検証、Codex再起動、`T-001`の計画開始、初期化後のproject検証までの導線を定義する。
- `T-001`で`README.md`と`docs/PROJECT.md`を対象プロジェクト用へ初期化し、`maintenance` task・template scopeのdecision・保守用snapshotを除去する契約を定義する。
- validatorのtemplate modeではテンプレート保守成果物を要求し、project modeではその残存を拒否する。
- 既存プロジェクトでは通常のcloneや一括上書きを避け、専用branch上で既存の`AGENTS.md`、`.codex/`、`.agents/`、`docs/`、`.github/`、`.gitignore`を調査・統合する移行手順を記載する。
- `README.md`の必須導入情報をvalidatorとunit testで機械検証する。
- 別の外部操作承認後に、GitHub repositoryをTemplate Repositoryとして有効化し、結果を確認する。

### Non-goals

- 既存プロジェクトへファイルを自動コピー・自動マージするinstallerの実装。
- テンプレート更新を利用プロジェクトへ自動同期する仕組み。
- 新しいプロジェクトの実作成、`T-001`の実行、application実装。
- commit、push、PR作成。

## Implementation plan

1. `README.md`の導入節を、新規プロジェクトと既存プロジェクトの2経路へ再構成する。
2. 新規経路へGitHub Web UIと`gh repo create --template ... --clone`の手順、履歴・remote・更新同期の境界を記載する。
3. 生成後の検証、Codex project configの読込、`T-001`開始までの順序を記載する。
4. `T-001`へREADMEのproject化、テンプレート保守情報の清掃、ハーネス不変条件の保持を追加する。
5. 既存経路へread-only inventory、専用branch、ファイル単位の統合、検証、独立reviewという移行手順を記載する。
6. `docs/PROJECT.md`の要件、意思決定、task索引、現在地を実装結果へ同期する。
7. `scripts/check_harness.py`をtemplate／projectそれぞれの成果物契約へ分離し、必須導入情報とテンプレート保守情報の残存を検査する。
8. `scripts/test_check_harness.py`へ導入情報欠落とproject modeでの保守情報残存を検出するtestを追加する。
9. unit test、template validation、project化fixture、Python compile、whitespace検証を行う。
10. 未commit差分を会話履歴のない別エージェントへ独立reviewさせ、指摘を解消して再検証する。
11. owner review後、別承認を得て`gh repo edit --template`を実行し、`isTemplate: true`を確認する。

### Expected changes

- `README.md`
- `docs/PROJECT.md`
- `docs/tasks/README.md`
- `docs/tasks/T-001-project-initialization.md`
- `docs/tasks/T-003-harness-adoption.md`
- `scripts/check_harness.py`
- `scripts/test_check_harness.py`
- GitHub repository setting: `fuuta0201/app-design-harness-template`のTemplate Repository有効化

### Red / Green / Refactor / Verify

- Red: 新規・既存の導入経路または必須commandがREADMEから欠落したfixtureでvalidator testを失敗させる。
- Red: project modeのfixtureへテンプレート保守用taskまたはdecisionを残し、validator testを失敗させる。
- Green: README、`T-001`、validatorへ導入・project化契約を追加する。
- Refactor: 重複する原則を正本へ集約し、READMEは実行順と利用者向け説明に限定する。
- Verify: unit test、template mode、Python compile、`git diff --check`、GitHubの`isTemplate`確認。

### Risks and recovery

- Risk: 既存プロジェクト向け手順が一括コピーを促し、既存規約や設定を上書きする。
- Mitigation: read-only inventory、専用branch、file単位の統合、差分reviewを必須手順にする。
- Risk: Template Repository化を、利用プロジェクトへの更新同期機能と誤解させる。
- Mitigation: 単発生成であり自動同期しないことを明記する。
- Risk: 初期化時に`AGENTS.md`、Skill、Codex設定、`HR-*`まで削除してハーネスを失う。
- Mitigation: 削除対象をテンプレート保守用task、索引、snapshot、decisionへ限定し、project modeのfixture testで保持対象を検証する。
- Recovery / rollback: 文書・validator変更は差分をrevertする。GitHub設定は別承認のうえ`gh repo edit --template=false`で無効化し、実行前後の状態を記録する。

## Approval gate

- Plan presented: yes
- Approved by: owner
- Approved at: 2026-11-11 22:26 JST
- Approval covers: READMEの新規・既存導入経路、`T-001`のproject化契約、validator／unit test、正本文書、検証、独立review
- Separate approval still required for: `gh repo edit --template`、commit、push、PR作成、scope拡張

承認前はREADME、validator、test、GitHub設定を変更しません。承認後は、repository内の承認済みscopeを追加確認なしで実装・検証・独立reviewまで進めます。

## Acceptance criteria

- [x] 新規プロジェクトをWeb UIまたは`gh repo create --template ... --clone`で生成できる手順がある。
- [x] 通常のclone・forkとの違い、生成先のremote、履歴分離、自動更新されないことが説明されている。
- [x] 生成後にtemplate検証、Codex再起動、`T-001`の計画、project検証へ進む順序が明確である。
- [x] `T-001`がREADMEとPROJECTを対象プロジェクト用へ初期化し、テンプレート保守用task・索引・snapshot・decisionを削除する。
- [x] project modeがテンプレート保守情報の残存を拒否し、`AGENTS.md`、Skill、Codex設定、`HR-*`の保持を検証する。
- [x] 既存プロジェクトの既存資産を保護する移行手順と、自動installerが今回の対象外であることが明確である。
- [x] 必須導入情報の欠落をvalidator unit testが検出する。
- [x] 独立reviewが完了する。
- [x] owner reviewが完了する。
- [x] 別の外部操作承認後、GitHub repositoryで`isTemplate: true`を確認できる。

## Verification

| command / review | result | evidence / limitations |
| --- | --- | --- |
| `python3 -m unittest scripts/test_check_harness.py` | pass | 29 tests。project化fixture、保守task／template decision残存、`HR-001`〜`HR-013`保持、README導入契約を含む |
| `python3 scripts/check_harness.py --mode template` | pass | template全体の整合性 |
| `python3 -m py_compile scripts/check_harness.py scripts/test_check_harness.py` | pass | Python syntax |
| `git diff --check` | pass | whitespace errorなし |
| independent review | pass | 初回2 findingsを修正後、再reviewでfindingなし |
| `gh repo view fuuta0201/app-design-harness-template --json nameWithOwner,isTemplate,url,visibility,defaultBranchRef` | pass | 2026-11-11、`isTemplate: true`、PUBLIC、default branch `main`を確認 |

## Independent review

- Reviewer context: fresh / no implementation conversation
- Verdict: pass
- 完了値: `pass` または `pass_with_non_blocking_findings`
- Findings: 初回reviewでsnapshot fixtureの状態依存と`HR-*`保持testの欠落を指摘。両方を修正し、再reviewではfindingなし。
- Re-review: 2026-11-11 pass。completion-state fixture修正後もfindingなし。

## Owner review

- Required: yes
- Reason: 公開リポジトリの設定変更と、利用者が最初に従う導入体験の判断を含む。
- Result: approved
- Approved at: 2026-11-11 22:42 JST
- Decision: 新規／既存の導入経路、`T-001`のproject化境界、保持・削除対象を承認する。
- 完了値: `approved`

## Decisions and discoveries

- 2026-11-11: GitHub APIで`fuuta0201/app-design-harness-template`の`isTemplate: false`を確認した。
- 新規生成と既存プロジェクトへの移行は、既存資産の有無と安全条件が異なるため別経路として扱う。
- GitHub Template Repositoryに生成後hookはないため、`T-001`をtemplateからprojectへの明示的な変換工程とする。
- taskの`Template role`とdecisionの`scope`をproject modeで検査し、将来の保守taskも固定IDに依存せず除去対象として判別する。
- 独立reviewで、taskを`in_review`へ更新した後にsnapshot fixtureが旧状態へ依存していたことが判明した。snapshot置換を正規表現で状態非依存にし、検証証拠を再取得した。
- `HR-*`保持を文書だけでなくvalidator contractに加え、`HR-001`〜`HR-013`を個別に削除するnegative testで保証する。
- 2026-11-11: 別の外部操作承認後に`gh repo edit fuuta0201/app-design-harness-template --template`を実行し、GitHub APIで`isTemplate: true`を確認した。
- `done`同期後にsnapshot mismatch testが旧`T-003`状態へ依存して失敗したため、現在のnext ready行の存在をtest内で確認してから不整合へ変更するfixtureへ修正した。

## Handoff

- Completed: 導入手順、project化契約、validator／tests、独立review、owner review、Template Repository有効化、commit `b2daf70`の`origin/main`反映。
- Remaining: none。
- Next action: 生成先で`T-001`を計画し、対象プロジェクト用へ初期化する。
- Do not touch: application code、dependencies、利用プロジェクト、新たなGitHub設定。
