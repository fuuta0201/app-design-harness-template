#!/usr/bin/env python3
"""repository harnessを変更せず検証する。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    ".gitignore",
    ".codex/config.toml",
    ".codex/rules/project.rules",
    "README.md",
    "AGENTS.md",
    "docs/PROJECT.md",
    "docs/tasks/README.md",
    "docs/tasks/TEMPLATE.md",
    "docs/tasks/T-000-harness-template.md",
    "docs/tasks/T-001-project-initialization.md",
    "docs/tasks/T-002-repository-collaboration-rules.md",
    ".agents/skills/app-development-harness/SKILL.md",
    ".agents/skills/app-development-harness/agents/openai.yaml",
    ".agents/skills/independent-change-review/SKILL.md",
    ".agents/skills/independent-change-review/agents/openai.yaml",
    ".agents/skills/pull-request-workflow/SKILL.md",
    ".agents/skills/pull-request-workflow/agents/openai.yaml",
    ".github/pull_request_template.md",
    "scripts/check_harness.py",
    "scripts/test_check_harness.py",
)

REQUIRED_HEADINGS = (
    "## 0. Current snapshot",
    "## 1. Background and problem",
    "## 2. Outcomes, scope, and success",
    "## 3. Users and journeys",
    "## 4. Requirements",
    "## 5. Constraints and external dependencies",
    "## 6. Existing-state inventory and preservation",
    "## 7. Technology decisions",
    "## 8. Architecture and contracts",
    "## 9. Experience and design system",
    "## 10. Verification strategy",
    "## 11. Delivery and operations",
    "## 12. Roadmap and task ledger",
    "## 13. Decision log",
    "## 14. Open questions and risks",
    "## 15. Task evidence and handoff",
    "## 16. Supplementary document registry",
)

VALID_TASK_STATUSES = {
    "planned",
    "ready",
    "in_progress",
    "in_review",
    "blocked",
    "done",
}

COMPLETE_VERIFICATION_RESULTS = {"pass", "passed", "success", "not_applicable"}
COMPLETE_REVIEW_VERDICTS = {"pass", "pass_with_non_blocking_findings"}

REQUIRED_PR_HEADINGS = (
    "## 概要",
    "## 実装内容",
    "## テスト内容",
    "## レビュー観点",
)

REQUIRED_TASK_HEADINGS = (
    "## 目的",
    "## Source context",
    "## Scope",
    "## Implementation plan",
    "## Approval gate",
    "## Acceptance criteria",
    "## Verification",
    "## Independent review",
    "## Owner review",
    "## Decisions and discoveries",
    "## Handoff",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--mode",
        choices=("template", "project"),
        default="project",
        help="Template permits placeholders; project rejects them.",
    )
    return parser.parse_args()


def section(project_text: str, start: str, end: str) -> str:
    lines = project_text.splitlines()
    try:
        start_index = lines.index(start) + 1
    except ValueError:
        return ""
    try:
        end_index = lines.index(end, start_index)
    except ValueError:
        end_index = len(lines)
    return "\n".join(lines[start_index:end_index])


def task_rows(project_text: str) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    ledger = section(project_text, "### 12.3 Tasks", "## 13. Decision log")
    in_index_table = False
    for line in ledger.splitlines():
        stripped = line.strip()
        if not in_index_table:
            if re.fullmatch(r"\|\s*ID\s*\|.*", stripped):
                in_index_table = True
            continue
        if not stripped.startswith("|"):
            break
        if re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", stripped):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"T-\d{3,}", cells[0]):
            task_path = cells[3].strip("`")
            rows.append((cells[0], cells[4], task_path, cells[5]))
    return rows


def registered_supplementary_files(project_text: str) -> set[str]:
    registry = project_text.split("## 16. Supplementary document registry", 1)
    if len(registry) != 2:
        return set()
    registered: set[str] = set()
    for line in registry[1].splitlines():
        if not line.lstrip().startswith("|"):
            continue
        first_cell = line.strip().strip("|").split("|", 1)[0].strip()
        match = re.fullmatch(r"`(docs/[^`|]+)`", first_cell)
        if match:
            registered.add(match.group(1))
    return registered


def table_data_rows(markdown: str) -> list[list[str]]:
    """Markdown tableからheaderとseparatorを除いたdata rowを返す。"""
    rows: list[list[str]] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and cells[0].lower() not in {"command / review", "項目"}:
            rows.append(cells)
    return rows


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if line.endswith((" ", "\t")):
                errors.append(f"trailing whitespace: {relative}:{line_number}")

    project_path = root / "docs/PROJECT.md"
    if project_path.is_file():
        project_text = project_path.read_text(encoding="utf-8")

        for heading in REQUIRED_HEADINGS:
            if not re.search(rf"^{re.escape(heading)}$", project_text, re.MULTILINE):
                errors.append(f"missing PROJECT heading: {heading}")

        placeholders = sorted(set(re.findall(r"\{\{[^{}]+\}\}", project_text)))
        if args.mode == "project" and placeholders:
            preview = ", ".join(placeholders[:5])
            suffix = " ..." if len(placeholders) > 5 else ""
            errors.append(f"unresolved project placeholders: {preview}{suffix}")
        if args.mode == "template" and not placeholders:
            warnings.append("template mode found no {{...}} placeholders")

        rows = task_rows(project_text)
        if not rows:
            errors.append("no task rows found in section 12.3")
        ids = [task_id for task_id, _, _, _ in rows]
        duplicate_ids = sorted({task_id for task_id in ids if ids.count(task_id) > 1})
        if duplicate_ids:
            errors.append(f"duplicate task IDs: {', '.join(duplicate_ids)}")

        invalid_statuses = sorted(
            {status for _, status, _, _ in rows if status not in VALID_TASK_STATUSES}
        )
        if invalid_statuses:
            errors.append(f"invalid task statuses: {', '.join(invalid_statuses)}")

        active = [task_id for task_id, status, _, _ in rows if status == "in_progress"]
        if len(active) > 1:
            errors.append(
                "multiple in_progress tasks without machine-verifiable ownership: "
                + ", ".join(active)
            )

        indexed_task_paths: set[str] = set()
        indexed_statuses = {task_id: status for task_id, status, _, _ in rows}
        for task_id, status, relative, index_owner in rows:
            path_match = re.fullmatch(
                r"docs/tasks/(T-\d{3,})-[a-z0-9-]+\.md", relative
            )
            if not path_match:
                errors.append(f"invalid task path for {task_id}: {relative}")
                continue
            if path_match.group(1) != task_id:
                errors.append(
                    f"task filename ID mismatch for {task_id}: {relative}"
                )
            indexed_task_paths.add(relative)
            task_path = root / relative
            if not task_path.is_file():
                errors.append(f"missing indexed task file: {relative}")
                continue
            task_text = task_path.read_text(encoding="utf-8")
            if not re.search(rf"^# {re.escape(task_id)}:", task_text, re.MULTILINE):
                errors.append(f"task heading ID mismatch: {relative}")
            for heading in REQUIRED_TASK_HEADINGS:
                if not re.search(rf"^{re.escape(heading)}$", task_text, re.MULTILINE):
                    errors.append(f"missing task heading in {relative}: {heading}")
            status_match = re.search(r"^\| Status \| ([^|]+) \|$", task_text, re.MULTILINE)
            if not status_match:
                errors.append(f"missing task status row: {relative}")
            elif status_match.group(1).strip() != status:
                errors.append(
                    f"task status mismatch for {task_id}: index={status}, "
                    f"file={status_match.group(1).strip()}"
                )
            owner_match = re.search(
                r"^\| Owner review \| (required|not_required)(?:\s|—|\|)",
                task_text,
                re.MULTILINE,
            )
            if not owner_match:
                errors.append(f"missing owner review classification: {relative}")
            elif owner_match.group(1) != index_owner:
                errors.append(
                    f"owner review mismatch for {task_id}: "
                    f"index={index_owner}, file={owner_match.group(1)}"
                )
            approval_match = re.search(
                r"^\| Plan approval \| ([^|]+) \|$", task_text, re.MULTILINE
            )
            if not approval_match:
                errors.append(f"missing plan approval row: {relative}")
            else:
                approval = approval_match.group(1).strip()
                if approval not in {"pending", "approved", "rejected"}:
                    errors.append(f"invalid plan approval state in {relative}: {approval}")
                elif status in {"in_progress", "in_review", "done"} and approval != "approved":
                    errors.append(f"active task lacks approved plan: {relative}")
            if status in {"in_progress", "in_review", "done"}:
                approval_gate = section(
                    task_text, "## Approval gate", "## Acceptance criteria"
                )
                if not re.search(
                    r"^- Plan presented: yes$", approval_gate, re.MULTILINE
                ):
                    errors.append(f"active task plan was not presented: {relative}")
                for field in ("Approved by", "Approved at", "Approval covers"):
                    metadata_match = re.search(
                        rf"^- {re.escape(field)}: ([^\n]+)$",
                        approval_gate,
                        re.MULTILINE,
                    )
                    value = metadata_match.group(1).strip() if metadata_match else ""
                    if (
                        not value
                        or value.lower() in {"pending", "not_run", "no", "-"}
                        or "{{" in value
                    ):
                        errors.append(
                            f"active task lacks {field.lower()} metadata: {relative}"
                        )
            if status == "done":
                acceptance = section(
                    task_text, "## Acceptance criteria", "## Verification"
                )
                criteria = re.findall(r"^- \[([ xX])\] ", acceptance, re.MULTILINE)
                if not criteria:
                    errors.append(f"done task has no acceptance criteria: {relative}")
                elif any(mark == " " for mark in criteria):
                    errors.append(
                        f"done task has unchecked acceptance criteria: {relative}"
                    )

                verification = section(
                    task_text, "## Verification", "## Independent review"
                )
                verification_rows = table_data_rows(verification)
                if not verification_rows:
                    errors.append(f"done task has no verification evidence: {relative}")
                else:
                    incomplete_results = [
                        row
                        for row in verification_rows
                        if len(row) < 2
                        or row[1].strip().lower() not in COMPLETE_VERIFICATION_RESULTS
                    ]
                    if incomplete_results:
                        errors.append(
                            f"done task has incomplete verification: {relative}"
                        )

                independent = section(
                    task_text, "## Independent review", "## Owner review"
                )
                verdict_match = re.search(
                    r"^- Verdict: ([^\n]+)$", independent, re.MULTILINE
                )
                verdict = verdict_match.group(1).strip() if verdict_match else ""
                if verdict not in COMPLETE_REVIEW_VERDICTS:
                    errors.append(
                        f"done task lacks completed independent review: {relative}"
                    )

                owner_review = section(
                    task_text, "## Owner review", "## Decisions and discoveries"
                )
                owner_result_match = re.search(
                    r"^- Result: ([^\n]+)$", owner_review, re.MULTILINE
                )
                owner_result = (
                    owner_result_match.group(1).strip()
                    if owner_result_match
                    else ""
                )
                required_owner_result = (
                    "approved" if index_owner == "required" else "not_required"
                )
                if owner_result != required_owner_result:
                    errors.append(
                        f"done task lacks completed owner review: {relative}"
                    )
            if args.mode == "project":
                task_placeholders = sorted(
                    set(re.findall(r"\{\{[^{}]+\}\}", task_text))
                )
                if task_placeholders:
                    errors.append(f"unresolved task placeholders: {relative}")

        task_directory = root / "docs/tasks"
        task_files = {
            path.relative_to(root).as_posix()
            for path in task_directory.glob("T-*.md")
            if path.is_file() and re.fullmatch(r"T-\d{3,}-[a-z0-9-]+\.md", path.name)
        }
        unindexed_tasks = sorted(task_files - indexed_task_paths)
        if unindexed_tasks:
            errors.append("unindexed task files: " + ", ".join(unindexed_tasks))

        task_support_files = {"docs/tasks/README.md", "docs/tasks/TEMPLATE.md"}
        all_task_files = {
            path.relative_to(root).as_posix()
            for path in task_directory.rglob("*")
            if path.is_file()
        }
        unexpected_task_files = sorted(
            all_task_files - indexed_task_paths - task_support_files
        )
        if unexpected_task_files:
            errors.append(
                "unexpected files in docs/tasks: " + ", ".join(unexpected_task_files)
            )

        if (root / "tasks").exists():
            errors.append("legacy task directory remains: tasks")

        snapshot = section(
            project_text, "## 0. Current snapshot", "## 1. Background and problem"
        )
        for task_id, snapshot_status in re.findall(
            r"`(T-\d{3,})`（(planned|ready|in_progress|in_review|blocked|done)）",
            snapshot,
        ):
            indexed_status = indexed_statuses.get(task_id)
            if indexed_status is None:
                errors.append(f"current snapshot references unknown task: {task_id}")
            elif indexed_status != snapshot_status:
                errors.append(
                    f"current snapshot status mismatch for {task_id}: "
                    f"index={indexed_status}, snapshot={snapshot_status}"
                )

        supplementary_files = {
            path.relative_to(root).as_posix()
            for path in (root / "docs").rglob("*")
            if path.is_file()
            and path != project_path
            and task_directory not in path.parents
        }
        unregistered = sorted(
            supplementary_files - registered_supplementary_files(project_text)
        )
        if unregistered:
            errors.append("unregistered supplementary files: " + ", ".join(unregistered))

    pr_template = root / ".github/pull_request_template.md"
    if pr_template.is_file():
        pr_template_text = pr_template.read_text(encoding="utf-8")
        for heading in REQUIRED_PR_HEADINGS:
            if not re.search(
                rf"^{re.escape(heading)}$", pr_template_text, re.MULTILINE
            ):
                errors.append(f"missing PR template heading: {heading}")

    for relative in (
        ".agents/skills/app-development-harness/SKILL.md",
        ".agents/skills/independent-change-review/SKILL.md",
        ".agents/skills/pull-request-workflow/SKILL.md",
    ):
        path = root / relative
        if path.is_file() and "[TODO:" in path.read_text(encoding="utf-8"):
            errors.append(f"unfinished skill scaffold: {relative}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Harness validation failed with {len(errors)} error(s).")
        return 1

    print(f"Harness validation passed ({args.mode} mode).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
