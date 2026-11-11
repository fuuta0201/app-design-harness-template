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
│       ├── T-002-repository-collaboration-rules.md
│       └── T-003-harness-adoption.md
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
│   ├── check_harness.py
│   └── test_check_harness.py
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

## 新規プロジェクトへ導入する

通常のcloneやforkではなく、GitHub Template Repositoryから新しいリポジトリを生成します。生成先は元テンプレートとは異なるGit履歴を持ち、`origin`は生成したリポジトリを指します。テンプレート側の更新は生成先へ自動同期されません。

仕様の詳細は[GitHub Docs: Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)と[GitHub CLI: `gh repo create`](https://cli.github.com/manual/gh_repo_create)を参照してください。

GitHubのWeb UIでは、このリポジトリの **Use this template** から **Create a new repository** を選び、owner、repository名、visibilityを指定します。CLIでは次のように作成とcloneを一度に行えます。

```bash
gh repo create OWNER/REPOSITORY \
  --private \
  --template fuuta0201/app-design-harness-template \
  --clone
cd REPOSITORY
```

`OWNER/REPOSITORY`、visibility、clone先はプロジェクトに合わせて変更します。`--include-all-branches`は指定せず、承認済みのdefault branchだけを開始点にします。

### 生成後の初期化

1. `python3 scripts/check_harness.py --mode template`で生成直後の構造を確認する。
2. Codexで生成先をtrusted projectとして開き直す。`.codex/config.toml`を読み込ませるため、信頼設定後にCodexを再起動する。
3. Codexへ「`$app-development-harness`を使って`T-001`を計画して」と依頼し、提示されたscopeを確認して承認する。
4. `T-001`で`README.md`と`docs/PROJECT.md`を対象プロジェクト用へ初期化し、`Template role: maintenance`のtask、template scopeのdecision、保守用snapshotを削除する。
5. `AGENTS.md`、`.agents/skills/`、`.codex/`、`docs/tasks/TEMPLATE.md`、`HR-*`のハーネス不変条件は保持する。
6. 初期化後に`python3 scripts/check_harness.py --mode project`を実行し、placeholderとテンプレート保守情報が残っていないことを確認する。

`T-001`完了後は、対象プロジェクトの`README.md`、`docs/PROJECT.md`、`docs/tasks/`が正本になります。通常のcloneでこの配布元を直接開発したり、生成先の`origin`を配布元へ向けたりしないでください。

## 既存プロジェクトへ導入する

既存プロジェクトでは、テンプレートを一括コピーしたり既存リポジトリのremoteに設定したりしません。既存の規約、文書、設定、application codeを保護するため、導入自体を1つの変更taskとして扱います。

1. 対象リポジトリで`git status`、適用中の指示、既存の`AGENTS.md`、`.codex/`、`.agents/`、`docs/`、`.github/`、`.gitignore`をread-onlyで調査する。
2. `chore/adopt-development-harness`等の専用branchを作る。
3. このテンプレートは対象リポジトリ外の一時directoryへ取得し、対象リポジトリの`.git`やremoteを変更しない。
4. 衝突するfileごとに、既存内容を維持する部分、ハーネスから統合する契約、採用しない部分を計画へ記載し、承認を得る。
5. 承認後に`AGENTS.md`、`.agents/skills/`、`.codex/`、`docs/PROJECT.md`、`docs/tasks/`、`.github/pull_request_template.md`、validatorをfile単位で統合する。既存fileを無条件に上書きしない。
6. プロジェクト固有の`PROJECT.md`と初期taskを作り、`python3 scripts/check_harness.py --mode project`、対象プロジェクト固有のtest、独立reviewを実行する。

既存構成はプロジェクトごとに異なるため、自動コピー・自動マージするinstallerは提供しません。テンプレート更新も自動適用せず、必要な変更だけを新しいtaskとして取り込みます。

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
