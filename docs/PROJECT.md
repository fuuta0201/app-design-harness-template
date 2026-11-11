# Project Control Document

最終更新: {{YYYY-MM-DD}}

この文書はプロジェクトの背景、仕様、設計、phase、意思決定、未解決事項、現在地、task索引を一元管理する正本です。taskごとの計画と証拠は `docs/tasks/` が所有します。二重波括弧のplaceholderはプロジェクト開始時にすべて埋めます。確認できない内容は断定せず、`仮説`、`未決定`、`要確認` のいずれかを明記します。

## 0. Current snapshot

| 項目 | 内容 |
| --- | --- |
| プロジェクト名 | {{PROJECT_NAME}} |
| 種別 | {{website / web application / hybrid}} |
| 現在フェーズ | `P0` |
| 実行中タスク | なし |
| 次のreadyタスク | `T-001`（ready） |
| blocker | なし |
| 最終検証 | 2026-11-11: validator tests 29件、template validation／Python compile／whitespace検証、独立review、`isTemplate: true`確認成功 |
| 次に行うこと | テンプレート配布準備は完了。生成先では`T-001`からプロジェクト初期化を開始する |

## 1. Background and problem

### 1.1 Background

{{なぜこのプロジェクトが必要か。組織・事業・利用状況・既存システムの背景}}

### 1.2 Problem statement

{{誰が、どの状況で、何に困っているか。解決策ではなく問題を書く}}

### 1.3 Evidence and assumptions

| ID | 種別 | 内容 | 根拠／確認方法 | 状態 |
| --- | --- | --- | --- | --- |
| C-001 | 仮説 | {{EXAMPLE_ASSUMPTION}} | {{SOURCE_OR_VALIDATION}} | 未確認 |

## 2. Outcomes, scope, and success

### 2.1 Goals

- `G-001`: {{OUTCOME}}

### 2.2 Success measures

| ID | 指標 | 基準値 | 目標 | 計測方法 | 判定時期 |
| --- | --- | --- | --- | --- | --- |
| K-001 | {{METRIC}} | {{BASELINE}} | {{TARGET}} | {{METHOD}} | {{WHEN}} |

### 2.3 In scope

- {{IN_SCOPE}}

### 2.4 Non-goals

- {{NON_GOAL}}

## 3. Users and journeys

| ID | 利用者／役割 | 主な目的 | 重要な状況・制約 |
| --- | --- | --- | --- |
| U-001 | {{USER}} | {{JOB_TO_BE_DONE}} | {{CONTEXT}} |

| ID | 開始条件 | 行動 | 期待結果 | 失敗／復帰経路 |
| --- | --- | --- | --- | --- |
| J-001 | {{START}} | {{FLOW}} | {{RESULT}} | {{RECOVERY}} |

## 4. Requirements

### 4.1 Functional requirements

| ID | 要件 | 優先度 | 受け入れ条件 | 関連journey |
| --- | --- | --- | --- | --- |
| FR-001 | {{REQUIREMENT}} | must | {{OBSERVABLE_CRITERIA}} | `J-001` |

### 4.2 Quality attributes

数値は根拠がある場合だけ固定します。対象外とする属性にも理由を記録します。

| ID | 属性 | 基準／予算 | 検証方法 | 適用範囲 |
| --- | --- | --- | --- | --- |
| QR-001 | accessibility | {{STANDARD}} | {{AUTOMATED_AND_MANUAL}} | {{SCOPE}} |
| QR-002 | performance | {{BUDGET}} | {{MEASUREMENT}} | {{SCOPE}} |
| QR-003 | security/privacy | {{REQUIREMENT}} | {{THREAT_OR_TEST}} | {{SCOPE}} |
| QR-004 | reliability/recovery | {{REQUIREMENT}} | {{FAILURE_TEST}} | {{SCOPE}} |
| QR-005 | compatibility | {{BROWSERS_DEVICES}} | {{TEST_MATRIX}} | {{SCOPE}} |

### 4.3 Harness template requirements

この節はテンプレート自体の不変条件です。新規プロジェクトでも削除せず、プロジェクト固有要件と併存させます。

