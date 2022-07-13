# CloudLinux Leapp Elevation

**Before doing anything, please read
[Leapp framework documentation](https://leapp.readthedocs.io/).**

## Running
Make sure your system is fully updated before starting the elevation process.

Download and execute the preparation script: https://raw.githubusercontent.com/prilr/leapp-repository/cloudlinux/utils/cl_elevate_prepare.sh

Start a preupgrade check. In the meanwhile, the Leapp utility creates a special /var/log/leapp/leapp-report.txt file that contains possible problems and recommended solutions. No rpm packages will be installed at this phase.

`sudo leapp preupgrade`

The preupgrade process may stall with the following message:
> Inhibitor: Newest installed kernel not in use

Make sure your system is running the latest kernel before proceeding with the upgrade. If you updated the system recently, a reboot may be sufficient to do so. Otherwise, edit your Grub configuration accordingly.

> NOTE: In certain configurations, Leapp generates `/var/log/leapp/answerfile` with true/false questions. Leapp utility requires answers to all these questions in order to proceed with the upgrade.

Once the preupgrade process completes, the results will be contained in `/var/log/leapp/leapp-report.txt` file.
It's advised to review the report and consider how the changes will affect your system.

Start an upgrade. You’ll be offered to reboot the system after this process is completed.

```bash
sudo leapp upgrade
sudo reboot
```

> NOTE: The upgrade process after the reboot may take a long time, up to 40-50 minutes, depending on the machine resources. If the machine remains unresponsive for more than 2 hours, assume the upgrade process failed during the after-reboot phase.
> If it's still possible to access the machine in some way, for example, through remote VNC access, the logs containing the information on what went wrong are located in this folder: `/var/log/leapp`

A new entry in GRUB called ELevate-Upgrade-Initramfs will appear. The system will be automatically booted into it. See how the update process goes in the console.

After reboot, login to the system and check how the migration went. Verify that the current OS is the one you need.

```bash
cat /etc/redhat-release
cat /etc/os-release
```

Check the leapp logs for .rpmnew configuration files that may have been created during the upgrade process. In some cases os-release or yum package files may not be replaced automatically, requiring the user to rename the .rpmnew files manually.

## How to gather debugging information and create issues
If you encounter an unresolvable issue during an attempt to perform the system upgrade, all relevant information will be placed by leapp in the folder `/var/log/leapp/`.

**You can pack all logs with this command:**

`# tar -czf leapp-logs.tgz /var/log/leapp /var/lib/leapp/leapp.db`

Then you may attach only the `leapp-logs.tgz` file.

When filing an issue, include:
- Steps to reproduce the issue
- *All files in /var/log/leapp*
- */var/lib/leapp/leapp.db*
- *journalctl*
- If you want, you can optionally send anything else would you like to provide (e.g. storage info)

GitHub issues are preferred:
	- Leapp repository (actors, common configuration): [https://github.com/prilr/leapp-repository/issues/new/choose](https://github.com/prilr/leapp-repository/issues/new/choose)
	- Leapp data (package actions, rpm repository list): [https://github.com/prilr/leapp-data/issues/new/choose](https://github.com/prilr/leapp-data/issues/new/choose)

## How to add simple changes (package migration (PES), repository changes)
If the changes you want to enact are limited to addition/replacement of package repositories or replacement of packages that have changed between versions, making changes to the project’s codebase isn’t requred.

### Packages
The Leapp upgrade process uses information from the AlmaLinux PES (Package Evolution System) to keep track of how packages change between the OS versions.
This data is located in `leapp-data/files/cloudlinux/pes-events.json` in repository and in `/etc/leapp/files/pes-events.json` on a system being upgraded.

To add new rules to the pes-events.json, add a new entry to the packageinfo array.

Required fields:
- action: what action to perform on the listed package
	- 1 - removed
	- 2 - deprecated
	- 3 - replaced
	- 4 - split
	- 5 - merged
	- 6 - moved
	- 7 - renamed
- arches: what system architectures the listed entry relates to
- id: entry ID, must be unique
- in_packageset: set of packages on the old system
- out_packageset: set of packages to switch to, empty if removed or deprecated
- initial_release: source OS release
- release: target OS release

Please refer to [PES contribution guide](https://wiki.almalinux.org/elevate/Contribution-guide.html) for additional information on entry fields.

### Repositories
To provide Leapp with the list of the package repositories that should be used during the upgrade process, add them into the file `/etc/leapp/files/leapp_upgrade_repositories.repo`.

> NOTE: The repositories listed in the file are only used during the process.
> If the repositories you want to enable on the upgraded system are associated with a package, you can simply install it during the upgrade.

However, your repository files aren’t associated with a package and you wish to automate their deployment, continue to the next section.

## How to add complex changes (custom actors for migration)
To perform any changes of arbitrary complexity during the migration process, add a component to the existing Leapp pipeline.

To begin, clone the code repository: https://github.com/prilr/leapp-repository
For instructions on how to deploy a development enviroment, refer to [Leapp framework documentation](https://leapp.readthedocs.io/en/latest/devenv-install.html).

Create an actor inside the cloudlinux leapp repository:

```bash
cd ./leapp-repository/repos/system_upgrade/cloudlinux
snactor new-actor testactor
```

Alternatively, you can [create your own repository](https://leapp.readthedocs.io/en/latest/create-repository.html) in the system_upgrade folder, if you wish to keep your actors separate from others. However, you’ll need to link all other repositories whose functions you will use.
The created subfolder will contain the main Python file of your new actor.

The actor’s main class has three fields of interest:
- consumes
- produces
- tags

consumes and produces defines the [data that the actor may receive or provide to other actors](https://leapp.readthedocs.io/en/latest/messaging.html).

Tags define the phase of the upgrade process during which the actor runs.
All actors also must be assigned the `IPUWorkflowTag` to mark them as a part of the in-place upgrade process.
The file `leapp-repository/repos/system_upgrade/common/workflows/inplace_upgrade.py` lists all phases of the elevation process.

### Submitting changes
Changes you want to submit upstream should be sent through pull requests to repositories https://github.com/prilr/leapp-repository and https://github.com/prilr/leapp-data.
The standard GitHub contribution process applies - fork the repository, make your changes inside of it, then submit the pull request to be reviewed.

### Example
Suppose you would like to create an actor to copy a pre-supplied repository file into the upgraded CloudLinux system’s /etc/yum.repos.d.

First, you would create the new actor:
`cd ./leapp-repository/repos/system_upgrade/cloudlinux snactor new-actor addcustomrepositories`

Since you'd want to run this actor after the upgrade has successfully completed, you’d use the FirstBootPhase tag in its tags field.

```python
	tags = (IPUWorkflowTag, FirstBootPhaseTag)
```

To ensure the actor only runs on CloudLinux systems, and not on any migration variant, we would check the release name by importing the corresponding function from leapp API:

```python
from leapp.libraries.common.config import version

	def process(self):
					# We only want to run this actor on CloudLinux systems.
					# current_version returns a tuple (release_name, version_value).
					if (version.current_version()[0] == "cloudlinux"):
									copy_custom_repo_files()
```

Files that are accessible by all actors in the repository should be placed into the files/ subdirectory. For cloudlinux leapp repository, that directory has the path leapp-repository/repos/system_upgrade/cloudlinux/files.

Create the subfolder `custom-repos` to place repo files into, then complete the actor’s code:

```python
import os
import os.path
import shutil

from leapp.libraries.stdlib import api

CUSTOM_REPOS_FOLDER = 'custom-repos'
REPO_ROOT_PATH = "/etc/yum.repos.d"

def copy_custom_repo_files():
		custom_repo_dir = api.get_common_folder_path(CUSTOM_REPOS_FOLDER)

		for repofile in os.listdir(custom_repo_dir):
				full_repo_path = os.path.join(custom_repo_dir, repofile)
				shutil.copy(full_repo_path, REPO_ROOT_PATH)
```

Refer to existing actors and [Leapp documentation](https://leapp.readthedocs.io/) to use more complex functionality in your actors.
