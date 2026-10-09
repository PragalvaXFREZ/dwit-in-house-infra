# 5. Run on our infrastructure

## Goal

Move working checks to a machine we manage and understand what that exposes.

This is an instructor-led lab after labs 1–4. Do not attach a runner to this public repository or install it on the Proxmox host.

## Before registration

The instructor prepares:
- A separate private teaching repository with access limited to the lab participants.
- A disposable VM with a dedicated non-root runner user and no sudo privileges.
- Network restrictions blocking access to Proxmox, SSH on other hosts, the tailnet and other management services. Keep only the connectivity needed for GitHub and dependencies.
- No infrastructure credentials, SSH keys, mounted host directories or Docker socket.
- A clean snapshot or rebuild procedure.

Private visibility does not make participant code trusted. Review all code that will execute, including tests, dependency files and imported modules—not only workflow YAML.

Read GitHub's [self-hosted runner security guidance](https://docs.github.com/en/actions/reference/security/secure-use#hardening-for-self-hosted-runners) and [runner setup instructions](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners) before proceeding.

## Build

1. Copy the working demo and workflow into the private teaching repository. Restrict who can change or dispatch its workflow. Use a manual `workflow_dispatch` trigger for this supervised exercise; remove automatic push/PR triggers from this copy.
2. Review the exact commit and dependencies with the instructor. Freeze changes during the run. Manual dispatch is not itself a trust boundary.
3. From repository Settings → Actions → Runners, follow GitHub's generated registration commands on the VM as the runner user. Keep registration tokens out of Git, notes and screenshots.
4. Give it a distinct label such as `ci-lab`. Target `[self-hosted, linux, ci-lab]`, verify Python and virtual-environment support, and run one job at a time.
5. Dispatch the reviewed workflow, inspect its logs and artifact, then remove the runner registration and destroy/rebuild the VM before reusing it for different students' code.

Keep read-only token permissions, action SHA pins and the timeout from lab 4. Labels select a runner; they do not authorize workloads. A timeout also does not clean up a compromised machine.

## Think through approval

Explain the difference between:
- Reviewing a PR before merging.
- Approving a workflow run.
- Allowing particular third-party actions.
- Restricting which repositories/workflows may use a runner.

These controls are not interchangeable. Availability of finer runner controls depends on account type and plan. Approval does not sandbox code or clean up persistence left by a previous job.

## Your challenge

On paper, trace what could happen if a test reads files from the runner or makes a network request. Which actual VM, credential and network controls limit the damage? Do not test against college services.

## Done when

The same checks run on the VM, you can identify that runner in the logs, and the instructor verifies registration removal and VM cleanup.