| ID | 要件 | 受け入れ条件 |
| --- | --- | --- |
| HR-001 | 正本の責務を一元化する | project context／spec／task索引は `docs/PROJECT.md`、task詳細／証拠は `docs/tasks/` が所有し、補助資料は台帳登録される |
| HR-002 | 常時規約と反復手順を分離する | `AGENTS.md` が短い入口、`.agents/skills/` が必要時に読む工程を所有する |
| HR-003 | 仕様駆動で進行する | すべての実装taskが独立fileとして仕様ID、scope、plan、承認、受け入れ条件、検証、review分類を持つ |
| HR-004 | 独立reviewを必須化する | 実装会話を継承しないreviewerが完了前の未コミット差分を確認する |
| HR-005 | owner reviewを判断領域に限定する | unit／interaction testで十分に保証した挙動はowner reviewを省略でき、visual・content・business・release判断は残す |
| HR-006 | 技術選定を固定しない | framework、hosting、CMS、test製品をテンプレートが決め打ちせず、要件から選定する |
| HR-007 | templateと利用プロジェクトを検証できる | validatorがplaceholderを許すtemplate modeと、拒否するproject modeを持ち、ネストした未登録補助文書も検出する |
| HR-008 | Plan承認後に自動実装する | 書き込み前にplan approvalを必須とし、承認済みscope内は追加確認なしで実装・検証・独立reviewまで進める。高影響操作は別承認とする |
| HR-009 | taskをdocs配下へ集約する | task正本、雛形、運用説明を `docs/tasks/` に置き、索引・validator・Skill・文書参照が同じpathを使う |
| HR-010 | 開発成果物の言語とcode commentを統一する | commit、code comment、PR、documentationは日本語とし、code commentはwhatを反復せずwhyを1〜2行で簡潔に記す |
| HR-011 | PR作成手順を再利用可能にする | PR Skillが概要、commit単位の実装内容、test内容、review観点を日本語で生成し、PR作成時に必ず適用される |
| HR-012 | GitHub操作を標準化する | local Gitは`git`、GitHubのPR／repository操作は`gh`を使用でき、project初期化時は権限とremoteがあればmerge済みbranchの自動削除を設定する |
| HR-013 | ハーネスを安全に導入できる | 新規プロジェクトは元リポジトリとGit履歴・remoteを共有しないTemplate Repositoryから生成し、`T-001`でテンプレート保守用の現在地・task・decisionを除去してプロジェクト正本へ初期化する。既存プロジェクトは既存資産を保護する移行手順で導入する |

## 5. Constraints and external dependencies

| ID | 種別 | 内容 | 所有者 | 変更権限 | 障害時の扱い |
| --- | --- | --- | --- | --- | --- |
| X-001 | constraint | {{CONSTRAINT}} | {{OWNER}} | {{AUTHORITY}} | {{FALLBACK}} |

### Secrets and environments

値は書かず、名前と用途だけを管理します。

| 名前 | 用途 | local | preview/staging | production | 保管場所 |
| --- | --- | --- | --- | --- | --- |
| `{{ENV_NAME}}` | {{PURPOSE}} | 要 | 要 | 要 | {{SECRET_STORE}} |

## 6. Existing-state inventory and preservation

新規プロジェクトで不要な場合は「対象外」と理由を書きます。リニューアル／移行では、現行情報・URL・機能・データ・外部連携を承認なく欠落させません。

| ID | 現行資産／挙動 | 所在・根拠 | 方針 | 移行後の検証 | 状態 |
| --- | --- | --- | --- | --- | --- |
| M-001 | {{CURRENT_ASSET}} | {{SOURCE}} | preserve / change / retire | {{VERIFICATION}} | 未確認 |

## 7. Technology decisions

### 7.1 Selection criteria

- 要件・品質属性への適合
- 運用、保守、障害復旧、移行の容易さ
- チームの経験と学習コスト
- エコシステム、更新頻度、サポート期間
- セキュリティ、プライバシー、費用、ベンダーロックイン
- build、test、preview、deployを再現できること

### 7.2 Decision matrix

| 候補 | 適合性 | 利点 | リスク／不採用理由 | 検証根拠 | 結論 |
| --- | --- | --- | --- | --- | --- |
| {{OPTION}} | {{FIT}} | {{BENEFITS}} | {{RISKS}} | {{PRIMARY_SOURCES_OR_SPIKE}} | 未決定 |

### 7.3 Adopted stack

| 領域 | 採用 | バージョンの正本 | 選定理由 |
| --- | --- | --- | --- |
| runtime | {{TBD}} | {{LOCK_OR_CONFIG}} | {{RATIONALE}} |
| application | {{TBD}} | {{LOCK_OR_CONFIG}} | {{RATIONALE}} |
| styling/design | {{TBD}} | {{LOCK_OR_CONFIG}} | {{RATIONALE}} |
| test | {{TBD}} | {{LOCK_OR_CONFIG}} | {{RATIONALE}} |
| hosting/operations | {{TBD}} | {{CONFIG}} | {{RATIONALE}} |

## 8. Architecture and contracts

### 8.1 System boundaries

{{クライアント、サーバー、データ、外部サービス、信頼境界、生成／実行時の責務}}

### 8.2 Modules and ownership

| ID | モジュール | 責務 | 入出力／契約 | 依存してよいもの | 依存禁止 |
| --- | --- | --- | --- | --- | --- |
| A-001 | {{MODULE}} | {{RESPONSIBILITY}} | {{CONTRACT}} | {{ALLOWED}} | {{FORBIDDEN}} |

