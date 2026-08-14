import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
from typing import Any

from agent_ros2_gbp_github_org.categories import (
    IssueCategory,
    NewReleaseRepository,
    NewReleaseTeam,
    UpdateReleaseTeamMembership,
    UnknownCategory,
)
from agent_ros2_gbp_github_org.categorize import categorize_issue
from agent_ros2_gbp_github_org.planner import TerraformConfigPlanner


async def _run(
    path_to_ros2_gbp_github_org: Path,
    issue_data: dict[str, Any] | None = None,
) -> None:
    if issue_data is None:
        print("Error: No issue data provided.", file=sys.stderr)
        sys.exit(1)

    category = categorize_issue(issue_data)
    if category == UnknownCategory:
        print(f"Error: Issue category '{category}' is not supported.", file=sys.stderr)
        sys.exit(1)

    planner = TerraformConfigPlanner(workspace=path_to_ros2_gbp_github_org)
    plan = await planner.plan(issue_data, category=category)
    print(plan)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI tool for agent_ros2-gbp-github-org."
    )
    parser.add_argument(
        "--path-to-ros2-gbp-github-org",
        type=Path,
        required=True,
        help="Path to a git clone of https://github.com/ros2-gbp/ros2-gbp-github-org/",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--issue-json",
        type=Path,
        default=None,
        help="Used to load eval issues instead of fetching them from github.",
    )
    group.add_argument(
        "--issue",
        type=str,
        default=None,
        help="Issue number or URL (e.g., 1107 or https://github.com/ros2-gbp/ros2-gbp-github-org/issues/1107).",
    )
    args = parser.parse_args()

    if args.issue is not None:
        raise NotImplementedError("Fetching issues via --issue is not implemented yet.")

    issue_data = None
    if args.issue_json is not None:
        with open(args.issue_json, encoding="utf-8") as f:
            issue_data = json.load(f)

    asyncio.run(_run(args.path_to_ros2_gbp_github_org, issue_data=issue_data))


if __name__ == "__main__":
    main()
