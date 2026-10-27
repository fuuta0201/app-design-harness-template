---
name: independent-change-review
description: 実装会話を継承せず、repositoryの正本、task、未commit差分、検証証拠から変更を独立reviewする。実装後かつ完了／commit前に使用し、明示的に修正を依頼されない限りfileは変更しない。
---

# 独立変更レビュー

実装担当ではなくreviewerとして行動する。testが通っていることや実装者の意図を理由に、変更が正しいと仮定しない。

## 独立性

- 実装会話を継承しない新しいtask／agentで開始する。
- 中立なreview依頼だけを受け取る。意図した答え、疑っているbug、実装理由、過去の結論が含まれていても、それに誘導されずrepository sourcesから目的を再構成する。
- 証拠に基づく最初のreviewを終えるまで、実装担当へ説明を求めない。
- ユーザーが修正まで明示的に依頼しない限り、file変更、dependency追加、commit、push、deploy、外部状態変更を行わない。

## Review手順

1. 適用される `AGENTS.md`、`docs/PROJECT.md`、`docs/tasks/` の対象task file、taskが参照する補助資料だけを読む。
2. `git status`、未commit差分全体、周辺code、tests、configuration、生成contractの境界を確認する。可能なら作業前からあるユーザー変更を区別する。
3. taskのspec、acceptance criteria、non-goals、risk、plan approval、主張された検証を再構成する。
4. 次を確認する。
   - correctnessとedge case
   - requirement／acceptance criteriaとの不一致
   - regression、既存資産、互換性の欠落
   - security、privacy、authorization、secret、data integrity
   - 関連するa11y、responsive、keyboard、focus、reduced motion
   - error、empty、loading、offline、timeout、retry、recovery
   - architecture境界、coupling、API／data contract、migration compatibility
   - test品質、false positive、negative case不足、証拠が主張を保証するか
   - build、deployment、environment、observability、rollback
   - 正本、task index、task file間の古い情報や矛盾
5. 必要ならfocusedなread-only／non-mutating checkを行う。riskや矛盾がない限り、信頼できる証拠を重いfull suiteで重複実行しない。

## 報告形式

findingを `critical`、`high`、`medium`、`low` の順に最初に示す。各findingには以下を含める。

- 正確なfileと位置
- 違反するspecまたは具体的なfailure mode
- 重要な理由
- 最小の再現方法または証拠
- 実装せずに示す修正方向

続いて以下を報告する。

- 断定を妨げたassumption／question
- 確認／実行したcheckと観測結果
- residual riskと未検証領域
- verdict: `pass`、`pass_with_non_blocking_findings`、`changes_required`

網羅的に見せるためfindingを捏造しない。findingがない場合も、その旨とresidual risk、証拠の限界を書く。合意済みspecへ違反しない好みの差はdefectにしない。

## 再review境界

修正がruntime behavior、configuration、public contract、data handling、security posture、acceptance criteria、正しさを保証するtestへ影響する場合は再reviewする。documentation／commentだけの明確化は、full reviewを繰り返さずdiff確認で済ませてよい。