### 8.3 Data and failure behavior

| ID | データ／処理 | 正本 | validation | error / empty / loading | recovery |
| --- | --- | --- | --- | --- | --- |
| D-001 | {{DATA_FLOW}} | {{SOURCE}} | {{RULE}} | {{STATES}} | {{RECOVERY}} |

## 9. Experience and design system

### 9.1 Information architecture / application structure

| ID | route / screen / flow | 目的 | 主な内容・操作 | entry / exit | 権限・状態 |
| --- | --- | --- | --- | --- | --- |
| IA-001 | {{ROUTE_OR_SCREEN}} | {{PURPOSE}} | {{CONTENT_ACTION}} | {{NAVIGATION}} | {{STATE}} |

### 9.2 Visual direction

{{ブランド、tone、参考、避ける表現。探索案と承認済み仕様を区別する}}

### 9.3 Design tokens

| ID | category | semantic role | value / scale | accessibility notes | 状態 |
| --- | --- | --- | --- | --- | --- |
| DS-001 | color | {{ROLE}} | {{VALUE}} | {{CONTRAST_OR_MEANING}} | proposal |

### 9.4 Component contracts

| ID | component | responsibility | states / variants | accessibility | story/test | 状態 |
| --- | --- | --- | --- | --- | --- | --- |
| UI-001 | {{COMPONENT}} | {{RESPONSIBILITY}} | {{STATES}} | {{A11Y_CONTRACT}} | {{EXECUTABLE_SPEC}} | planned |

デザイン探索は本番UIと分離し、比較・承認した値だけをproduction token／componentへ昇格します。共通UIは重要状態、keyboard、focus、reduced motion、responsive、error／emptyを必要に応じて実行可能な仕様にします。

## 10. Verification strategy

### 10.1 Test layers

| layer | 保証するもの | 対象外 | command / environment |
| --- | --- | --- | --- |
| static | format、lint、types、schema | runtime behavior | {{COMMAND}} |
| unit | 純粋ロジックと局所契約 | browser integration | {{COMMAND}} |
| interaction | 利用者操作、role、focus、component states | live external services | {{COMMAND}} |
| integration | module／service境界 | end-to-end deployment | {{COMMAND}} |
| E2E | build成果物、主要journey、失敗復帰 | exhaustive edge cases | {{COMMAND}} |
| visual/manual | 視覚品質、content、brand、実機特性 | 自動判定可能な挙動 | {{METHOD}} |

### 10.2 Standard commands

| intent | command | CIでも同一か | 備考 |
| --- | --- | --- | --- |
| develop | `{{COMMAND}}` | - | {{NOTES}} |
| test | `{{COMMAND}}` | yes / no | {{NOTES}} |
| build | `{{COMMAND}}` | yes / no | {{NOTES}} |
| integrated check | `{{COMMAND}}` | yes | formatからbuildまでの主要検証を1コマンドへ集約 |

### 10.3 Review policy

- 実装・設定・仕様変更は、機械検証後かつ完了前に独立エージェントレビューを通す。
- reviewerは実装会話を継承せず、リポジトリの正本とdiffから判断する。
- unit／interaction testで受け入れ条件が十分に保証される場合、オーナーの逐次レビューは不要。該当テストをタスクの証拠欄へ記録する。
- visual、copy、business rule、legal、cost、external state、release acceptanceはオーナー判断を残す。
- commit message、code comment、PR、documentationは日本語で記載する。code commentはwhyが必要な場合だけ1〜2行で書き、whatを反復しない。
- PR作成・更新時は `pull-request-workflow` Skillを必ず使い、GitHub操作は`gh`で行う。

## 11. Delivery and operations

| environment | purpose | source / branch | data / service boundary | deploy trigger | approval |
| --- | --- | --- | --- | --- | --- |
| local | {{PURPOSE}} | working tree | {{BOUNDARY}} | manual | none |
| preview/staging | {{PURPOSE}} | {{SOURCE}} | {{BOUNDARY}} | {{TRIGGER}} | {{GATE}} |
| production | {{PURPOSE}} | {{SOURCE}} | {{BOUNDARY}} | {{TRIGGER}} | owner |

### Release checklist

- [ ] 対象version／commitと成果物が一致する
- [ ] migration、環境変数、外部サービス境界を確認した
- [ ] backup／rollback方法と実行権限を確認した
- [ ] 主要journey、accessibility、performance、securityの必要なgateが成功した
- [ ] monitoring、analytics、error reporting、問い合わせ経路を確認した
- [ ] 公開後smoke testと観測期間を決めた

### Rollback and recovery

{{直前の正常版、データ互換性、切り戻し手順、責任者、許容停止時間}}

### GitHub repository settings

