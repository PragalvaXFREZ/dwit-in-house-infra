Hardware: pve01 (8 GB), plus one 4 GB and one 2 GB machine.

Decision:
At idle, Proxmox alone used about 1.32 GiB of RAM. That leaves too little memory on the 4 GB and 2 GB machines for a cluster to be useful, so we dropped the cluster.

pve01 stays as a standalone Proxmox host for running VMs.
The 4 GB and 2 GB machines run Debian 13 directly, which is much lighter, for experimenting with other projects.

What we did:
Installed Debian 13 on the 4 GB and 2 GB machines.
Set up Tailscale on pve01 and confirmed remote SSH access.

Problem
Ethernet isn't working on either Debian machine. Until it is, we can't access the internet, assign static IPs, and install Tailscale on them.
