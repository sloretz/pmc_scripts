# rosboss

`rosboss` is a CLI tool for ROS bosses (ROS release managers).

## Installation

```bash
pip install -e .
```

## Reference

Everything is a subcommand of `rosboss`.

### Announce a sync freeze

```bash
rosboss sync announce-freeze --rosdistro <distro> [--date YYYY-MM-DD]
```
Create Discourse announcements and Zulip chat messages for a ROS sync freeze.

### Announce a comleted sync

```bash
rosboss sync announce-sync --rosdistro <distro> [--date YYYY-MM-DD]
```
Create Discourse announcements and Zulip chat messages when a ROS sync is complete.

### Tag ros/rosdistro for a sync

```bash
rosboss sync tag-rosdistro --rosdistro <distro> [--date YYYY-MM-DD]
```
Create a tag on `ros/rosdistro` matching the last commit that changed the distribution file.

### Update ros2/ros2 ros2.repos for a sync

```bash
rosboss sync update-repos-file --rosdistro <distro> [--pin <repo=version> ...]
```
Update the `ros2.repos` file on the distribution-specific release branch (e.g., `{distro}-release`) with the latest release versions.
*Note:* You probably want to pin `ros2/system_tests` (e.g. `--pin ros2/system_tests=<commit_hash>`).