- project初期化時にremote、`gh auth status`、repository権限を確認する。
- 条件を満たし、外部変更の明示承認を得た場合は `gh repo edit --delete-branch-on-merge` を実行する。
- 実行結果または実行できない理由を初期化taskのVerificationへ記録する。

## 12. Roadmap and task ledger

### 12.1 Phase model

フェーズは順序の目安です。不要なフェーズは理由を意思決定ログへ残して省略できます。

| ID | phase | exit criteria | 状態 |
| --- | --- | --- | --- |
| P0 | context and discovery | 背景、現状、制約、仮説が区別される | active |
| P1 | product specification | goals、users、requirements、success、non-goalsが合意される | planned |
| P2 | technology and architecture | 比較根拠、境界、risk、spike結果が記録される | planned |
| P3 | experience and design system | IA、visual direction、tokens、component contractsが承認される | planned |
| P4 | foundation | 標準command、test、CI、preview、secret境界が成立する | planned |
| P5 | incremental implementation | 各sliceが仕様、test、独立reviewを満たす | planned |
| P6 | system verification | E2E、a11y、performance、security、recoveryを確認する | planned |
| P7 | release | staging、本番、smoke、rollback、monitoringが成立する | planned |
| P8 | retrospective | 学びをハーネスと次のbacklogへ反映する | planned |

### 12.2 Status rules

`planned → ready → in_progress → in_review → done`

- `blocked` は理由と解除条件を必ず持つ。
- `ready`: 仕様、依存関係、受け入れ条件、検証方法、権限が明確。
- `in_review`: 実装と該当検証が完了し、独立レビュー中。
- `done`: 受け入れ条件、該当検証、独立レビュー、必要なオーナー判断、文書更新が完了。

### 12.3 Tasks

この表は人が現在地を把握するための索引です。taskの詳細と証拠は `docs/tasks/` の対応fileが所有します。

| ID | phase | title | task file | status | owner review |
| --- | --- | --- | --- | --- | --- |
| T-000 | P0 | 再利用可能な開発ハーネス基盤を定義する | `docs/tasks/T-000-harness-template.md` | done | required |
| T-001 | P0 | プロジェクト制御文書を初期化する | `docs/tasks/T-001-project-initialization.md` | ready | required |
| T-002 | P0 | task配置とGitHub協業規約を更新する | `docs/tasks/T-002-repository-collaboration-rules.md` | done | required |
| T-003 | P0 | ハーネスの導入経路を整備する | `docs/tasks/T-003-harness-adoption.md` | done | required |

## 13. Decision log

重要な選択、却下案、例外、仕様変更を追記します。過去の決定を消さず、置換関係を記録します。

`scope`は、利用プロジェクトに残す決定を`project`、配布元の保守だけに必要な決定を`template`として区別します。Template Repositoryから生成したプロジェクトでは、`T-001`でtemplate scopeの行を削除します。

| ID | scope | 日付 | 状態 | 決定 | 理由 | 影響／置換 | 決定者 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADR-001 | {{project / template}} | {{YYYY-MM-DD}} | proposed | {{DECISION}} | {{RATIONALE}} | {{IMPACT}} | {{OWNER}} |
| ADR-002 | template | 2026-11-11 | accepted | 新規プロジェクトはGitHub Template Repositoryから生成し、既存プロジェクトへの導入は移行手順として分離する | 新規生成では元リポジトリとのremote・履歴共有を避け、既存導入では既存の規約・文書・設定を上書きしないため | `README.md`、GitHub repository設定、`T-001`への導線 | owner |

## 14. Open questions and risks

| ID | 種別 | 内容 | 影響 | owner | 期限／解除条件 | 状態 |
| --- | --- | --- | --- | --- | --- | --- |
| Q-001 | question | {{QUESTION}} | {{IMPACT}} | {{OWNER}} | {{CONDITION}} | open |
| R-001 | risk | {{RISK}} | {{IMPACT}} | {{OWNER}} | {{MITIGATION}} | open |

## 15. Task evidence and handoff

- 各taskの計画、承認、検証証拠、独立review、owner review、handoffは対応する `docs/tasks/<ID>-<slug>.md` を正本とする。
- この文書には詳細logを複製せず、Current snapshotと12.3のtask索引だけを同期する。
- 復帰時はセクション0、関連spec、12.3、14と、実行中／次のready task fileを読む。

## 16. Supplementary document registry

`docs/PROJECT.md` と標準の `docs/tasks/` から分ける実益がある場合だけ追加します。生成物、長大な調査資料、法務上独立管理が必要な文書などが対象です。拡張子や階層にかかわらず、未登録の補助fileを `docs/` 配下へ作らないでください。

| path | 所有する情報 | 分離理由 | 更新契機 | status |
| --- | --- | --- | --- | --- |
| - | - | 現在は補助文書なし | - | - |
