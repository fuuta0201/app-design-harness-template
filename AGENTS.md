# Repository instructions

このリポジトリは、Webサイト／Webアプリケーション開発の再利用可能なハーネステンプレートです。

## Source of truth

- 作業前に `docs/PROJECT.md` を読む。
- 背景、仕様、設計、phase、決定、未解決事項、現在地、task索引の正本は `docs/PROJECT.md` とする。
- taskごとのscope、計画、承認、受け入れ条件、検証証拠、review、handoffの正本は `docs/tasks/<ID>-<slug>.md` とする。
- 同じ情報を複数ファイルへ複製しない。補助文書が必要なら、理由・所有情報・パスを `docs/PROJECT.md` の補助資料台帳へ登録する。
- 実装変更で仕様・判断が変わる場合は `docs/PROJECT.md`、taskの進捗・検証結果が変わる場合はtask fileを同じ変更単位で更新する。

## Standard workflow

1. `git status`、適用される指示、`docs/PROJECT.md`、対象コードを読み、既存変更を保護する。
2. 対応する仕様IDとtask IDを特定し、`PROJECT.md` の索引からtask fileを読む。存在しなければ、実装前に `docs/tasks/TEMPLATE.md` から作成して索引へ追加する。
3. read-only調査後、task fileへscope、非目標、変更予定箇所、実装計画、検証、risk、owner review要否を書く。
4. 計画をオーナーへ提示して停止し、明示的なOKをtask fileへ記録してから `in_progress` にする。
5. 承認済みscope内は追加確認を挟まず、実装、test、修正、文書更新、独立reviewまで自動で進める。
6. リポジトリが定義するformat、lint、typecheck、unit、interaction、integration、E2E、build等から該当する検証を実行する。
7. 完了前に、会話履歴を継承しない別エージェントへ未commit差分の独立reviewを依頼する。
8. 指摘を解消して必要な検証を再実行し、task fileへ証拠を記録してから `done` にする。

詳細な進行には `.agents/skills/app-development-harness/SKILL.md`、独立レビューには `.agents/skills/independent-change-review/SKILL.md` を使う。

## Git and GitHub collaboration

- local repositoryの確認・branch・diff・commitには `git` を使用してよい。GitHub上のPR、comment、repository設定などには `gh` を使用してよい。
- commit message、code comment、PRのtitle／body／comment、documentationは日本語で記載する。固有名詞、識別子、command、API名は原表記を保ってよい。
- code commentはcodeから分かるwhatを言い換えず、制約、選択理由、直感に反する事情などのwhyを1〜2行で簡潔に書く。whyが不要ならcommentを追加しない。
- PRを作成・更新するときは必ず `.agents/skills/pull-request-workflow/SKILL.md` を使用し、概要、commitごとの実装内容、test内容、review観点を含む日本語本文を作る。
- `git commit`、`git push`、`gh pr create`／`edit`／`comment`／`merge`、`gh repo edit` など状態を変える操作は、承認済みtask scopeとは別に対象と影響を提示し、明示承認後に実行する。

## Specification-driven rules

- コードから推測した仕様と、承認済み仕様を混同しない。
- `ready` でないtask、またはplan approvalがないtaskを実装しない。ただし緊急修正は、理由・risk・暫定受け入れ条件・承認を先にtask fileへ記録すれば着手できる。
- 中央のタスク台帳で `in_progress` にするタスクは同時に1件とする。並行作業はそのタスク配下のsubtaskとして、担当範囲・ファイル所有権・統合条件を詳細欄に書く。
- 完了の主張には、観測したcommand結果または手動確認の証拠をtask fileへ残す。未実行、失敗、環境制約は隠さない。
- 仕様変更は既存タスクへ埋め込まず、仕様・受け入れ条件・影響タスクを先に更新する。

## Review gates

- 独立レビュー担当へ実装会話の要約、意図した答え、懸念点の誘導を渡さない。担当は `AGENTS.md`、`docs/PROJECT.md`、対象task file、コード、未commit差分、検証出力から自力で判断する。
- 独立レビュー担当は原則としてファイルを変更しない。重要度、根拠、該当箇所、再現／修正方向を報告する。
- 挙動、設定、公開API、データ、セキュリティ、受け入れ条件に影響する修正後は再レビューする。説明だけの修正は再レビューを省略できる。
- unit test／interaction testで受け入れ条件が十分に保証される変更は、オーナーレビューを必須にしない。その判断とテスト名をタスクへ記録する。
- 視覚品質、コンテンツ、ブランド、事業ルール、法務、費用、外部サービス、本番公開など、人の判断が残る変更はオーナーレビューを要求する。

## Safety and scope

- 技術スタックやデプロイ先をテンプレートから決め打ちしない。変更可能性のある技術情報は公式一次資料で確認する。
- シークレット値をコード、文書、ログへ残さない。変数名、用途、保管場所だけを記録する。
- 承認済みplanはcommit、push、deploy、外部サービス変更、データ移行、破壊操作、課金を自動では許可しない。対象・影響・backup／rollbackを確認し、別の明示承認後に実行する。
- ユーザーの既存変更を上書き、破棄、無関係に整形しない。
- 特定ツールの不足を理由に品質属性を省略しない。利用可能な手段へ置き換え、差分を記録する。

## Codex project configuration

- `.codex/config.toml` は承認後の通常実装を `workspace-write` sandbox内で進め、境界approvalをauto reviewへ送る。
- `.codex/rules/project.rules` はGit履歴・remote、GitHub操作、削除、package公開と代表的なwrapperを追加review対象にする。任意の子processを完全に捕捉する安全境界ではないため、外部操作の人間承認はこのruleだけに依存しない。
- Plan modeはconfigで強制されない。利用可能なsurfaceでは `/plan` を使い、利用できないsurfaceでも上記Plan gateを守る。
- `.codex` の変更はtrusted projectでのみ読み込まれ、変更後はCodexを再起動する。
