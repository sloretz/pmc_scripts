import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

from rosboss.ui import console, display_and_interactive_copy, pretty_command


def add_subparser(subparser):
    parser = subparser.add_parser(
        "tag-rosdistro",
        help="Tag rosdistro repository at the last commit that changed a distribution file."
    )
    parser.add_argument(
        "--rosdistro",
        required=True,
        help="The name of the ROS distribution (e.g., lyrical, humble, rolling)."
    )
    parser.add_argument(
        "--date",
        help="The date to use for the tag (format: YYYY-MM-DD). If unspecified, current date is used."
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Disable interactive copy menu."
    )
    parser.set_defaults(func=main)
    return parser


def clone_repository():
    """Clone the rosdistro repository from GitHub into the current directory."""
    try:
        pretty_command(['git', 'clone', '-b', 'master', 'git@github.com:ros/rosdistro.git', '.'])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone rosdistro repository: {e}") from e


def print_last_commit_log(file_path):
    """Print the last commit log for the specified file path."""
    try:
        pretty_command(['git', 'log', '-n', '1', '--', file_path])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to show git log for {file_path}: {e}") from e


def get_last_commit_hash(file_path):
    """Retrieve the hash of the last commit modifying the specified file."""
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '1', '--format=format:%H', '--', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        commit_hash = result.stdout.strip()
        if not commit_hash:
            raise ValueError(f"Could not retrieve commit hash for {file_path}")
        return commit_hash
    except (subprocess.CalledProcessError, ValueError) as e:
        raise RuntimeError(f"Failed to retrieve commit hash: {e}") from e


def git_checkout(commit_hash):
    """Check out the repository to the specified commit hash."""
    try:
        pretty_command(['git', 'checkout', commit_hash])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check out commit {commit_hash}: {e}") from e


def git_tag(tag_name):
    """Create a git tag with the specified tag name."""
    try:
        pretty_command(['git', 'tag', tag_name])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create tag {tag_name}: {e}") from e


def main(args):
    rosdistro = args.rosdistro.lower()
    
    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).date().strftime('%Y-%m-%d')
    
    tag_name = f"{rosdistro}/{date_str}"
    
    repo_dir = tempfile.mkdtemp(prefix='rosdistro_')
    os.chdir(repo_dir)
    
    try:
        clone_repository()

        distribution_file = f"{rosdistro}/distribution.yaml"
        
        # Check if the distribution file exists in the repo
        if not os.path.exists(distribution_file):
            raise RuntimeError(f"Distribution file '{distribution_file}' does not exist in the repository.")

        print_last_commit_log(distribution_file)

        commit_hash = get_last_commit_hash(distribution_file)

        git_checkout(commit_hash)

        git_tag(tag_name)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    sections = [
        {"key": "1", "label": "ros/rosdistro Clone Directory", "content": repo_dir, "render_as": "text"},
        {"key": "2", "label": "Push Git Tag Command", "content": f"git push origin {tag_name}", "render_as": "text"},
    ]
    interactive = not getattr(args, "no_interactive", False)
    display_and_interactive_copy(sections, header_info="If this looks good, then run:", header_title="Next Steps", interactive=interactive)
