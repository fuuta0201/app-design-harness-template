# Web Application Development Harness Template

Webサイト／Webアプリケーションの企画、設計、開発、テスト、公開を、セッションをまたいで一貫して進めるためのリポジトリテンプレートです。

このテンプレートは特定のフレームワーク、ホスティング、CMS、テストランナーを前提にしません。技術はプロジェクトの要件から選び、選定理由・仕様・タスク・検証証拠をリポジトリ内に残します。

## Harness structure

```text
.
├── AGENTS.md
├── README.md
├── docs/
│   ├── PROJECT.md
│   └── tasks/
│       ├── README.md
│       ├── TEMPLATE.md
│       ├── T-000-harness-template.md
│       ├── T-001-project-initialization.md
│       └── T-002-repository-collaboration-rules.md
├── .codex/
│   ├── config.toml
│   └── rules/project.rules
├── .agents/skills/
│   ├── app-development-harness/
│   │   └── SKILL.md
│   ├── independent-change-review/
│   │   └── SKILL.md
│   └── pull-request-workflow/
│       └── SKILL.md
├── scripts/
│   └── check_harness.py
└── .github/
    └── pull_request_template.md
```

- `AGENTS.md`: Codexが常に守る短い作業規約と、正本への案内。
- `docs/PROJECT.md`: 背景、仕様、設計、phase、決定、未解決事項、現在地、task索引を一元管理する正本。
- `docs/tasks/`: taskごとのscope、plan、承認、受け入れ条件、検証証拠、review、handoff。
- `.codex/`: 承認済みtaskを低摩擦で自動実装するsandbox／approval設定と、高影響commandのrules。
- `app-development-harness`: 企画から公開までを仕様駆動で進めるrepo-local Skill。
- `independent-change-review`: 実装会話を継承しない別エージェントによる変更レビュー手順。
- `pull-request-workflow`: 検証済み差分から日本語PR本文を作り、承認後に`gh`で公開する手順。
- `scripts/check_harness.py`: ハーネス構造、`docs/PROJECT.md` の整合性、必須成果物の末尾空白を検査する標準ライブラリのみのスクリプト。

Codexはルートから作業すると `AGENTS.md` を自動的に読みます。repo-local Skillは `.agents/skills/` に置き、繰り返し使う手順を必要なときだけ読み込ませます。この役割分担は、常時コンテキストを小さく保ちながら、詳細な工程を再利用するためのものです。

## 新しいプロジェクトでの使い方

1. このテンプレートからリポジトリを作成する。
2. `docs/PROJECT.md` の `{{...}}` を、確認済み事実または明示した仮説で埋める。
3. 背景、目標、非目標、利用者、制約、成功条件を先に確定する。
4. `docs/tasks/TEMPLATE.md` から最初のtask fileを作り、`PROJECT.md` の索引へ登録する。
5. Codexへ「`$app-development-harness` を使って次のready taskを計画して」と依頼する。UIで利用できる場合は `/plan` を使う。
6. 計画を確認してOKを出す。Codexは承認済みscope内を追加確認なしで実装・検証・独立reviewまで進める。
7. 公開など外部状態を変える操作は、影響とロールバックを確認してから別途実行する。

テンプレート状態の確認:

```bash
python3 scripts/check_harness.py --mode template
```

プロジェクトとして利用開始した後の確認:

```bash
python3 scripts/check_harness.py --mode project
```

## 基本原則

- 仕様を実装より先に書き、受け入れ条件と検証方法をタスクへ結び付ける。
- `docs/` は `PROJECT.md` と `docs/tasks/` を標準構成とする。
- task詳細は `docs/tasks/` に分離し、`PROJECT.md` には人が一覧できる索引だけを置く。
- 大きな調査結果、生成物、法務文書など、分離する実益がある場合だけ補助ファイルを作り、拡張子にかかわらず `PROJECT.md` の補助資料台帳へ登録する。
- 技術選定は最新情報、運用条件、チームの経験、保守性、費用、セキュリティ、公開方式を比較して決める。
- UIは可能な限り実行可能な仕様として、Storybook等のカタログ、unit test、interaction test、E2Eへ落とす。採用ツール自体は固定しない。
- 実装担当とは会話文脈を共有しない独立エージェントが、未コミット差分と検証証拠をレビューする。
- unit test／interaction testで十分に保証できる挙動は、逐一オーナーの目視承認を要求しない。視覚、文言、事業判断、公開判断など自動化できない部分だけをオーナーレビュー対象にする。
- commit、code comment、PR、documentationは日本語で記載し、code commentはwhatではなくwhyを1〜2行で書く。
- GitHub操作には`gh`を利用でき、PR作成時は必ず`pull-request-workflow` Skillへ従う。
- project初期化時はremote、認証、権限を確認し、可能ならmerge済み作業branchの自動削除を有効化する。

## テンプレートが固定しないもの

- UIフレームワーク、言語、パッケージマネージャー
- SSR／SSG／SPA等の配信方式
- CSS、デザインシステム、コンポーネントカタログの製品
- unit／interaction／E2E／visual regressionの製品
- CI、ホスティング、CMS、認証、Analytics、監視サービス
- ブランチ戦略、コミット粒度、公開環境数

これらは `docs/PROJECT.md` の制約と選定記録からプロジェクトごとに決定します。

## CodexのPlan → Auto運用

`.codex/config.toml` は、公式OpenAI Docsの低摩擦構成に合わせて `workspace-write`、`approval_policy = "on-request"`、`approvals_reviewer = "auto_review"` を設定しています。project-local configはtrusted projectでのみ読み込まれ、変更後はCodexの再起動が必要です。

- Plan: `/plan` またはrepositoryのPlan gateで、書き込み前に計画を提示する。
- Approval: オーナーのOKをtask fileへ記録する。
- Auto implementation: 承認済みscope内を実装、test、修正、独立reviewまで継続する。
- Stop: scope変更、仕様判断、credential、破壊操作、commit、push、deploy、外部変更だけは別承認を求める。

ユーザー本人が境界approvalも確認したい場合は、`.codex/config.toml` の `approvals_reviewer = "auto_review"` を `"user"` へ変更します。Plan modeのon/off自体はconfig項目ではなく、対応surfaceの `/plan` で切り替えます。
