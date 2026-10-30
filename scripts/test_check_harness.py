#!/usr/bin/env python3
"""check_harness.pyの回帰test。"""

from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.check_harness import (
    REQUIRED_FILES,
    REQUIRED_HEADINGS,
    REQUIRED_PR_HEADINGS,
    REQUIRED_TASK_HEADINGS,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "scripts/check_harness.py"


class HarnessCheckTests(unittest.TestCase):
    def run_check(self, root: Path, mode: str = "template") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(CHECKER), "--root", str(root), "--mode", mode],
            check=False,
            capture_output=True,
            text=True,
        )

    def copy_harness(self, destination: Path) -> None:
        for relative in REQUIRED_FILES:
            source = REPOSITORY_ROOT / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def test_template_mode_accepts_template(self) -> None:
        result = self.run_check(REPOSITORY_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_mode_rejects_placeholders(self) -> None:
        result = self.run_check(REPOSITORY_ROOT, mode="project")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unresolved project placeholders", result.stdout)

    def test_project_mode_rejects_placeholders_in_indexed_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            project = root / "docs/PROJECT.md"
            project.write_text(
                re.sub(
                    r"\{\{[^{}]+\}\}", "未決定", project.read_text(encoding="utf-8")
                ),
                encoding="utf-8",
            )

            result = self.run_check(root, mode="project")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "unresolved task placeholders: docs/tasks/T-001-project-initialization.md",
                result.stdout,
            )

    def test_each_required_heading_is_enforced(self) -> None:
        for heading in REQUIRED_HEADINGS:
            with self.subTest(heading=heading), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                project = root / "docs/PROJECT.md"
                project.write_text(
                    project.read_text(encoding="utf-8").replace(heading, f"{heading} removed", 1),
                    encoding="utf-8",
                )

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"missing PROJECT heading: {heading}", result.stdout)

    def test_each_required_file_is_enforced(self) -> None:
        for relative in REQUIRED_FILES:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                (root / relative).unlink()

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"missing required file: {relative}", result.stdout)

    def test_each_required_pr_heading_is_enforced(self) -> None:
        for heading in REQUIRED_PR_HEADINGS:
            with self.subTest(heading=heading), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                template = root / ".github/pull_request_template.md"
                template.write_text(
                    template.read_text(encoding="utf-8").replace(
                        heading, f"{heading} removed", 1
                    ),
                    encoding="utf-8",
                )

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"missing PR template heading: {heading}", result.stdout)

    def test_legacy_root_task_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            legacy = root / "tasks/T-999-legacy.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("# legacy\n", encoding="utf-8")

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("legacy task directory remains: tasks", result.stdout)

    def test_unexpected_file_in_docs_tasks_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            unexpected = root / "docs/tasks/NOTES.md"
            unexpected.write_text("# notes\n", encoding="utf-8")

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unexpected files in docs/tasks: docs/tasks/NOTES.md", result.stdout)

    def test_nested_unregistered_file_is_rejected_regardless_of_extension(self) -> None:
        for relative in (
            "docs/research/UNREGISTERED.md",
            "docs/research/result.txt",
        ):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                extra = root / relative
                extra.parent.mkdir(parents=True)
                extra.write_text("Unregistered\n", encoding="utf-8")

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(relative, result.stdout)

    def test_registered_nested_file_is_accepted_regardless_of_extension(self) -> None:
        for relative in (
            "docs/research/REGISTERED.md",
            "docs/research/result.txt",
        ):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                extra = root / relative
                extra.parent.mkdir(parents=True)
                extra.write_text("Registered\n", encoding="utf-8")
                project = root / "docs/PROJECT.md"
                project.write_text(
                    project.read_text(encoding="utf-8").replace(
                        "| - | - | 現在は補助文書なし | - | - |",
                        f"| `{relative}` | 調査記録 | 長大なため | 調査更新時 | active |",
                    ),
                    encoding="utf-8",
                )

                result = self.run_check(root)

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_trailing_whitespace_in_required_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            readme = root / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8") + "trailing space \n",
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("trailing whitespace: README.md", result.stdout)

    def test_invalid_task_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            project = root / "docs/PROJECT.md"
            project.write_text(
                project.read_text(encoding="utf-8").replace(
                    "| T-001 | P0 | プロジェクト制御文書を初期化する | `docs/tasks/T-001-project-initialization.md` | ready | required |",
                    "| T-001 | P0 | プロジェクト制御文書を初期化する | `docs/tasks/T-001-project-initialization.md` | unknown | required |",
                ),
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid task statuses: unknown", result.stdout)

    def test_task_shaped_row_in_task_detail_does_not_mask_empty_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            project = root / "docs/PROJECT.md"
            project_text = project.read_text(encoding="utf-8")
            ledger_start = project_text.index("### 12.3 Tasks")
            ledger_end = project_text.index("## 13. Decision log")
            ledger = project_text[ledger_start:ledger_end]
            ledger = "\n".join(
                line for line in ledger.splitlines() if not line.startswith("| T-")
            )
            detail_row = (
                "| T-999 | P0 | outside | `docs/tasks/T-999-outside.md` | ready | not required |\n\n"
            )
            project.write_text(
                project_text[:ledger_start]
                + ledger.replace("#### T-000", detail_row + "#### T-000", 1)
                + project_text[ledger_end:],
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no task rows found in section 12.3", result.stdout)

    def test_index_and_task_file_status_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            task = root / "docs/tasks/T-001-project-initialization.md"
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "| Status | ready |", "| Status | blocked |", 1
                ),
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task status mismatch for T-001", result.stdout)

    def test_each_required_task_heading_is_enforced(self) -> None:
        for heading in REQUIRED_TASK_HEADINGS:
            with self.subTest(heading=heading), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                task = root / "docs/tasks/T-001-project-initialization.md"
                task.write_text(
                    task.read_text(encoding="utf-8").replace(
                        heading, f"{heading} removed", 1
                    ),
                    encoding="utf-8",
                )

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"missing task heading in docs/tasks/T-001", result.stdout)

    def test_owner_review_classification_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            task = root / "docs/tasks/T-001-project-initialization.md"
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "| Owner review | required —", "| Owner review | not_required —", 1
                ),
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("owner review mismatch for T-001", result.stdout)

    def test_task_filename_id_must_match_ledger_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            project = root / "docs/PROJECT.md"
            project.write_text(
                project.read_text(encoding="utf-8").replace(
                    "| T-001 | P0 | プロジェクト制御文書を初期化する |",
                    "| T-999 | P0 | プロジェクト制御文書を初期化する |",
                    1,
                ),
                encoding="utf-8",
            )
            task = root / "docs/tasks/T-001-project-initialization.md"
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "# T-001:", "# T-999:", 1
                ),
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task filename ID mismatch for T-999", result.stdout)

    def test_active_task_requires_explicit_approved_plan(self) -> None:
        for approval in ("no", "rejected", ""):
            with self.subTest(approval=approval), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                task = root / "docs/tasks/T-000-harness-template.md"
                task.write_text(
                    task.read_text(encoding="utf-8").replace(
                        "| Plan approval | approved |",
                        f"| Plan approval | {approval} |",
                        1,
                    ),
                    encoding="utf-8",
                )

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                expected = {
                    "": "missing plan approval row",
                    "no": "invalid plan approval state",
                    "rejected": "approved plan",
                }[approval]
                self.assertIn(expected, result.stdout)

    def test_active_task_requires_complete_plan_approval_evidence(self) -> None:
        mutations = {
            "- Approved by: project owner": (
                "- Approved by: pending",
                "active task lacks approved by metadata",
            ),
            "- Approved at: 2026-10-25 / revised 2026-10-26": (
                "- Approved at: pending",
                "active task lacks approved at metadata",
            ),
            "- Plan presented: yes": (
                "- Plan presented: no",
                "active task plan was not presented",
            ),
            "- Approval covers: repository-local harness artifactsの作成と今回指定の再構成": (
                "- Approval covers: pending",
                "active task lacks approval covers metadata",
            ),
        }
        for original, (replacement, expected) in mutations.items():
            with self.subTest(original=original), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                task = root / "docs/tasks/T-000-harness-template.md"
                task.write_text(
                    task.read_text(encoding="utf-8").replace(
                        original, replacement, 1
                    ),
                    encoding="utf-8",
                )

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout)

    def test_unindexed_task_file_is_rejected(self) -> None:
        for filename in ("T-999-unindexed.md", "T-1000-unindexed.md"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.copy_harness(root)
                extra = root / f"docs/tasks/{filename}"
                extra.write_text("# Unindexed\n", encoding="utf-8")

                result = self.run_check(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"unindexed task files: docs/tasks/{filename}", result.stdout)

    def test_done_task_requires_completed_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            task = root / "docs/tasks/T-000-harness-template.md"
            task.write_text(
                task.read_text(encoding="utf-8")
                .replace("- [x] owner reviewが完了する。", "- [ ] owner reviewが完了する。", 1)
                .replace("- Verdict: pass", "- Verdict: pending", 1)
                .replace("- Result: approved", "- Result: pending", 1),
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("done task has unchecked acceptance criteria", result.stdout)
            self.assertIn("done task lacks completed independent review", result.stdout)
            self.assertIn("done task lacks completed owner review", result.stdout)

    def test_current_snapshot_status_must_match_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            project = root / "docs/PROJECT.md"
            project.write_text(
                project.read_text(encoding="utf-8").replace(
                    "| 実行中タスク | なし |", "| 実行中タスク | `T-000`（in_review） |", 1
                ),
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("current snapshot status mismatch for T-000", result.stdout)

    def test_done_task_rejects_incomplete_verification_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_harness(root)
            project = root / "docs/PROJECT.md"
            project.write_text(
                project.read_text(encoding="utf-8")
                .replace("`T-000`（in_review）", "`T-000`（done）", 1)
                .replace(
                    "| T-000 | P0 | 再利用可能な開発ハーネス基盤を定義する | `docs/tasks/T-000-harness-template.md` | in_review | required |",
                    "| T-000 | P0 | 再利用可能な開発ハーネス基盤を定義する | `docs/tasks/T-000-harness-template.md` | done | required |",
                    1,
                ),
                encoding="utf-8",
            )
            task = root / "docs/tasks/T-000-harness-template.md"
            task.write_text(
                task.read_text(encoding="utf-8")
                .replace("| Status | in_review |", "| Status | done |", 1)
                .replace("- [ ] 独立reviewがpassする。", "- [x] 独立reviewがpassする。", 1)
                .replace("- [ ] owner reviewが完了する。", "- [x] owner reviewが完了する。", 1)
                .replace("| `python3 -m unittest scripts/test_check_harness.py` | pass |", "| `python3 -m unittest scripts/test_check_harness.py` | not_run |", 1)
                .replace("- Verdict: pending after requested restructuring", "- Verdict: pass", 1)
                .replace("- Result: pending", "- Result: approved", 1),
                encoding="utf-8",
            )

            result = self.run_check(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("done task has incomplete verification", result.stdout)


if __name__ == "__main__":
    unittest.main()
