from modules.printProgressAuto.progressBar import printProgressBar
from modules.termcolor.termcolor import cprint
from subprocess import Popen, PIPE
from time import time
from csv import writer


"""
benchmark structure
for b in benchmark_*:
    b[0] = recommendation id number
    b[1] = Scored (1) [OR] Not Scored (0)
    b[2] = Server      Profile  -> Level 1 (1) [OR] Level 2 (2) [OR] N/A (0)
    b[3] = Workstation Profile  -> Level 1 (1) [OR] Level 2 (2) [OR] N/A (0)
    b[4] = explanation
"""
benchmark_ind = [
    ['1.1.1.1', 1, 1, 1, 'Ensure mounting of cramfs filesystems is disabled'],
    ['1.1.1.2', 1, 1, 1, 'Ensure mounting of freevxfs filesystems is disabled'],
    ['1.1.1.3', 1, 1, 1, 'Ensure mounting of jffs2 filesystems is disabled'],
    ['1.1.1.4', 1, 1, 1, 'Ensure mounting of hfs filesystems is disabled'],
    ['1.1.1.5', 1, 1, 1, 'Ensure mounting of hfsplus filesystems is disabled'],
    ['1.1.1.6', 1, 1, 1, 'Ensure mounting of squashfs filesystems is disabled'],
    ['1.1.1.7', 1, 1, 1, 'Ensure mounting of udf filesystems is disabled'],
    ['1.1.1.8', 0, 2, 2, 'Ensure mounting of FAT filesystems is limited'],
    ['1.1.2', 1, 1, 1, 'Ensure /tmp is configured'],
    ['1.1.3', 1, 1, 1, 'Ensure nodev option set on /tmp partition'],
    ['1.1.4', 1, 1, 1, 'Ensure nosuid option set on /tmp partition'],
    ['1.1.5', 1, 1, 1, 'Ensure noexec option set on /tmp partition'],
    ['1.1.6', 1, 2, 2, 'Ensure separate partition exists for /var'],
    ['1.1.7', 1, 2, 2, 'Ensure separate partition exists for /var/tmp'],
    ['1.1.8', 1, 1, 1, 'Ensure nodev option set on /var/tmp partition'],
    ['1.1.9', 1, 1, 1, 'Ensure nosuid option set on /var/tmp partition'],
    ['1.1.10', 1, 1, 1, 'Ensure noexec option set on /var/tmp partition'],
    ['1.1.11', 1, 2, 2, 'Ensure separate partition exists for /var/log'],
    ['1.1.12', 1, 2, 2, 'Ensure separate partition exists for /var/log/audit'],
    ['1.1.13', 1, 2, 2, 'Ensure separate partition exists for /home'],
    ['1.1.14', 1, 1, 1, 'Ensure nodev option set on /home partition'],
    ['1.1.15', 1, 1, 1, 'Ensure nodev option set on /dev/shm partition'],
    ['1.1.16', 1, 1, 1, 'Ensure nosuid option set on /dev/shm partition'],
    ['1.1.17', 1, 1, 1, 'Ensure noexec option set on /dev/shm partition'],
    ['1.1.18', 0, 1, 1, 'Ensure nodev option set on removable media partitions'],
    ['1.1.19', 0, 1, 1, 'Ensure nosuid option set on removable media partitions'],
    ['1.1.20', 0, 1, 1, 'Ensure noexec option set on removable media partitions'],
    ['1.1.21', 1, 1, 1, 'Ensure sticky bit is set on all world-writable directories'],
    ['1.1.22', 1, 1, 2, 'Disable Automounting'],
    ['1.1.23', 1, 1, 2, 'Disable USB Storage'],
    ['1.2.1', 0, 1, 1,
        'Ensure package manager repositories are configured (distro specific)'],
    ['1.2.2', 0, 1, 1, 'Ensure GPG keys are configured (distro specific)'],
    ['1.3.1', 1, 1, 1, 'Ensure AIDE is installed (distro specific)'],
    ['1.3.2', 1, 1, 1, 'Ensure filesystem integrity is regularly checked'],
    ['1.4.1', 1, 1, 1,
        'Ensure permissions on bootloader config are configured (bootloader specific)'],
    ['1.4.2', 1, 1, 1,
        'Ensure bootloader password is set (bootloader specific)'],
    ['1.4.3', 1, 1, 1, 'Ensure authentication required for single user mode'],
    ['1.4.4', 0, 1, 1,
        'Ensure interactive boot is not enabled (distro specific)'],
    ['1.5.1', 1, 1, 1, 'Ensure core dumps are restricted'],
    ['1.5.2', 1, 1, 1, 'Ensure XD/NX support is enabled'],
    ['1.5.3', 1, 1, 1,
        'Ensure address space layout randomization (ASLR) is enabled'],
    ['1.5.4', 1, 1, 1, 'Ensure prelink is disabled (distro specific)'],
    ['1.6.1.1', 1, 2, 2,
        'Ensure SELinux or AppArmor are installed (distro specific)'],
    ['1.6.2.1', 1, 2, 2, 'Ensure SELinux is not disabled in bootloader configuration'],
    ['1.6.2.2', 1, 2, 2, 'Ensure the SELinux state is enforcing'],
    ['1.6.2.3', 1, 2, 2, 'Ensure SELinux policy is configured'],
    ['1.6.2.4', 1, 2, 0,
        'Ensure SETroubleshoot is not installed (distro specific)'],
    ['1.6.2.5', 1, 2, 2,
        'Ensure the MCS Translation Service (mcstrans) is not installed (distro specific)'],
    ['1.6.2.6', 1, 2, 2, 'Ensure no unconfined daemons exist'],
    ['1.6.3.1', 1, 2, 2, 'Ensure AppArmor is not disabled in bootloader configuration'],
    ['1.6.3.2', 1, 2, 2, 'Ensure all AppArmor Profiles are enforcing'],
    ['1.7.1.1', 1, 1, 1, 'Ensure message of the day is configured properly'],
    ['1.7.1.2', 1, 1, 1, 'Ensure local login warning banner is configured properly'],
    ['1.7.1.3', 1, 1, 1, 'Ensure remote login warning banner is configured properly'],
    ['1.7.1.4', 1, 1, 1, 'Ensure permissions on /etc/motd are configured'],
    ['1.7.1.5', 1, 1, 1, 'Ensure permissions on /etc/issue are configured'],
    ['1.7.1.6', 1, 1, 1, 'Ensure permissions on /etc/issue.net are configured'],
    ['1.7.2', 1, 1, 1, 'Ensure GDM login banner is configured'],
    ['1.8', 0, 1, 1,
        'Ensure updates, patches, and additional security software are installed (distro specific)'],
    ['2.1.1', 1, 1, 1, 'Ensure chargen services are not enabled'],
    ['2.1.2', 1, 1, 1, 'Ensure daytime services are not enabled'],
    ['2.1.3', 1, 1, 1, 'Ensure discard services are not enabled'],
    ['2.1.4', 1, 1, 1, 'Ensure echo services are not enabled'],
    ['2.1.5', 1, 1, 1, 'Ensure time services are not enabled'],
    ['2.1.6', 1, 1, 1, 'Ensure rsh server is not enabled'],
    ['2.1.7', 1, 1, 1, 'Ensure talk server is not enabled'],
    ['2.1.8', 1, 1, 1, 'Ensure telnet server is not enabled'],
    ['2.1.9', 1, 1, 1, 'Ensure tftp server is not enabled'],
    ['2.1.10', 1, 1, 1, 'Ensure xinetd is not enabled'],
    ['2.2.1.1', 0, 1, 1,
        'Ensure time synchronization is in use (distro specific)'],
    ['2.2.1.2', 1, 1, 1, 'Ensure ntp is configured'],
    ['2.2.1.3', 1, 1, 1, 'Ensure chrony is configured'],
    ['2.2.1.4', 1, 1, 1, 'Ensure systemd-timesyncd is configured'],
    ['2.2.2', 1, 1, 0,
        'Ensure X Window System is not installed (distro specific)'],
    ['2.2.3', 1, 1, 1, 'Ensure Avahi Server is not enabled'],
    ['2.2.4', 1, 1, 2, 'Ensure CUPS is not enabled'],
    ['2.2.5', 1, 1, 1, 'Ensure DHCP Server is not enabled'],
    ['2.2.6', 1, 1, 1, 'Ensure LDAP server is not enabled'],
    ['2.2.7', 1, 1, 1, 'Ensure NFS and RPC are not enabled'],
    ['2.2.8', 1, 1, 1, 'Ensure DNS Server is not enabled'],
    ['2.2.9', 1, 1, 1, 'Ensure FTP Server is not enabled'],
    ['2.2.10', 1, 1, 1, 'Ensure HTTP server is not enabled'],
    ['2.2.11', 1, 1, 1, 'Ensure IMAP and POP3 server is not enabled'],
    ['2.2.12', 1, 1, 1, 'Ensure Samba is not enabled'],
    ['2.2.13', 1, 1, 1, 'Ensure HTTP Proxy Server is not enabled'],
    ['2.2.14', 1, 1, 1, 'Ensure SNMP Server is not enabled'],
    ['2.2.15', 1, 1, 1, 'Ensure mail transfer agent is configured for local-only mode'],
    ['2.2.16', 1, 1, 1, 'Ensure rsync service is not enabled'],
    ['2.2.17', 1, 1, 1, 'Ensure NIS Server is not enabled'],
    ['2.3.1', 1, 1, 1, 'Ensure NIS Client is not installed (distro specific)'],
    ['2.3.2', 1, 1, 1, 'Ensure rsh client is not installed (distro specific)'],
    ['2.3.3', 1, 1, 1,
        'Ensure talk client is not installed (distro specific)'],
    ['2.3.4', 1, 1, 1,
        'Ensure telnet client is not installed (distro specific)'],
    ['2.3.5', 1, 1, 1,
        'Ensure telnet client is not installed (distro specific)'],
    ['3.1.1', 1, 1, 1, 'Ensure IP forwarding is disabled'],
    ['3.1.2', 1, 1, 1, 'Ensure packet redirect sending is disabled'],
    ['3.2.1', 1, 1, 1, 'Ensure source routed packets are not accepted'],
    ['3.2.2', 1, 1, 1, 'Ensure ICMP redirects are not accepted'],
    ['3.2.3', 1, 1, 1, 'Ensure secure ICMP redirects are not accepted'],
    ['3.2.4', 1, 1, 1, 'Ensure suspicious packets are logged'],
    ['3.2.5', 1, 1, 1, 'Ensure broadcast ICMP requests are ignored'],
    ['3.2.6', 1, 1, 1, 'Ensure bogus ICMP responses are ignored'],
    ['3.2.7', 1, 1, 1, 'Ensure Reverse Path Filtering is enabled'],
    ['3.2.8', 1, 1, 1, 'Ensure TCP SYN Cookies is enabled'],
    ['3.2.9', 1, 1, 1, 'Ensure IPv6 router advertisements are not accepted'],
    ['3.3.1', 0, 1, 1, 'Ensure TCP Wrappers is installed (distro specific)'],
    ['3.3.2', 0, 1, 1, 'Ensure /etc/hosts.allow is configured'],
    ['3.3.3', 0, 1, 1, 'Ensure /etc/hosts.deny is configured'],
    ['3.3.4', 1, 1, 1, 'Ensure permissions on /etc/hosts.allow are configured'],
    ['3.3.5', 1, 1, 1, 'Ensure permissions on /etc/hosts.deny are configured'],
    ['3.4.1', 1, 2, 2, 'Ensure DCCP is disabled'],
    ['3.4.2', 1, 2, 2, 'Ensure SCTP is disabled'],
    ['3.4.3', 1, 2, 2, 'Ensure RDS is disabled'],
    ['3.4.4', 1, 2, 2, 'Ensure TIPC is disabled'],
]
benchmark_cen = [
    ['1.1.1.1', 1, 1, 1, 'Ensure mounting of cramfs filesystems is disabled'],
    ['1.1.1.2', 0, 2, 2, 'Ensure mounting of vFAT filesystems is limited'],
    ['1.1.1.3', 1, 1, 1, 'Ensure mounting of squashfs filesystems is disabled'],
    ['1.1.1.4', 1, 1, 1, 'Ensure mounting of udf filesystems is disabled'],
    ['1.1.2', 1, 1, 1, 'Ensure /tmp is configured'],
    ['1.1.3', 1, 1, 1, 'Ensure nodev option set on /tmp partition'],
    ['1.1.4', 1, 1, 1, 'Ensure nosuid option set on /tmp partition'],
    ['1.1.5', 1, 1, 1, 'Ensure noexec option set on /tmp partition'],
    ['1.1.6', 1, 2, 2, 'Ensure separate partition exists for /var'],
    ['1.1.7', 1, 2, 2, 'Ensure separate partition exists for /var/tmp'],
    ['1.1.8', 1, 1, 1, 'Ensure nodev option set on /var/tmp partition'],
    ['1.1.9', 1, 1, 1, 'Ensure nosuid option set on /var/tmp partition'],
    ['1.1.10', 1, 1, 1, 'Ensure noexec option set on /var/tmp partition'],
    ['1.1.11', 1, 2, 2, 'Ensure separate partition exists for /var/log'],
    ['1.1.12', 1, 2, 2, 'Ensure separate partition exists for /var/log/audit'],
    ['1.1.13', 1, 2, 2, 'Ensure separate partition exists for /home'],
    ['1.1.14', 1, 1, 1, 'Ensure nodev option set on /home partition'],
    ['1.1.15', 1, 1, 1, 'Ensure nodev option set on /dev/shm partition'],
    ['1.1.16', 1, 1, 1, 'Ensure nosuid option set on /dev/shm partition'],
    ['1.1.17', 1, 1, 1, 'Ensure noexec option set on /dev/shm partition'],
    ['1.1.21', 1, 1, 1, 'Ensure sticky bit is set on all world-writable directories'],
    ['1.1.22', 1, 1, 2, 'Disable Automounting'],
    ['1.1.23', 1, 1, 2, 'Disable USB Storage'],
]
benchmark_deb = [
    ['1.1.1.1', 1, 1, 1, 'Ensure mounting of freevxfs filesystems is disabled'],
    ['1.1.1.2', 1, 1, 1, 'Ensure mounting of jffs2 filesystems is disabled'],
    ['1.1.1.3', 1, 1, 1, 'Ensure mounting of hfs filesystems is disabled'],
    ['1.1.1.4', 1, 1, 1, 'Ensure mounting of hfsplus filesystems is disabled'],
    ['1.1.2', 1, 1, 1, 'Ensure /tmp is configured'],
    ['1.1.3', 1, 1, 1, 'Ensure nodev option set on /tmp partition'],
    ['1.1.4', 1, 1, 1, 'Ensure nosuid option set on /tmp partition'],
    ['1.1.5', 1, 1, 1, 'Ensure noexec option set on /tmp partition'],
    ['1.1.6', 1, 2, 2, 'Ensure separate partition exists for /var'],
    ['1.1.7', 1, 2, 2, 'Ensure separate partition exists for /var/tmp'],
    ['1.1.8', 1, 1, 1, 'Ensure nodev option set on /var/tmp partition'],
    ['1.1.9', 1, 1, 1, 'Ensure nosuid option set on /var/tmp partition'],
    ['1.1.10', 1, 1, 1, 'Ensure noexec option set on /var/tmp partition'],
    ['1.1.11', 1, 2, 2, 'Ensure separate partition exists for /var/log'],
    ['1.1.12', 1, 2, 2, 'Ensure separate partition exists for /var/log/audit'],
    ['1.1.13', 1, 2, 2, 'Ensure separate partition exists for /home'],
    ['1.1.14', 1, 1, 1, 'Ensure nodev option set on /home partition'],
    ['1.1.15', 1, 1, 1, 'Ensure nodev option set on /dev/shm partition'],
    ['1.1.16', 1, 1, 1, 'Ensure nosuid option set on /dev/shm partition'],
    ['1.1.17', 1, 1, 1, 'Ensure noexec option set on /dev/shm partition'],
    ['1.1.21', 1, 1, 1, 'Ensure sticky bit is set on all world-writable directories'],
    ['1.1.22', 1, 1, 2, 'Disable Automounting'],
]
benchmark_fed = [
    ['1.1.1.1', 1, 1, 1, 'Ensure mounting of cramfs filesystems is disabled'],
    ['1.1.1.2', 0, 2, 2, 'Ensure mounting of vFAT filesystems is limited'],
    ['1.1.1.3', 1, 1, 1, 'Ensure mounting of squashfs filesystems is disabled'],
    ['1.1.1.4', 1, 1, 1, 'Ensure mounting of udf filesystems is disabled'],
    ['1.1.2', 1, 1, 1, 'Ensure /tmp is configured'],
    ['1.1.3', 1, 1, 1, 'Ensure nodev option set on /tmp partition'],
    ['1.1.4', 1, 1, 1, 'Ensure nosuid option set on /tmp partition'],
    ['1.1.5', 1, 1, 1, 'Ensure noexec option set on /tmp partition'],
    ['1.1.6', 1, 2, 2, 'Ensure separate partition exists for /var'],
    ['1.1.7', 1, 2, 2, 'Ensure separate partition exists for /var/tmp'],
    ['1.1.8', 1, 1, 1, 'Ensure nodev option set on /var/tmp partition'],
    ['1.1.9', 1, 1, 1, 'Ensure nosuid option set on /var/tmp partition'],
    ['1.1.10', 1, 1, 1, 'Ensure noexec option set on /var/tmp partition'],
    ['1.1.11', 1, 2, 2, 'Ensure separate partition exists for /var/log'],
    ['1.1.12', 1, 2, 2, 'Ensure separate partition exists for /var/log/audit'],
    ['1.1.13', 1, 2, 2, 'Ensure separate partition exists for /home'],
    ['1.1.14', 1, 1, 1, 'Ensure nodev option set on /home partition'],
    ['1.1.15', 1, 1, 1, 'Ensure nodev option set on /dev/shm partition'],
    ['1.1.16', 1, 1, 1, 'Ensure nosuid option set on /dev/shm partition'],
    ['1.1.17', 1, 1, 1, 'Ensure noexec option set on /dev/shm partition'],
    ['1.1.21', 1, 1, 1, 'Ensure sticky bit is set on all world-writable directories'],
    ['1.1.22', 1, 1, 2, 'Disable Automounting'],
    ['1.1.23', 1, 1, 2, 'Disable USB Storage'],
]
benchmark_red = [
    ['1.1.1.1', 1, 1, 1, 'Ensure mounting of cramfs filesystems is disabled'],
    ['1.1.1.2', 0, 2, 2, 'Ensure mounting of vFAT filesystems is limited'],
    ['1.1.1.3', 1, 1, 1, 'Ensure mounting of squashfs filesystems is disabled'],
    ['1.1.1.4', 1, 1, 1, 'Ensure mounting of udf filesystems is disabled'],
    ['1.1.2', 1, 1, 1, 'Ensure /tmp is configured'],
    ['1.1.3', 1, 1, 1, 'Ensure nodev option set on /tmp partition'],
    ['1.1.4', 1, 1, 1, 'Ensure nosuid option set on /tmp partition'],
    ['1.1.5', 1, 1, 1, 'Ensure noexec option set on /tmp partition'],
    ['1.1.6', 1, 2, 2, 'Ensure separate partition exists for /var'],
    ['1.1.7', 1, 2, 2, 'Ensure separate partition exists for /var/tmp'],
    ['1.1.8', 1, 1, 1, 'Ensure nodev option set on /var/tmp partition'],
    ['1.1.9', 1, 1, 1, 'Ensure nosuid option set on /var/tmp partition'],
    ['1.1.10', 1, 1, 1, 'Ensure noexec option set on /var/tmp partition'],
    ['1.1.11', 1, 2, 2, 'Ensure separate partition exists for /var/log'],
    ['1.1.12', 1, 2, 2, 'Ensure separate partition exists for /var/log/audit'],
    ['1.1.13', 1, 2, 2, 'Ensure separate partition exists for /home'],
    ['1.1.14', 1, 1, 1, 'Ensure nodev option set on /home partition'],
    ['1.1.15', 1, 1, 1, 'Ensure nodev option set on /dev/shm partition'],
    ['1.1.16', 1, 1, 1, 'Ensure nosuid option set on /dev/shm partition'],
    ['1.1.17', 1, 1, 1, 'Ensure noexec option set on /dev/shm partition'],
    ['1.1.21', 1, 1, 1, 'Ensure sticky bit is set on all world-writable directories'],
    ['1.1.22', 1, 1, 2, 'Disable Automounting'],
    ['1.1.23', 1, 1, 2, 'Disable USB Storage'],
]
benchmark_sus = [
    ['1.1.1.1', 1, 1, 1, 'Ensure mounting of cramfs filesystems is disabled'],
    ['1.1.1.2', 1, 1, 1, 'Ensure mounting of freevxfs filesystems is disabled'],
    ['1.1.1.3', 1, 1, 1, 'Ensure mounting of jffs2 filesystems is disabled'],
    ['1.1.1.4', 1, 1, 1, 'Ensure mounting of hfs filesystems is disabled'],
    ['1.1.1.5', 1, 1, 1, 'Ensure mounting of hfsplus filesystems is disabled'],
    ['1.1.1.6', 1, 1, 1, 'Ensure mounting of squashfs filesystems is disabled'],
    ['1.1.1.7', 1, 1, 1, 'Ensure mounting of udf filesystems is disabled'],
    ['1.1.1.8', 1, 2, 2, 'Ensure mounting of FAT filesystems is disabled'],
    ['1.1.2', 1, 2, 2, 'Ensure /tmp is configured'],
    ['1.1.3', 1, 1, 1, 'Ensure nodev option set on /tmp partition'],
    ['1.1.4', 1, 1, 1, 'Ensure nosuid option set on /tmp partition'],
    ['1.1.5', 1, 1, 1, 'Ensure noexec option set on /tmp partition'],
    ['1.1.6', 1, 2, 2, 'Ensure separate partition exists for /var'],
    ['1.1.7', 1, 2, 2, 'Ensure separate partition exists for /var/tmp'],
    ['1.1.8', 1, 1, 1, 'Ensure nodev option set on /var/tmp partition'],
    ['1.1.9', 1, 1, 1, 'Ensure nosuid option set on /var/tmp partition'],
    ['1.1.10', 1, 1, 1, 'Ensure noexec option set on /var/tmp partition'],
    ['1.1.11', 1, 2, 2, 'Ensure separate partition exists for /var/log'],
    ['1.1.12', 1, 2, 2, 'Ensure separate partition exists for /var/log/audit'],
    ['1.1.13', 1, 2, 2, 'Ensure separate partition exists for /home'],
    ['1.1.14', 1, 1, 1, 'Ensure nodev option set on /home partition'],
    ['1.1.15', 1, 1, 1, 'Ensure nodev option set on /dev/shm partition'],
    ['1.1.16', 1, 1, 1, 'Ensure nosuid option set on /dev/shm partition'],
    ['1.1.17', 1, 1, 1, 'Ensure noexec option set on /dev/shm partition'],
    ['1.1.21', 1, 1, 1, 'Ensure sticky bit is set on all world-writable directories'],
    ['1.1.22', 1, 1, 2, 'Disable Automounting'],
]
benchmark_ubu = [
    ['1.1.1.1', 1, 1, 1, 'Ensure mounting of cramfs filesystems is disabled'],
    ['1.1.1.2', 1, 1, 1, 'Ensure mounting of freevxfs filesystems is disabled'],
    ['1.1.1.3', 1, 1, 1, 'Ensure mounting of jffs2 filesystems is disabled'],
    ['1.1.1.4', 1, 1, 1, 'Ensure mounting of hfs filesystems is disabled'],
    ['1.1.1.5', 1, 1, 1, 'Ensure mounting of hfsplus filesystems is disabled'],
    ['1.1.1.6', 1, 1, 1, 'Ensure mounting of squashfs filesystems is disabled'],
    ['1.1.1.7', 1, 1, 1, 'Ensure mounting of udf filesystems is disabled'],
    ['1.1.1.8', 0, 2, 2, 'Ensure mounting of FAT filesystems is limited'],
    ['1.1.2', 1, 1, 1, 'Ensure /tmp is configured'],
    ['1.1.3', 1, 1, 1, 'Ensure nodev option set on /tmp partition'],
    ['1.1.4', 1, 1, 1, 'Ensure nosuid option set on /tmp partition'],
    ['1.1.5', 1, 1, 1, 'Ensure noexec option set on /tmp partition'],
    ['1.1.6', 1, 2, 2, 'Ensure separate partition exists for /var'],
    ['1.1.7', 1, 2, 2, 'Ensure separate partition exists for /var/tmp'],
    ['1.1.8', 1, 1, 1, 'Ensure nodev option set on /var/tmp partition'],
    ['1.1.9', 1, 1, 1, 'Ensure nosuid option set on /var/tmp partition'],
    ['1.1.10', 1, 1, 1, 'Ensure noexec option set on /var/tmp partition'],
    ['1.1.11', 1, 2, 2, 'Ensure separate partition exists for /var/log'],
    ['1.1.12', 1, 2, 2, 'Ensure separate partition exists for /var/log/audit'],
    ['1.1.13', 1, 2, 2, 'Ensure separate partition exists for /home'],
    ['1.1.14', 1, 1, 1, 'Ensure nodev option set on /home partition'],
    ['1.1.15', 1, 1, 1, 'Ensure nodev option set on /dev/shm partition'],
    ['1.1.16', 1, 1, 1, 'Ensure nosuid option set on /dev/shm partition'],
    ['1.1.17', 1, 1, 1, 'Ensure noexec option set on /dev/shm partition'],
    ['1.1.21', 1, 1, 1, 'Ensure sticky bit is set on all world-writable directories'],
    ['1.1.22', 1, 1, 2, 'Disable Automounting'],
    ['1.1.23', 1, 1, 2, 'Disable USB Storage'],
]


def print_success(r, x, p): cprint(
    '{:<8}   {:<50}\t{:>4}'.format(r, x, p), 'green', attrs=['bold'])


def print_fail(r, x, p): cprint('{:<8}   {:<50}\t{:>4}'.format(
    r, x, p), 'red', attrs=['bold'])


def print_neutral(r, x, p): cprint('{:<8}   {:<50}\t{:>4}'.format(
    r, x, p), 'grey', attrs=['bold'])


# function to execute the check
def check(execute):
    execute = Popen(execute, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                    shell=True, executable='/bin/bash').communicate()
    execute = [e.decode('utf-8') for e in execute]
    return execute


"""
Definitions of Functions that perform independent checks against benchmarks
return_value[0] = result
return_value[1] = PASS/FAIL/CHEK
return_value[2] = success/error message
Goto line "156" in order to view definition of test()
"""


def _1_1_1_1_ind():
    return_value = list()
    success, error = check('modprobe -n -v cramfs')
    if 'insmod' in success:
        return_value.append('cramfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep cramfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('cramfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('cramfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('cramfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_2_ind():
    return_value = list()
    success, error = check('modprobe -n -v freevxfs')
    if 'insmod' in success:
        return_value.append('freevxfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep freevxfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('freevxfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('freevxfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('freevxfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_3_ind():
    return_value = list()
    success, error = check('modprobe -n -v jffs2')
    if 'insmod' in success:
        return_value.append('jffs2 can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep jffs2')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('jffs2 cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('jffs2 is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('jffs2 mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_4_ind():
    return_value = list()
    success, error = check('modprobe -n -v hfs')
    if 'insmod' in success:
        return_value.append('hfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_5_ind():
    return_value = list()
    success, error = check('modprobe -n -v hfsplus')
    if 'insmod' in success:
        return_value.append('hfsplus can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfsplus')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfsplus cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfsplus is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfsplus mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_6_ind():
    return_value = list()
    success, error = check('modprobe -n -v squashfs')
    if 'insmod' in success:
        return_value.append('squashfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep squashfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('squashfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('squashfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('squashfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_7_ind():
    return_value = list()
    success, error = check('modprobe -n -v udf')
    if 'insmod' in success:
        return_value.append('udf can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep udf')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('udf cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('udf is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('udf mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_8_ind():
    return_value = list()
    success, error = check('grep -i vfat /etc/fstab')
    if success:
        return_value.append('vfat is mounted')
        return_value.append('CHEK')
        return_value.append(success)
    else:
        success, error = check('modprobe -n -v vfat')
        if 'insmod' in success:
            return_value.append('vfat can be mounted')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            result_success = success
            result_error = error
            success, error = check('lsmod | grep vfat')
            if 'install /bin/true' in result_success or 'not found in directory' in result_error:
                if not success:
                    return_value.append('vfat cannot be mounted')
                    return_value.append('PASS')
                    return_value.append(
                        result_success if result_success else result_error)
                else:
                    return_value.append('vfat is mounted')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success if result_success else result_error + '\n' + success)
            else:
                return_value.append('vfat mount status undetermined')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_2_ind():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        return_value.append('/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('/tmp is not configured')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_3_ind():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nodev did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nodev is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_4_ind():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nosuid did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nosuid is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_5_ind():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v noexec did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('noexec is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_6_ind():
    return_value = list()
    success, error = check("mount | grep -E '\s/var\s'")
    if success:
        return_value.append('/var is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/var\s' did not return any result")
    return return_value


def _1_1_7_ind():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        return_value.append('/var/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/tmp is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/tmp did not return any result")
    return return_value


def _1_1_8_ind():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_9_ind():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_10_ind():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_11_ind():
    return_value = list()
    success, error = check('mount | grep /var/log')
    if success:
        return_value.append('/var/log is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/log did not return any result")
    return return_value


def _1_1_12_ind():
    return_value = list()
    success, error = check('mount | grep /var/log/audit')
    if success:
        return_value.append('/var/log/audit is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log/audit is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep /var/log/audit did not return any result")
    return return_value


def _1_1_13_ind():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        return_value.append('/home is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/home is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /home did not return any result")
    return return_value


def _1_1_14_ind():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        success, error = check("mount | grep -E '\s/home\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /home')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/home\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /home')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /home')
        return_value.append('FAIL')
        return_value.append(
            "/home does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_15_ind():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_16_ind():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nosuid is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_17_ind():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_18_ind():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nodev = [drive for drive in success.splitlines()
                 if 'nodev' not in drive]
        if not nodev:
            return_value.append('nodev is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nodev is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nodev" set\n'
            for n in nodev:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_19_ind():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nosuid = [drive for drive in success.splitlines()
                  if 'nosuid' not in drive]
        if not nosuid:
            return_value.append('nosuid is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nosuid is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nosuid" set\n'
            for n in nosuid:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_20_ind():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        noexec = [drive for drive in success.splitlines()
                  if 'noexec' not in drive]
        if not noexec:
            return_value.append('noexec is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('noexec is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "noexec" set\n'
            for n in noexec:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_21_ind():
    return_value = list()
    success, error = check(
        "df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null")
    if not success:
        return_value.append('sticky bit set on w-w directories')
        return_value.append('PASS')
        return_value.append(
            "running df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null confirms that all world writable directories have the sticky variable set")
    else:
        return_value.append('directories without sticky bit found')
        return_value.append('FAIL')
        return_value.append(
            'The following directories does not have their sticky bit set\n' + success)
    return return_value


def _1_1_22_ind():
    return_value = list()
    success, error = check('systemctl is-enabled autofs | grep enabled')
    if error:
        return_value.append('automounting could not be checked')
        return_value.append('PASS')
        return_value.append(error)
    else:
        if 'enabled' in success:
            return_value.append('automounting is enabled')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            return_value.append('automounting is disabled')
            return_value.append('PASS')
            return_value.append(success)
    return return_value


def _1_1_23_ind():
    return_value = list()
    success, error = check('modprobe -n -v usb-storage')
    if 'insmod' in success:
        return_value.append('usb-storage can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep usb-storage')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('usb-storage cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('usb-storage is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('usb-storage mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


# distro specific
def _1_2_1_ind():
    return_value = list()
    return_value.append('package configuration not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo apt-cache policy')
    if success:
        return_value.append('check configuration of repos')
        return_value.append('CHEK')
        return_value.append(
            'The following are the configuration of the package manager repositories\n' + success)
    else:
        return_value.append('package configuration not checked')
        return_value.append('CHEK')
        return_value.append(
            'sudo apt-cache policy did not return anything\n' + error)
    return return_value


# distro specific
def _1_2_2_ind():
    return_value = list()
    return_value.append('GPG keys source not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo apt-key list')
    if success:
        return_value.append('check GPG keys source')
        return_value.append('CHEK')
        return_value.append(
            'The following are the configuration of the GPG keys\n' + success)
    else:
        return_value.append('GPG keys not checked')
        return_value.append('CHEK')
        return_value.append(
            'sudo apt-key list did not return any keys\n' + error)
    return return_value


# distro specific
def _1_3_1_ind():
    return_value = list()
    return_value.append('AIDE not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s aide')
    if success:
        return_value.append('AIDE is installed')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('AIDE is not installed')
        return_value.append('FAIL')
        return_value.append('sudo dpkg -s aide returned\n' + error)
    return return_value


def _1_3_2_ind():
    return_value = list()
    success, error = check('sudo crontab -u root -l | grep aide')
    if success:
        result = success
        success, error = check('grep -r aide /etc/cron.* /etc/crontab')
        if success:
            result += '\nThe following cron jobs are scheduled\n' + success
            return_value.append('file integrity is checked')
            return_value.append('PASS')
            return_value.append(result)
        else:
            result += '\nNo cron jobs are scheduled for AIDE\n' + error
            return_value.append('file integrity is not checked')
            return_value.append('FAIL')
            return_value.append(result)
    else:
        return_value.append('No AIDE cron jobs scheduled')
        return_value.append('FAIL')
        return_value.append(
            'grep -r aide /etc/cron.* /etc/crontab returned the following\n' + success + '\n' + error)
    return return_value


# bootloader specific
def _1_4_1_ind():
    return_value = list()
    success, error = check('sudo stat /boot/grub*/grub.cfg | grep Access')
    if success:
        if 'Uid: (    0/    root)   Gid: (    0/    root)' in success:
            if '(0400/-r--------)' in success:
                return_value.append('bootloader permissions configured')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append('bootloader permits group and others')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('bootloader invalid uid and gid')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('grub config not found')
        return_value.append('CHEK')
        return_value.append(
            'stat /boot/grub*/grub.cfg | grep Access returned\n' + success + '\n' + error)
    return return_value


# bootloader specific
def _1_4_2_ind():
    return_value = list()
    success, error = check('sudo grep "^\s*password" /boot/grub/menu.lst')
    if success:
        return_value.append('bootloader password is set')
        return_value.append('PASS')
        return_value.append(success)
    else:
        success, error = check('sudo grep "^\s*password" /boot/grub/grub.cfg')
        if success:
            return_value.append('bootloader password is set')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('bootloader password not checked')
            return_value.append('CHEK')
            return_value.append(error)
    return return_value


def _1_4_3_ind():
    return_value = list()
    success, error = check('sudo grep ^root:[*\!]: /etc/shadow')
    if success:
        return_value.append('auth required for single user mode')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('auth not required for single user mode')
        return_value.append('FAIL')
        return_value.append(
            'sudo grep ^root:[*\!]: /etc/shadow returned the following\n' + error)
    return return_value


# distro specific
def _1_4_4_ind():
    return_value = list()
    success, error = check(
        'sudo grep "^PROMPT_FOR_CONFIRM=" /etc/sysconfig/boot')
    if 'PROMPT_FOR_CONFIRM="no"' in success:
        return_value.append('interactive boot disabled')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('interactive boot not checked')
        return_value.append('CHEK')
        return_value.append(
            'sudo grep "^PROMPT_FOR_CONFIRM=" /etc/sysconfig/boot returned the following\n' + success + '\n' + error)
    return return_value


def _1_5_1_ind():
    return_value = list()
    result_success = ''
    result_error = ''
    success, error = check(
        'grep "hard core" /etc/security/limits.conf /etc/security/limits.d/*')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    success, error = check('sysctl fs.suid_dumpable')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    success, error = check(
        'grep "fs\.suid_dumpable" /etc/sysctl.conf /etc/sysctl.d/*')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    if len(result_success.splitlines()) == 6:
        return_value.append('core dumps are restricted')
        return_value.append('PASS')
        return_value.append(result_success)
    else:
        return_value.append('core dumps not restricted')
        return_value.append('FAIL')
        return_value.append('Following are configured properly\n' + result_success +
                            '\n' + 'Following are configured improperly\n' + result_error)
    return return_value


def _1_5_2_ind():
    return_value = list()
    success, error = check("sudo journalctl | grep 'protection: active'")
    if success:
        return_value.append('XD/NX support is enabled')
        return_value.append('PASS')
        return_value.append(success)
    else:
        result_error = error
        success, error = check(
            "[[ -n $(grep noexec[0-9]*=off /proc/cmdline) || -z $(grep -E -i ' (pae|nx) ' /proc/cpuinfo) || -n $(grep '\sNX\s.*\sprotection:\s' /var/log/dmesg | grep -v active) ]] && echo \"NX Protection is not active\"")
        if not success:
            return_value.append('XD/NX support is enabled')
            return_value.append('PASS')
            return_value.append(error)
        else:
            return_value.append('XD/NX not enabled')
            return_value.append('FAIL')
            return_value.append(result_error + '\n' + success + '\n' + error)
    return return_value


def _1_5_3_ind():
    return_value = list()
    result_success = ''
    result_error = ''
    success, error = check('sysctl kernel.randomize_va_space')
    if '2' in success:
        result_success += success + '\n'
    else:
        result_error += success + '\n' + error + '\n'
    success, error = check(
        'grep "kernel\.randomize_va_space" /etc/sysctl.conf /etc/sysctl.d/*')
    if '2' in success:
        result_success += success + '\n'
    else:
        result_error += success + '\n' + error + '\n'
    if len(result_success.splitlines()) == 4:
        return_value.append('ASLR enabled')
        return_value.append('PASS')
        return_value.append(result_success)
    else:
        return_value.append('ASLR not enabled')
        return_value.append('FAIL')
        return_value.append('Following are configured properly\n' + result_success +
                            '\n' + 'Following are configured improperly\n' + result_error)
    return return_value


# distro specific
def _1_5_4_ind():
    return_value = list()
    return_value.append('prelink not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s prelink')
    if not success:
        return_value.append('prelink is not installed')
        return_value.append('PASS')
        return_value.append(error)
    else:
        return_value.append('prelink is installed')
        return_value.append('FAIL')
        return_value.append('sudo dpkg -s prelink returned\n' + success)
    return return_value


# distro specific
def _1_6_1_1_ind():
    return_value = list()
    return_value.append('SELinux or AppArmor not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s libselinux1')
    if success:
        return_value.append('SELinux is installed')
        return_value.append('PASS')
        return_value.append(success)
    else:
        result_error = error + '\n'
        success, error = check('sudo dpkg -s apparmor')
        if success:
            return_value.append('AppArmor is installed')
            return_value.append('PASS')
            return_value.append(success)
        else:
            result_error += error
            return_value.append('SELinux and AppArmor is not installed')
            return_value.append('FAIL')
            return_value.append(result_error)
    return return_value


def _1_6_2_1_ind():
    return_value = list()
    success, error = check('grep "^\s*kernel" /boot/grub/menu.lst')
    if success:
        if 'selinux=0' not in success and 'enforcing=0' not in success:
            return_value.append('SELinux not disabled boot-config')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('SELinux disabled boot-config')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        result_error = error + '\n'
        success, error = check('grep "^\s*linux" /boot/grub2/grub.cfg')
        if success:
            if 'selinux=0' not in success and 'enforcing=0' not in success:
                return_value.append('SELinux not disabled boot-config')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append('SELinux disabled boot-config')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('SELinux not checked')
            return_value.append('CHEK')
            return_value.append(result_error + error)
    return return_value


def _1_6_2_2_ind():
    return_value = list()
    result_success = ''
    result_error = ''
    success, error = check('grep SELINUX=enforcing /etc/selinux/config')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    success, error = check('sudo sestatus')
    if 'SELinux status: enabled' in success and 'Current mode: enforcing' in success and 'Mode from config file: enforcing' in success:
        result_success += success + '\n'
    else:
        result_error += success + '\n' + error + '\n'
    if len(result_success.splitlines()) == 4:
        return_value.append('SELinux state is enforcing')
        return_value.append('PASS')
        return_value.append(result_success)
    else:
        return_value.append('SELinux state is not enforcing')
        return_value.append('FAIL')
        return_value.append('Following are configured properly\n' + result_success +
                            '\n' + 'Following are configured improperly\n' + result_error)
    return return_value


def _1_6_2_3_ind():
    return_value = list()
    result_success = ''
    result_error = ''
    success, error = check('grep SELINUXTYPE= /etc/selinux/config')
    if 'SELINUXTYPE=targeted' in success or 'SELINUXTYPE=mls' in success:
        result_success += success + '\n'
    else:
        result_error += success + '\n' + error + '\n'
    success, error = check('sudo sestatus')
    if 'Policy from config file: targeted' in success or 'Policy from config file: mls' in success:
        result_success += success + '\n'
    else:
        result_error += success + '\n' + error + '\n'
    if len(result_success.splitlines()) == 4:
        return_value.append('SELinux policy is configured')
        return_value.append('PASS')
        return_value.append(result_success)
    else:
        return_value.append('SELinux policy is not configured')
        return_value.append('FAIL')
        return_value.append('Following are configured properly\n' + result_success +
                            '\n' + 'Following are configured improperly\n' + result_error)
    return return_value


# distro specific
def _1_6_2_4_ind():
    return_value = list()
    return_value.append('SETroubleshoot not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s setroubleshoot')
    if not success:
        return_value.append('SETroubleshoot is not installed')
        return_value.append('PASS')
        return_value.append(error)
    else:
        return_value.append('SETroubleshoot is installed')
        return_value.append('FAIL')
        return_value.append('sudo dpkg -s setroubleshoot returned\n' + success)
    return return_value


# distro specific
def _1_6_2_5_ind():
    return_value = list()
    return_value.append('mcstrans not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s mcstrans')
    if not success:
        return_value.append('mcstrans is not installed')
        return_value.append('PASS')
        return_value.append(error)
    else:
        return_value.append('mcstrans is installed')
        return_value.append('FAIL')
        return_value.append('sudo dpkg -s mcstrans returned\n' + success)
    return return_value


def _1_6_2_6_ind():
    return_value = list()
    success, error = check(
        "ps -eZ | grep -E \"initrc\" | grep -E -v -w \"tr|ps|grep|bash|awk\" | tr ':' ' ' | awk '{ print $NF }'")
    if not success:
        return_value.append('no unconfined daemons exist')
        return_value.append('PASS')
        return_value.append(
            "ps -eZ | grep -E \"initrc\" | grep -E -v -w \"tr|ps|grep|bash|awk\" | tr ':' ' ' | awk '{ print $NF }' returned nothing")
    else:
        return_value.append('unconfined daemons exist')
        return_value.append('FAIL')
        return_value.append(success)
    return return_value


def _1_6_3_1_ind():
    return_value = list()
    success, error = check('grep "^\s*kernel" /boot/grub/menu.lst')
    if success:
        if 'apparmor=0' not in success:
            return_value.append('AppArmor not disabled boot-config')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('SELinux disabled boot-config')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        result_error = error + '\n'
        success, error = check('grep "^\s*linux" /boot/grub/menu.lst')
        if success:
            if 'apparmor=0' not in success:
                return_value.append('AppArmor not disabled boot-config')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append('AppArmor disabled boot-config')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('AppArmor not checked')
            return_value.append('CHEK')
            return_value.append(result_error + error)
    return return_value


def _1_6_3_2_ind():
    return_value = list()
    success, error = check('sudo apparmor_status')
    if success:
        loaded_profiles = [
            p for p in success.splitlines() if 'profiles are loaded.' in p]
        complain_profiles = [p for p in success.splitlines(
        ) if 'profiles are in complain mode.' in p]
        unconfined_process = [
            p for p in success.splitlines() if 'processes are unconfined' in p]
        if loaded_profiles and not loaded_profiles[0].startswith('0'):
            if complain_profiles and complain_profiles[0].startswith('0'):
                if unconfined_process and unconfined_process[0].startswith('0'):
                    return_value.append('all AppArmor Profiles are enforcing')
                    return_value.append('PASS')
                    return_value.append(success)
                else:
                    return_value.append('AppArmor processes are confined')
                    return_value.append('FAIL')
                    return_value.append(success)
            else:
                return_value.append('AppArmor profiles are in complain mode')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('No AppArmor profiles are loaded')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('AppArmor status not found')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_7_1_1_ind():
    return_value = list()
    success, error = check('cat /etc/motd')
    if success:
        result_success = success
        success, error = check(
            "grep -E -i \"(\\v|\\r|\\m|\\s|$(grep '^ID=' /etc/os-release | cut -d= -f2 | sed -e 's/\"//g'))\" /etc/motd")
        if not success:
            return_value.append('motd is configured properly')
            return_value.append('PASS')
            return_value.append(
                'check if the message of the day matches site policy\n' + result_success)
        else:
            return_value.append('motd contains sensitive information')
            return_value.append('FAIL')
            return_value.append(
                'Following OS [or] patch level information were found in the message of the day\n' + result_success)
    else:
        return_value.append('no message of the day')
        return_value.append('CHEK')
        return_value.append(error)
    return return_value


def _1_7_1_2_ind():
    return_value = list()
    success, error = check('cat /etc/issue')
    if success:
        result_success = success
        success, error = check(
            "grep -E -i \"(\\v|\\r|\\m|\\s|$(grep '^ID=' /etc/os-release | cut -d= -f2 | sed -e 's/\"//g'))\" /etc/issue")
        if not success:
            return_value.append('login banner configured properly')
            return_value.append('PASS')
            return_value.append(
                'check if the local login warning banner matches site policy\n' + result_success)
        else:
            return_value.append('login banner contains sensitive info')
            return_value.append('FAIL')
            return_value.append(
                'Following OS [or] patch level information were found in the local login banner\n' + result_success)
    else:
        return_value.append('no local login warning banner')
        return_value.append('CHEK')
        return_value.append(error)
    return return_value


def _1_7_1_3_ind():
    return_value = list()
    success, error = check('cat /etc/issue.net')
    if success:
        result_success = success
        success, error = check(
            "grep -E -i \"(\\v|\\r|\\m|\\s|$(grep '^ID=' /etc/os-release | cut -d= -f2 | sed -e 's/\"//g'))\" /etc/issue.net")
        if not success:
            return_value.append('remote login banner configured properly')
            return_value.append('PASS')
            return_value.append(
                'check if the remote login warning banner matches site policy\n' + result_success)
        else:
            return_value.append('remote banner contains sensitive info')
            return_value.append('FAIL')
            return_value.append(
                'Following OS [or] patch level information were found in the remote login banner\n' + result_success)
    else:
        return_value.append('no remote login warning banner')
        return_value.append('CHEK')
        return_value.append(error)
    return return_value


def _1_7_1_4_ind():
    return_value = list()
    success, error = check('stat /etc/motd | grep Access')
    if success:
        if 'Uid: (    0/    root)   Gid: (    0/    root)' in success:
            if '(0644/-rw-r--r--)' in success:
                return_value.append('/etc/motd permissions configured')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append('/etc/motd permits group and others')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('/etc/motd invalid uid and gid')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('/etc/motd not found')
        return_value.append('CHEK')
        return_value.append(
            'stat /etc/motd | grep Access did not return anything\n' + error)
    return return_value


def _1_7_1_5_ind():
    return_value = list()
    success, error = check('stat /etc/issue | grep Access')
    if success:
        if 'Uid: (    0/    root)   Gid: (    0/    root)' in success:
            if '(0644/-rw-r--r--)' in success:
                return_value.append('/etc/issue permissions configured')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append('/etc/issue permits group and others')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('/etc/issue invalid uid and gid')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('/etc/issue not found')
        return_value.append('CHEK')
        return_value.append(
            'stat /etc/issue | grep Access did not return anything\n' + error)
    return return_value


def _1_7_1_6_ind():
    return_value = list()
    success, error = check('stat /etc/issue.net | grep Access')
    if success:
        if 'Uid: (    0/    root)   Gid: (    0/    root)' in success:
            if '(0644/-rw-r--r--)' in success:
                return_value.append('/etc/issue.net permissions configured')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append('/etc/issue.net permits group and others')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('/etc/issue.net invalid uid and gid')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('/etc/issue.net not found')
        return_value.append('CHEK')
        return_value.append(
            'stat /etc/issue.net | grep Access did not return anything\n' + error)
    return return_value


def _1_7_2_ind():
    return_value = list()
    success, error = check('cat /etc/gdm3/greeter.dconf-defaults')
    if success:
        result_success = success
        success, error = check(
            'cat /etc/gdm3/greeter.dconf-defaults | grep banner-message-')
        if success:
            if 'banner-message-enable=true' in success and not success.splitlines()[0].startswith('#'):
                if "banner-message-text='" in success and not success.splitlines()[1].startswith('#'):
                    return_value.append('GDM login banner is configured')
                    return_value.append('PASS')
                    return_value.append(result_success)
                else:
                    return_value.append('no GDM login banner message')
                    return_value.append('FAIL')
                    return_value.append(result_success)
            else:
                return_value.append('GDM banner message not enabled')
                return_value.append('FAIL')
                return_value.append(result_success)
        else:
            return_value.append('GDM login banner not configured')
            return_value.append('FAIL')
            return_value.append(result_success)
    else:
        return_value.append('GDM not found')
        return_value.append('CHEK')
        return_value.append(
            'cat /etc/gdm3/greeter.dconf-defaults did not return anything\n' + error)
    return return_value


def _1_8_ind():
    return_value = list()
    success, error = check('sudo apt-get -s upgrade')
    if success:
        if '0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.' in success:
            return_value.append('software installed properly')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('software packages need checking')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('software state not checked')
        return_value.append('CHEK')
        return_value.append(
            'sudo apt-get -s upgrade did not return anything\n' + error)
    return return_value


def _2_1_1_ind():
    return_value = list()
    success, error = check('grep -R "^chargen" /etc/inetd.*')
    if success:
        return_value.append('chargen services are enabled')
        return_value.append('FAIL')
        return_value.append(
            'grep -R "^chargen" /etc/inetd.* returned the following\n' + success)
    else:
        return_value.append('chargen is not present')
        return_value.append('PASS')
        return_value.append(
            'grep -R "^chargen" /etc/inetd.* returned the following\n' + error)
    return return_value


def _2_1_2_ind():
    return_value = list()
    success, error = check('grep -R "^daytime" /etc/inetd.*')
    if success:
        return_value.append('daytime services are enabled')
        return_value.append('FAIL')
        return_value.append(
            'grep -R "^daytime" /etc/inetd.* returned the following\n' + success)
    else:
        return_value.append('daytime is not present')
        return_value.append('PASS')
        return_value.append(
            'grep -R "^daytime" /etc/inetd.* returned the following\n' + error)
    return return_value


def _2_1_3_ind():
    return_value = list()
    success, error = check('grep -R "^discard" /etc/inetd.*')
    if success:
        return_value.append('discard services are enabled')
        return_value.append('FAIL')
        return_value.append(
            'grep -R "^discard" /etc/inetd.* returned the following\n' + success)
    else:
        return_value.append('discard is not present')
        return_value.append('PASS')
        return_value.append(
            'grep -R "^discard" /etc/inetd.* returned the following\n' + error)
    return return_value


def _2_1_4_ind():
    return_value = list()
    success, error = check('grep -R "^echo"/etc/inetd.*')
    if success:
        return_value.append('echo services are enabled')
        return_value.append('FAIL')
        return_value.append(
            'grep -R "^echo" /etc/inetd.* returned the following\n' + success)
    else:
        return_value.append('echo is not present')
        return_value.append('PASS')
        return_value.append(
            'grep -R "^echo" /etc/inetd.* returned the following\n' + error)
    return return_value


def _2_1_5_ind():
    return_value = list()
    success, error = check('grep -R "^time" /etc/inetd.*')
    if success:
        return_value.append('time services are enabled')
        return_value.append('FAIL')
        return_value.append(
            'grep -R "^time" /etc/inetd.* returned the following\n' + success)
    else:
        return_value.append('time is not present')
        return_value.append('PASS')
        return_value.append(
            'grep -R "^time" /etc/inetd.* returned the following\n' + error)
    return return_value


def _2_1_6_ind():
    return_value = list()
    result_success = ''
    result_error = ''
    success, error = check('grep -R "^shell" /etc/inetd.*')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    success, error = check('grep -R "^login" /etc/inetd.*')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    success, error = check('grep -R "^exec" /etc/inetd.*')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    if len(result_success):
        return_value.append('rsh services are enabled')
        return_value.append('FAIL')
        return_value.append(result_success + '\n' + result_error)
    else:
        return_value.append('rsh services not present')
        return_value.append('PASS')
        return_value.append(result_success + '\n' + result_error)
    return return_value


def _2_1_7_ind():
    return_value = list()
    result_success = ''
    result_error = ''
    success, error = check('grep -R "^talk" /etc/inetd.*')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    success, error = check('grep -R "^ntalk" /etc/inetd.*')
    if success:
        result_success += success + '\n'
    else:
        result_error += error + '\n'
    if len(result_success):
        return_value.append('talk server is enabled')
        return_value.append('FAIL')
        return_value.append(result_success + '\n' + result_error)
    else:
        return_value.append('talk server not present')
        return_value.append('PASS')
        return_value.append(result_success + '\n' + result_error)
    return return_value


def _2_1_8_ind():
    return_value = list()
    success, error = check('grep -R "^telnet" /etc/inetd.*')
    if success:
        return_value.append('telnet server is enabled')
        return_value.append('FAIL')
        return_value.append(
            'grep -R "^telnet" /etc/inetd.* returned the following\n' + success)
    else:
        return_value.append('telnet server not present')
        return_value.append('PASS')
        return_value.append(
            'grep -R "^telnet" /etc/inetd.* returned the following\n' + error)
    return return_value


def _2_1_9_ind():
    return_value = list()
    success, error = check('grep -R "^tftp" /etc/inetd.*')
    if success:
        return_value.append('tftp server is enabled')
        return_value.append('FAIL')
        return_value.append(
            'grep -R "^tftp" /etc/inetd.* returned the following\n' + success)
    else:
        return_value.append('tftp server not present')
        return_value.append('PASS')
        return_value.append(
            'grep -R "^tftp" /etc/inetd.* returned the following\n' + error)
    return return_value


def _2_1_10_ind():
    return_value = list()
    success, error = check('systemctl is-enabled xinetd')
    if success:
        if 'enabled' in success:
            return_value.append('xinetd is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled xinetd returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep xinetd')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('xinetd is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('xinetd is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep xinetd returned the following\n' + success)
            else:
                return_value.append('xinetd is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('xinetd not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled xinetd returned the following\n' + error)
    return return_value


# distro specific
def _2_2_1_1_ind():
    return_value = list()
    return_value.append('time sync not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s ntp')
    if 'Status: install ok installed' in success:
        return_value.append('ntp is installed')
        return_value.append('PASS')
        return_value.append(success)
    else:
        result_error = success + '\n' + error
        success, error = check('sudo dpkg -s chrony')
        if 'Status: install ok installed' in success:
            return_value.append('chrony is installed')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('time sync not used')
            return_value.append('FAIL')
            return_value.append(result_error + '\n' + success + '\n' + error)
    return return_value


def _2_2_1_2_ind():
    return_value = list()
    success, error = check('grep "^restrict" /etc/ntp.conf | grep default')
    if success:
        ntp_restrict = ['kod', 'nomodify', 'notrap', 'nopeer', 'noquery']
        if all(r in s for r in ntp_restrict for s in success.splitlines()):
            result_success = success
            success, error = check('grep -E "^(server|pool)" /etc/ntp.conf')
            if success:
                result_success += '\nVerify remote server configurations\n' + success
                success, error = check('grep "^OPTIONS" /etc/sysconfig/ntpd')
                if 'OPTIONS="-u ntp:ntp"' in success:
                    return_value.append('ntp is configured')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    result_error = success + '\n' + error
                    success, error = check(
                        'grep "^NTPD_OPTIONS" /etc/sysconfig/ntp')
                    if 'OPTIONS="-u ntp:ntp"' in success:
                        return_value.append('ntp is configured')
                        return_value.append('PASS')
                        return_value.append(result_success + '\n' + success)
                    else:
                        result_error += success + '\n' + error
                        success, error = check(
                            'grep "RUNASUSER=ntp" /etc/init.d/ntp')
                        if success:
                            return_value.append('ntp is configured')
                            return_value.append('PASS')
                            return_value.append(
                                result_success + '\n' + success)
                        else:
                            return_value.append(
                                'ntp user configuration not found')
                            return_value.append('FAIL')
                            return_value.append('Following were found configured\n' + result_success +
                                                '\nFollowing are misconfigured\n' + result_error + '\n' + error)
            else:
                return_value.append('remote server misconfigured')
                return_value.append('FAIL')
                return_value.append(
                    'grep -E "^(server|pool)" /etc/ntp.conf returned the following\n' + error)
        else:
            return_value.append('ntp options misconfigured')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('ntp not configured')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _2_2_1_3_ind():
    return_value = list()
    success, error = check('grep -E "^(server|pool)" /etc/chrony.conf')
    if success:
        result_success = 'Verify remote server configurations\n' + success
        success, error = check('ps -ef | grep chronyd')
        if success:
            if any(s.startswith('chrony') for s in success):
                return_value.append('chrony is configured')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + success)
            else:
                return_value.append('chrony not first field of chronyd')
                return_value.append('FAIL')
                return_value.append(result_success + '\n' + success)
        else:
            return_value.append('no chrony processes found')
            return_value.append('FAIL')
            return_value.append(result_success + '\n' + error)
    else:
        return_value.append('remote server not configured')
        return_value.append('FAIL')
        return_value.append(
            'grep -E "^(server|pool)" /etc/chrony.conf returned the following\n' + error)
    return return_value


def _2_2_1_4_ind():
    return_value = list()
    success, error = check('systemctl is-enabled systemd-timesyncd.service')
    if 'enabled' in success:
        result_success = success
        success, error = check('cat /etc/systemd/timesyncd.conf')
        if success:
            result_success += '\nEnsure that the NTP servers, NTP FallbackNTP servers, and RootDistanceMaxSec listed are in accordance with local policy\n' + success
            success, error = check('timedatectl status')
            if success:
                return_value.append('system clock is synchronized')
                return_value.append('PASS')
                return_value.append(result_success + '\nCheck\n' + success)
            else:
                return_value.append('system clock not synchronized')
                return_value.append('FAIL')
                return_value.append(result_success + '\n' + error)
        else:
            return_value.append('no timesync daemon found')
            return_value.append('FAIL')
            return_value.append(
                result_success + '\ncat /etc/systemd/timesyncd.conf returned the following\n' + error)
    else:
        return_value.append('systemd-timesyncd is misconfigured')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


# distro specific
def _2_2_2_ind():
    return_value = list()
    return_value.append('X Window System not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -l xserver-xorg*')
    if success:
        return_value.append('X Window System installed')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        return_value.append('X Window System not installed')
        return_value.append('PASS')
        return_value.append(error)
    return return_value


def _2_2_3_ind():
    return_value = list()
    success, error = check('systemctl is-enabled avahi-daemon')
    if success:
        if 'enabled' in success:
            return_value.append('avahi-daemon is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled avahi-daemon returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep avahi-daemon')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('avahi-daemon is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('avahi-daemon is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep avahi-daemon returned the following\n' + success)
            else:
                return_value.append('avahi-daemon is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('avahi-daemon not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled avahi-daemon returned the following\n' + error)
    return return_value


def _2_2_4_ind():
    return_value = list()
    success, error = check('systemctl is-enabled cups')
    if success:
        if 'enabled' in success:
            return_value.append('cups is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled cups returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep cups')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('cups is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('cups is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep cups returned the following\n' + success)
            else:
                return_value.append('cups is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('cups not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled cups returned the following\n' + error)
    return return_value


def _2_2_5_ind():
    return_value = list()
    success, error = check('systemctl is-enabled dhcpd')
    if success:
        if 'enabled' in success:
            return_value.append('dhcpd is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled dhcpd returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep dhcpd')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('dhcpd is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('dhcpd is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep dhcpd returned the following\n' + success)
            else:
                return_value.append('dhcpd is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('dhcpd not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled dhcpd returned the following\n' + error)
    return return_value


def _2_2_6_ind():
    return_value = list()
    success, error = check('systemctl is-enabled slapd')
    if success:
        if 'enabled' in success:
            return_value.append('slapd is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled slapd returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep slapd')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('slapd is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('slapd is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep slapd returned the following\n' + success)
            else:
                return_value.append('slapd is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('slapd not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled slapd returned the following\n' + error)
    return return_value


def _2_2_7_ind():
    return_value = list()
    nfs_enabled = True
    success, error = check('systemctl is-enabled nfs')
    if success:
        if 'enabled' in success:
            return_value.append('nfs is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled nfs returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep nfs')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    nfs_enabled = False
                    result_success += '\n' + success
                else:
                    return_value.append('nfs is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep nfs returned the following\n' + success)
            else:
                nfs_enabled = False
                result_success += '\n' + error
    else:
        nfs_enabled = False
        result_success = 'systemctl is-enabled nfs returned the following\n' + error
    if not nfs_enabled:
        success, error = check('systemctl is-enabled rpcbind')
        if success:
            if 'enabled' in success:
                return_value.append('rpcbind is enabled')
                return_value.append('FAIL')
                return_value.append(
                    result_success + '\nsystemctl is-enabled rpcbind returned the following\n' + success)
            else:
                result_success += '\n' + success
                success, error = check('ls /etc/rc*.d | grep rpcbind')
                if success:
                    if not any(s for s in success if s.startswith('S')):
                        return_value.append('nfs and rpcbind are disabled')
                        return_value.append('PASS')
                        return_value.append(result_success + '\n' + success)
                    else:
                        return_value.append('rpcbind is enabled')
                        return_value.append('FAIL')
                        return_value.append(
                            result_success + '\nls /etc/rc*.d | grep rpcbind returned the following\n' + success)
                else:
                    return_value.append('nfs and rpcbind are disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + error)
        else:
            return_value.append('npc and rpcbind are disabled')
            return_value.append('PASS')
            return_value.append(
                result_success + '\nsystemctl is-enabled rpcbind returned the following\n' + error)
    return return_value


def _2_2_8_ind():
    return_value = list()
    success, error = check('systemctl is-enabled named')
    if success:
        if 'enabled' in success:
            return_value.append('named is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled named returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep named')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('named is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('named is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep named returned the following\n' + success)
            else:
                return_value.append('named is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('named not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled named returned the following\n' + error)
    return return_value


def _2_2_9_ind():
    return_value = list()
    success, error = check('systemctl is-enabled vsftpd')
    if success:
        if 'enabled' in success:
            return_value.append('vsftpd is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled vsftpd returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep vsftpd')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('vsftpd is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('vsftpd is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep vsftpd returned the following\n' + success)
            else:
                return_value.append('vsftpd is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('vsftpd not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled vsftpd returned the following\n' + error)
    return return_value


def _2_2_10_ind():
    return_value = list()
    success, error = check('systemctl is-enabled httpd')
    if success:
        if 'enabled' in success:
            return_value.append('httpd is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled httpd returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep httpd')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('httpd is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('httpd is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep httpd returned the following\n' + success)
            else:
                return_value.append('httpd is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('httpd not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled httpd returned the following\n' + error)
    return return_value


def _2_2_11_ind():
    return_value = list()
    success, error = check('systemctl is-enabled dovecot')
    if success:
        if 'enabled' in success:
            return_value.append('dovecot is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled dovecot returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep dovecot')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('dovecot is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('dovecot is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep dovecot returned the following\n' + success)
            else:
                return_value.append('dovecot is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('dovecot not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled dovecot returned the following\n' + error)
    return return_value


def _2_2_12_ind():
    return_value = list()
    success, error = check('systemctl is-enabled smb')
    if success:
        if 'enabled' in success:
            return_value.append('smb is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled smb returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep smb')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('smb is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('smb is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep smb returned the following\n' + success)
            else:
                return_value.append('smb is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('smb not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled smb returned the following\n' + error)
    return return_value


def _2_2_13_ind():
    return_value = list()
    success, error = check('systemctl is-enabled squid')
    if success:
        if 'enabled' in success:
            return_value.append('squid is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled squid returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep squid')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('squid is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('squid is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep squid returned the following\n' + success)
            else:
                return_value.append('squid is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('squid not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled squid returned the following\n' + error)
    return return_value


def _2_2_14_ind():
    return_value = list()
    success, error = check('systemctl is-enabled snmpd')
    if success:
        if 'enabled' in success:
            return_value.append('snmpd is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled snmpd returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep snmpd')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('snmpd is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('snmpd is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep snmpd returned the following\n' + success)
            else:
                return_value.append('snmpd is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('snmpd not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled snmpd returned the following\n' + error)
    return return_value


def _2_2_15_ind():
    return_value = list()
    success, error = check(
        "ss -lntu | grep -E ':25\s' | grep -E -v '\s(127.0.0.1|::1):25\s'")
    if not success:
        return_value.append('mta is local only')
        return_value.append('PASS')
        return_value.append(
            "ss -lntu | grep -E ':25\s' | grep -E -v '\s(127.0.0.1|::1):25\s' returned the following\n" + error)
    else:
        return_value.append('mta is not local only')
        return_value.append('FAIL')
        return_value.append(
            "ss -lntu | grep -E ':25\s' | grep -E -v '\s(127.0.0.1|::1):25\s' returned the following\n" + success)
    return return_value


def _2_2_16_ind():
    return_value = list()
    success, error = check('systemctl is-enabled rsyncd')
    if success:
        if 'enabled' in success:
            return_value.append('rsyncd is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled rsyncd returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep rsyncd')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('rsyncd is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('rsyncd is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep rsyncd returned the following\n' + success)
            else:
                return_value.append('rsyncd is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('rsyncd not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled rsyncd returned the following\n' + error)
    return return_value


def _2_2_17_ind():
    return_value = list()
    success, error = check('systemctl is-enabled ypserv')
    if success:
        if 'enabled' in success:
            return_value.append('ypserv is enabled')
            return_value.append('FAIL')
            return_value.append(
                'systemctl is-enabled ypserv returned the following\n' + success)
        else:
            result_success = success
            success, error = check('ls /etc/rc*.d | grep ypserv')
            if success:
                if not any(s for s in success if s.startswith('S')):
                    return_value.append('ypserv is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + '\n' + success)
                else:
                    return_value.append('ypsesrv is enabled')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success + '\nls /etc/rc*.d | grep ypserv returned the following\n' + success)
            else:
                return_value.append('ypserv is disabled')
                return_value.append('PASS')
                return_value.append(result_success + '\n' + error)
    else:
        return_value.append('ypserv not found')
        return_value.append('PASS')
        return_value.append(
            'systemctl is-enabled ypserv returned the following\n' + error)
    return return_value


# distro specific
def _2_3_1_ind():
    return_value = list()
    return_value.append('NIS Client not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s ypbind')
    if 'Status: install ok installed' in success:
        return_value.append('X Window System installed')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        return_value.append('NIS Client not installed')
        return_value.append('PASS')
        return_value.append(error)
    return return_value


# distro specific
def _2_3_2_ind():
    return_value = list()
    return_value.append('rsh Client not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s rsh')
    if 'Status: install ok installed' in success:
        return_value.append('rsh client installed')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        return_value.append('rsh Client not installed')
        return_value.append('PASS')
        return_value.append(error)
    return return_value


# distro specific
def _2_3_3_ind():
    return_value = list()
    return_value.append('talk Client not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s talk')
    if 'Status: install ok installed' in success:
        return_value.append('talk client installed')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        return_value.append('talk Client not installed')
        return_value.append('PASS')
        return_value.append(error)
    return return_value


# distro specific
def _2_3_4_ind():
    return_value = list()
    return_value.append('telnet Client not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s telnet')
    if 'Status: install ok installed' in success:
        return_value.append('telnet client installed')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        return_value.append('telnet Client not installed')
        return_value.append('PASS')
        return_value.append(error)
    return return_value


# distro specific
def _2_3_5_ind():
    return_value = list()
    return_value.append('LDAP Client not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s openldap-clients')
    if error:
        result_error = error
        success, error = check('sudo dpkg -s openldap2-client')
        if error:
            result_error += '\n' + error
            success, error = check('sudo dpkg -s ldap-utils')
            if error:
                return_value.append('LDAP Client not installed')
                return_value.append('PASS')
                return_value.append(result_error + '\n' + error)
            else:
                return_value.append('ldap-utils installed')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('openldap2-client installed')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('openldap-clients installed')
        return_value.append('FAIL')
        return_value.append(success)
    return return_value


def _3_1_1_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.ip_forward')
    if success.endswith('0'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.ip_forward" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('0') for s in ipv4):
            result_success += success + '\n'
            success, error = check('sysctl net.ipv6.conf.all.forwarding')
            if success.endswith('0'):
                result_success = success + '\n'
                success, error = check(
                    'grep "net\.ipv6\.conf\.all\.forwarding" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv6 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('0') for s in ipv6):
                    return_value.append('IP forwarding disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + success)
                else:
                    return_value.append('ipv6 forwards packets')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv6 forwards packets')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv4 forwards packets')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 forwards packets')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_1_2_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.conf.all.send_redirects')
    if success.endswith('0'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.conf\.all\.send_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('0') for s in ipv4):
            result_success += success + '\n'
            success, error = check(
                'sysctl net.ipv4.conf.default.send_redirects')
            if success.endswith('0'):
                result_success = success + '\n'
                success, error = check(
                    'grep "net\.ipv4\.conf\.default\.send_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv4 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('0') for s in ipv4):
                    return_value.append('packet redirect sending is disabled')
                    return_value.append('PASS')
                    return_value.append(result_success + success)
                else:
                    return_value.append('ipv4 redirects default packets')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv4 redirects default packets')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv4 redirects all packets')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 redirects all packets')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_1_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.conf.all.accept_source_route')
    if success.endswith('0'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.conf\.all\.accept_source_route" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('0') for s in ipv4):
            result_success += success + '\n'
            success, error = check(
                'sysctl net.ipv4.conf.default.accept_source_route')
            if success.endswith('0'):
                result_success += success + '\n'
                success, error = check(
                    'grep "net\.ipv4\.conf\.default\.accept_source_route" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv4 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('0') for s in ipv4):
                    result_success += success + '\n'
                    success, error = check(
                        'sysctl net.ipv6.conf.all.accept_source_route')
                    if success.endswith('0'):
                        result_success = success + '\n'
                        success, error = check(
                            'grep "net\.ipv6\.conf\.all\.accept_source_route" /etc/sysctl.conf /etc/sysctl.d/*')
                        ipv6 = [s.split(':')[1] for s in success.splitlines()]
                        if all(s.endswith('0') for s in ipv6):
                            result_success += success + '\n'
                            success, error = check(
                                'sysctl net.ipv6.conf.default.accept_source_route')
                            if success.endswith('0'):
                                result_success += success + '\n'
                                success, error = check(
                                    'grep "net\.ipv6\.conf\.default\.accept_source_route" /etc/sysctl.conf /etc/sysctl.d/*')
                                ipv6 = [s.split(':')[1]
                                        for s in success.splitlines()]
                                if all(s.endswith('0') for s in ipv6):
                                    return_value.append(
                                        'source routed packets are not accepted')
                                    return_value.append('PASS')
                                    return_value.append(
                                        result_success + success)
                                else:
                                    return_value.append(
                                        'ipv6 accepts default source packets')
                                    return_value.append('PASS')
                                    return_value.append(
                                        result_success + success)
                            else:
                                return_value.append(
                                    'ipv6 accepts default source packets')
                                return_value.append('FAIL')
                                return_value.append(result_success + success)
                        else:
                            return_value.append(
                                'ipv6 accepts all source packets')
                            return_value.append('FAIL')
                            return_value.append(result_success + success)
                    else:
                        return_value.append('ipv6 accepts all source packets')
                        return_value.append('FAIL')
                        return_value.append(result_success + success)
                else:
                    return_value.append('ipv4 accepts default source packets')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv4 accepts default source packets')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv4 accepts all source packets')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 accepts all source packets')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_2_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.conf.all.accept_redirects')
    if success.endswith('0'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.conf\.all\.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('0') for s in ipv4):
            result_success += success + '\n'
            success, error = check(
                'sysctl net.ipv4.conf.default.accept_redirects')
            if success.endswith('0'):
                result_success += success + '\n'
                success, error = check(
                    'grep "net\.ipv4\.conf\.default\.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv4 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('0') for s in ipv4):
                    result_success += success + '\n'
                    success, error = check(
                        'sysctl net.ipv6.conf.all.accept_redirects')
                    if success.endswith('0'):
                        result_success = success + '\n'
                        success, error = check(
                            'grep "net\.ipv6\.conf\.all\.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
                        ipv6 = [s.split(':')[1] for s in success.splitlines()]
                        if all(s.endswith('0') for s in ipv6):
                            result_success += success + '\n'
                            success, error = check(
                                'sysctl net.ipv6.conf.default.accept_redirects')
                            if success.endswith('0'):
                                result_success += success + '\n'
                                success, error = check(
                                    'grep "net\.ipv6\.conf\.default\.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
                                ipv6 = [s.split(':')[1]
                                        for s in success.splitlines()]
                                if all(s.endswith('0') for s in ipv6):
                                    return_value.append(
                                        'ICMP redirects not accepted')
                                    return_value.append('PASS')
                                    return_value.append(
                                        result_success + success)
                                else:
                                    return_value.append(
                                        'ipv6 accepts default redirects')
                                    return_value.append('PASS')
                                    return_value.append(
                                        result_success + success)
                            else:
                                return_value.append(
                                    'ipv6 accepts default redirects')
                                return_value.append('FAIL')
                                return_value.append(result_success + success)
                        else:
                            return_value.append('ipv6 accepts all redirects')
                            return_value.append('FAIL')
                            return_value.append(result_success + success)
                    else:
                        return_value.append('ipv6 accepts all redirects')
                        return_value.append('FAIL')
                        return_value.append(result_success + success)
                else:
                    return_value.append('ipv4 accepts default redirects')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv4 accepts default redirects')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv4 accepts all redirects')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 accepts all redirects')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_3_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.conf.all.secure_redirects')
    if success.endswith('0'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.conf\.all\.secure_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('0') for s in ipv4):
            result_success += success + '\n'
            success, error = check(
                'sysctl net.ipv4.conf.default.secure_redirects')
            if success.endswith('0'):
                result_success = success + '\n'
                success, error = check(
                    'grep "net\.ipv4\.conf\.default\.secure_redirects" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv4 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('0') for s in ipv4):
                    return_value.append('secure ICMP redirects not accepted')
                    return_value.append('PASS')
                    return_value.append(result_success + success)
                else:
                    return_value.append('ipv4 redirects default secure ICMP')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv4 redirects default secure ICMP')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv4 redirects all secure ICMP')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 redirects all secure ICMP')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_4_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.conf.all.log_martians')
    if success.endswith('1'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.conf\.all\.log_martians" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('1') for s in ipv4):
            result_success += success + '\n'
            success, error = check('sysctl net.ipv4.conf.default.log_martians')
            if success.endswith('1'):
                result_success = success + '\n'
                success, error = check(
                    'grep "net\.ipv4\.conf\.default\.log_martians" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv4 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('1') for s in ipv4):
                    return_value.append('suspicious packets are logged')
                    return_value.append('PASS')
                    return_value.append(result_success + success)
                else:
                    return_value.append('ipv4 default packets not logged')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv4 default packets not logged')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv4 all packets not logged')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 all packets not logged')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_5_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.icmp_echo_ignore_broadcasts')
    if success.endswith('1'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.icmp_echo_ignore_broadcasts" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('1') for s in ipv4):
            return_value.append('broadcast ICMP requests ignored')
            return_value.append('PASS')
            return_value.append(result_success + success)
        else:
            return_value.append('ipv4 broadcasts not ignored')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 broadcasts not ignored')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_6_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.icmp_ignore_bogus_error_responses')
    if success.endswith('1'):
        result_success = success + '\n'
        success, error = check(
            'grep "net.ipv4.icmp_ignore_bogus_error_responses" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('1') for s in ipv4):
            return_value.append('bogus ICMP responses ignored')
            return_value.append('PASS')
            return_value.append(result_success + success)
        else:
            return_value.append('ipv4 bogus responses not ignored')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 bogus responses not ignored')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_7_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.conf.all.rp_filter')
    if success.endswith('1'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.conf\.all\.rp_filter" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('1') for s in ipv4):
            result_success += success + '\n'
            success, error = check('sysctl net.ipv4.conf.default.rp_filter')
            if success.endswith('1'):
                result_success = success + '\n'
                success, error = check(
                    'grep "net\.ipv4\.conf\.default\.rp_filter" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv4 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('1') for s in ipv4):
                    return_value.append('Reverse Path Filtering enabled')
                    return_value.append('PASS')
                    return_value.append(result_success + success)
                else:
                    return_value.append('ipv4 default rp filtering disabled')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv4 default rp filtering disabled')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv4 all rp filtering disabled')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 all rp filtering disabled')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_8_ind():
    return_value = list()
    success, error = check('sysctl net.ipv4.tcp_syncookies')
    if success.endswith('1'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv4\.tcp_syncookies" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('1') for s in ipv4):
            return_value.append('TCP SYN Cookies enabled')
            return_value.append('PASS')
            return_value.append(result_success + success)
        else:
            return_value.append('ipv4 tcp syncookies disabled')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv4 tcp syncookies disabled')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_2_9_ind():
    return_value = list()
    success, error = check('sysctl net.ipv6.conf.all.accept_ra')
    if success.endswith('0'):
        result_success = success + '\n'
        success, error = check(
            'grep "net\.ipv6\.conf\.all\.accept_ra" /etc/sysctl.conf /etc/sysctl.d/*')
        ipv4 = [s.split(':')[1] for s in success.splitlines()]
        if all(s.endswith('0') for s in ipv4):
            result_success += success + '\n'
            success, error = check('sysctl net.ipv6.conf.default.accept_ra')
            if success.endswith('0'):
                result_success = success + '\n'
                success, error = check(
                    'grep "net\.ipv6\.conf\.default\.accept_ra" /etc/sysctl.conf /etc/sysctl.d/*')
                ipv4 = [s.split(':')[1] for s in success.splitlines()]
                if all(s.endswith('0') for s in ipv4):
                    return_value.append('IPv6 router advert not accepted')
                    return_value.append('PASS')
                    return_value.append(result_success + success)
                else:
                    return_value.append('ipv6 default ra accepted')
                    return_value.append('FAIL')
                    return_value.append(result_success + success)
            else:
                return_value.append('ipv6 default ra accepted')
                return_value.append('FAIL')
                return_value.append(result_success + success)
        else:
            return_value.append('ipv6 all ra accepted')
            return_value.append('FAIL')
            return_value.append(result_success + success)
    else:
        return_value.append('ipv6 all ra accepted')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


# distro specific
def _3_3_1_ind():
    return_value = list()
    return_value.append('TCP Wrappers not checked (ind distro)')
    return_value.append('CHEK')
    return_value.append('Distribution was not specified')
    return return_value
    success, error = check('sudo dpkg -s tcpd')
    if 'Status: install ok installed' in success:
        return_value.append('talk client installed')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('TCP Wrappers not installed')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _3_3_2_ind():
    return_value = list()
    success, error = check('cat /etc/hosts.allow')
    if not all(s.startswith('#') or not s for s in success.splitlines()):
        return_value.append('/etc/hosts.allow configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/etc/hosts.allow not configured')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_3_3_ind():
    return_value = list()
    success, error = check('cat /etc/hosts.deny')
    if 'ALL: ALL' in success:
        return_value.append('/etc/hosts.deny configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/etc/hosts.deny not configured')
        return_value.append('FAIL')
        return_value.append(success + '\n' + error)
    return return_value


def _3_3_4_ind():
    return_value = list()
    success, error = check('stat /etc/hosts.allow | grep Access')
    if success:
        if 'Uid: (    0/    root)   Gid: (    0/    root)' in success:
            if '(0644/-rw-r--r--)' in success:
                return_value.append('/etc/hosts.allow permissions configured')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append(
                    '/etc/hosts.allow permits group and others')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('/etc/hosts.allow invalid uid and gid')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('/etc/hosts.allow not found')
        return_value.append('CHEK')
        return_value.append(
            'stat /etc/hosts.allow | grep Access did not return anything\n' + error)
    return return_value


def _3_3_5_ind():
    return_value = list()
    success, error = check('stat /etc/hosts.deny | grep Access')
    if success:
        if 'Uid: (    0/    root)   Gid: (    0/    root)' in success:
            if '(0644/-rw-r--r--)' in success:
                return_value.append('/etc/hosts.deny permissions configured')
                return_value.append('PASS')
                return_value.append(success)
            else:
                return_value.append('/etc/hosts.deny permits group and others')
                return_value.append('FAIL')
                return_value.append(success)
        else:
            return_value.append('/etc/hosts.deny invalid uid and gid')
            return_value.append('FAIL')
            return_value.append(success)
    else:
        return_value.append('/etc/hosts.deny not found')
        return_value.append('CHEK')
        return_value.append(
            'stat /etc/hosts.deny | grep Access did not return anything\n' + error)
    return return_value


def _3_4_1_ind():
    return_value = list()
    success, error = check('modprobe -n -v dccp')
    if 'insmod' in success:
        return_value.append('dccp can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep dccp')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('dccp cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('dccp is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('dccp mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _3_4_2_ind():
    return_value = list()
    success, error = check('modprobe -n -v sctp')
    if 'insmod' in success:
        return_value.append('sctp can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep sctp')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('sctp cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('sctp is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('sctp mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _3_4_3_ind():
    return_value = list()
    success, error = check('modprobe -n -v rds')
    if 'insmod' in success:
        return_value.append('rds can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep rds')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('rds cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('rds is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('rds mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _3_4_4_ind():
    return_value = list()
    success, error = check('modprobe -n -v tipc')
    if 'insmod' in success:
        return_value.append('tipc can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep tipc')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('tipc cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('tipc is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('tipc mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


"""
Definitions of Functions that perform CentOS checks against benchmarks
return_value[0] = result
return_value[1] = PASS/FAIL/CHEK
return_value[2] = success/error message
Goto line "156" in order to view definition of test()
"""


def _1_1_1_1_cen():
    return_value = list()
    success, error = check('modprobe -n -v cramfs')
    if 'insmod' in success:
        return_value.append('cramfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep cramfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('cramfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('cramfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('cramfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_2_cen():
    return_value = list()
    success, error = check("grep -E -i '\svfat\s' /etc/fstab")
    if success:
        return_value.append('vfat is mounted')
        return_value.append('CHEK')
        return_value.append(success)
    else:
        success, error = check('modprobe -n -v vfat')
        if 'insmod' in success:
            return_value.append('vfat can be mounted')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            result_success = success
            result_error = error
            success, error = check('lsmod | grep vfat')
            if 'install /bin/true' in result_success or 'not found in directory' in result_error:
                if not success:
                    return_value.append('vfat cannot be mounted')
                    return_value.append('PASS')
                    return_value.append(
                        result_success if result_success else result_error)
                else:
                    return_value.append('vfat is mounted')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success if result_success else result_error + '\n' + success)
            else:
                return_value.append('vfat mount status undetermined')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_3_cen():
    return_value = list()
    success, error = check('modprobe -n -v squashfs')
    if 'insmod' in success:
        return_value.append('squashfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep squashfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('squashfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('squashfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('squashfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_4_cen():
    return_value = list()
    success, error = check('modprobe -n -v udf')
    if 'insmod' in success:
        return_value.append('udf can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep udf')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('udf cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('udf is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('udf mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_2_cen():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        return_value.append('/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('/tmp is not configured')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_3_cen():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nodev did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nodev is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_4_cen():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nosuid did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nosuid is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_5_cen():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v noexec did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('noexec is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_6_cen():
    return_value = list()
    success, error = check("mount | grep -E '\s/var\s'")
    if success:
        return_value.append('/var is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/var\s' did not return any result")
    return return_value


def _1_1_7_cen():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        return_value.append('/var/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/tmp is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/tmp did not return any result")
    return return_value


def _1_1_8_cen():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_9_cen():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_10_cen():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_11_cen():
    return_value = list()
    success, error = check('mount | grep /var/log')
    if success:
        return_value.append('/var/log is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/log did not return any result")
    return return_value


def _1_1_12_cen():
    return_value = list()
    success, error = check('mount | grep /var/log/audit')
    if success:
        return_value.append('/var/log/audit is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log/audit is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep /var/log/audit did not return any result")
    return return_value


def _1_1_13_cen():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        return_value.append('/home is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/home is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /home did not return any result")
    return return_value


def _1_1_14_cen():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        success, error = check("mount | grep -E '\s/home\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /home')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/home\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /home')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /home')
        return_value.append('FAIL')
        return_value.append(
            "/home does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_15_cen():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_16_cen():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nosuid is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_17_cen():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_18_cen():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nodev = [drive for drive in success.splitlines()
                 if 'nodev' not in drive]
        if not nodev:
            return_value.append('nodev is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nodev is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nodev" set\n'
            for n in nodev:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_19_cen():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nosuid = [drive for drive in success.splitlines()
                  if 'nosuid' not in drive]
        if not nosuid:
            return_value.append('nosuid is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nosuid is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nosuid" set\n'
            for n in nosuid:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_20_cen():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        noexec = [drive for drive in success.splitlines()
                  if 'noexec' not in drive]
        if not noexec:
            return_value.append('noexec is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('noexec is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "noexec" set\n'
            for n in noexec:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_21_cen():
    return_value = list()
    success, error = check(
        "df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null")
    if not success:
        return_value.append('sticky bit set on w-w directories')
        return_value.append('PASS')
        return_value.append(
            "running df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null confirms that all world writable directories have the sticky variable set")
    else:
        return_value.append('directories without sticky bit found')
        return_value.append('FAIL')
        return_value.append(
            'The following directories does not have their sticky bit set\n' + success)
    return return_value


def _1_1_22_cen():
    return_value = list()
    success, error = check('systemctl is-enabled autofs | grep enabled')
    if error:
        return_value.append('automounting could not be checked')
        return_value.append('CHEK')
        return_value.append(error)
    else:
        if 'enabled' in success:
            return_value.append('automounting is enabled')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            return_value.append('automounting is disabled')
            return_value.append('PASS')
            return_value.append(success)
    return return_value


def _1_1_23_cen():
    return_value = list()
    success, error = check('modprobe -n -v usb-storage')
    if 'insmod' in success:
        return_value.append('usb-storage can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep usb-storage')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('usb-storage cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('usb-storage is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('usb-storage mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


"""
Definitions of Functions that perform Debian checks against benchmarks
return_value[0] = result
return_value[1] = PASS/FAIL/CHEK
return_value[2] = success/error message
Goto line "156" in order to view definition of test()
"""


def _1_1_1_1_deb():
    return_value = list()
    success, error = check('modprobe -n -v freevxfs')
    if 'insmod' in success:
        return_value.append('freevxfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep freevxfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('freevxfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('freevxfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('freevxfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_2_deb():
    return_value = list()
    success, error = check('modprobe -n -v jffs2')
    if 'insmod' in success:
        return_value.append('jffs2 can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep jffs2')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('jffs2 cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('jffs2 is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('jffs2 mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_3_deb():
    return_value = list()
    success, error = check('modprobe -n -v hfs')
    if 'insmod' in success:
        return_value.append('hfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_4_deb():
    return_value = list()
    success, error = check('modprobe -n -v hfsplus')
    if 'insmod' in success:
        return_value.append('hfsplus can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfsplus')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfsplus cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfsplus is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfsplus mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_2_deb():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        return_value.append('/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('/tmp is not configured')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_3_deb():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nodev did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nodev is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_4_deb():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nosuid did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nosuid is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_5_deb():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v noexec did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('noexec is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_6_deb():
    return_value = list()
    success, error = check("mount | grep -E '\s/var\s'")
    if success:
        return_value.append('/var is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/var\s' did not return any result")
    return return_value


def _1_1_7_deb():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        return_value.append('/var/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/tmp is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/tmp did not return any result")
    return return_value


def _1_1_8_deb():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_9_deb():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_10_deb():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_11_deb():
    return_value = list()
    success, error = check('mount | grep /var/log')
    if success:
        return_value.append('/var/log is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/log did not return any result")
    return return_value


def _1_1_12_deb():
    return_value = list()
    success, error = check('mount | grep /var/log/audit')
    if success:
        return_value.append('/var/log/audit is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log/audit is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep /var/log/audit did not return any result")
    return return_value


def _1_1_13_deb():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        return_value.append('/home is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/home is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /home did not return any result")
    return return_value


def _1_1_14_deb():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        success, error = check("mount | grep -E '\s/home\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /home')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/home\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /home')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /home')
        return_value.append('FAIL')
        return_value.append(
            "/home does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_15_deb():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_16_deb():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nosuid is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_17_deb():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_18_deb():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nodev = [drive for drive in success.splitlines()
                 if 'nodev' not in drive]
        if not nodev:
            return_value.append('nodev is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nodev is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nodev" set\n'
            for n in nodev:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_19_deb():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nosuid = [drive for drive in success.splitlines()
                  if 'nosuid' not in drive]
        if not nosuid:
            return_value.append('nosuid is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nosuid is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nosuid" set\n'
            for n in nosuid:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_20_deb():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        noexec = [drive for drive in success.splitlines()
                  if 'noexec' not in drive]
        if not noexec:
            return_value.append('noexec is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('noexec is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "noexec" set\n'
            for n in noexec:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_21_deb():
    return_value = list()
    success, error = check(
        "df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null")
    if not success:
        return_value.append('sticky bit set on w-w directories')
        return_value.append('PASS')
        return_value.append(
            "running df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null confirms that all world writable directories have the sticky variable set")
    else:
        return_value.append('directories without sticky bit found')
        return_value.append('FAIL')
        return_value.append(
            'The following directories does not have their sticky bit set\n' + success)
    return return_value


def _1_1_22_deb():
    return_value = list()
    success, error = check('systemctl is-enabled autofs | grep enabled')
    if error:
        return_value.append('automounting could not be checked')
        return_value.append('CHEK')
        return_value.append(error)
    else:
        if 'enabled' in success:
            return_value.append('automounting is enabled')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            return_value.append('automounting is disabled')
            return_value.append('PASS')
            return_value.append(success)
    return return_value


"""
Definitions of Functions that perform Fedora checks against benchmarks
return_value[0] = result
return_value[1] = PASS/FAIL/CHEK
return_value[2] = success/error message
Goto line "156" in order to view definition of test()
"""


def _1_1_1_1_fed():
    return_value = list()
    success, error = check('modprobe -n -v cramfs')
    if 'insmod' in success:
        return_value.append('cramfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep cramfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('cramfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('cramfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('cramfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_2_fed():
    return_value = list()
    success, error = check("grep -E -i '\svfat\s' /etc/fstab")
    if success:
        return_value.append('vfat is mounted')
        return_value.append('CHEK')
        return_value.append(success)
    else:
        success, error = check('modprobe -n -v vfat')
        if 'insmod' in success:
            return_value.append('vfat can be mounted')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            result_success = success
            result_error = error
            success, error = check('lsmod | grep vfat')
            if 'install /bin/true' in result_success or 'not found in directory' in result_error:
                if not success:
                    return_value.append('vfat cannot be mounted')
                    return_value.append('PASS')
                    return_value.append(
                        result_success if result_success else result_error)
                else:
                    return_value.append('vfat is mounted')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success if result_success else result_error + '\n' + success)
            else:
                return_value.append('vfat mount status undetermined')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_3_fed():
    return_value = list()
    success, error = check('modprobe -n -v squashfs')
    if 'insmod' in success:
        return_value.append('squashfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep squashfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('squashfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('squashfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('squashfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_4_fed():
    return_value = list()
    success, error = check('modprobe -n -v udf')
    if 'insmod' in success:
        return_value.append('udf can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep udf')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('udf cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('udf is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('udf mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_2_fed():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        return_value.append('/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('/tmp is not configured')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_3_fed():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nodev did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nodev is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_4_fed():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nosuid did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nosuid is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_5_fed():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v noexec did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('noexec is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_6_fed():
    return_value = list()
    success, error = check("mount | grep -E '\s/var\s'")
    if success:
        return_value.append('/var is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/var\s' did not return any result")
    return return_value


def _1_1_7_fed():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        return_value.append('/var/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/tmp is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/tmp did not return any result")
    return return_value


def _1_1_8_fed():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_9_fed():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_10_fed():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_11_fed():
    return_value = list()
    success, error = check('mount | grep /var/log')
    if success:
        return_value.append('/var/log is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/log did not return any result")
    return return_value


def _1_1_12_fed():
    return_value = list()
    success, error = check('mount | grep /var/log/audit')
    if success:
        return_value.append('/var/log/audit is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log/audit is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep /var/log/audit did not return any result")
    return return_value


def _1_1_13_fed():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        return_value.append('/home is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/home is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /home did not return any result")
    return return_value


def _1_1_14_fed():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        success, error = check("mount | grep -E '\s/home\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /home')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/home\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /home')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /home')
        return_value.append('FAIL')
        return_value.append(
            "/home does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_15_fed():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_16_fed():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nosuid is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_17_fed():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_18_fed():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nodev = [drive for drive in success.splitlines()
                 if 'nodev' not in drive]
        if not nodev:
            return_value.append('nodev is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nodev is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nodev" set\n'
            for n in nodev:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_19_fed():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nosuid = [drive for drive in success.splitlines()
                  if 'nosuid' not in drive]
        if not nosuid:
            return_value.append('nosuid is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nosuid is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nosuid" set\n'
            for n in nosuid:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_20_fed():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        noexec = [drive for drive in success.splitlines()
                  if 'noexec' not in drive]
        if not noexec:
            return_value.append('noexec is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('noexec is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "noexec" set\n'
            for n in noexec:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_21_fed():
    return_value = list()
    success, error = check(
        "df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null")
    if not success:
        return_value.append('sticky bit set on w-w directories')
        return_value.append('PASS')
        return_value.append(
            "running df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null confirms that all world writable directories have the sticky variable set")
    else:
        return_value.append('directories without sticky bit found')
        return_value.append('FAIL')
        return_value.append(
            'The following directories does not have their sticky bit set\n' + success)
    return return_value


def _1_1_22_fed():
    return_value = list()
    success, error = check('systemctl is-enabled autofs | grep enabled')
    if error:
        return_value.append('automounting could not be checked')
        return_value.append('CHEK')
        return_value.append(error)
    else:
        if 'enabled' in success:
            return_value.append('automounting is enabled')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            return_value.append('automounting is disabled')
            return_value.append('PASS')
            return_value.append(success)
    return return_value


def _1_1_23_fed():
    return_value = list()
    success, error = check('modprobe -n -v usb-storage')
    if 'insmod' in success:
        return_value.append('usb-storage can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep usb-storage')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('usb-storage cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('usb-storage is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('usb-storage mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


"""
Definitions of Functions that perform RedHat checks against benchmarks
return_value[0] = result
return_value[1] = PASS/FAIL/CHEK
return_value[2] = success/error message
Goto line "156" in order to view definition of test()
"""


def _1_1_1_1_red():
    return_value = list()
    success, error = check('modprobe -n -v cramfs')
    if 'insmod' in success:
        return_value.append('cramfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep cramfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('cramfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('cramfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('cramfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_2_red():
    return_value = list()
    success, error = check("grep -E -i '\svfat\s' /etc/fstab")
    if success:
        return_value.append('vfat is mounted')
        return_value.append('CHEK')
        return_value.append(success)
    else:
        success, error = check('modprobe -n -v vfat')
        if 'insmod' in success:
            return_value.append('vfat can be mounted')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            result_success = success
            result_error = error
            success, error = check('lsmod | grep vfat')
            if 'install /bin/true' in result_success or 'not found in directory' in result_error:
                if not success:
                    return_value.append('vfat cannot be mounted')
                    return_value.append('PASS')
                    return_value.append(
                        result_success if result_success else result_error)
                else:
                    return_value.append('vfat is mounted')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success if result_success else result_error + '\n' + success)
            else:
                return_value.append('vfat mount status undetermined')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_3_red():
    return_value = list()
    success, error = check('modprobe -n -v squashfs')
    if 'insmod' in success:
        return_value.append('squashfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep squashfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('squashfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('squashfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('squashfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_4_red():
    return_value = list()
    success, error = check('modprobe -n -v udf')
    if 'insmod' in success:
        return_value.append('udf can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep udf')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('udf cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('udf is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('udf mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_2_red():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        return_value.append('/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('/tmp is not configured')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_3_red():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nodev did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nodev is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_4_red():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nosuid did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nosuid is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_5_red():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v noexec did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('noexec is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_6_red():
    return_value = list()
    success, error = check("mount | grep -E '\s/var\s'")
    if success:
        return_value.append('/var is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/var\s' did not return any result")
    return return_value


def _1_1_7_red():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        return_value.append('/var/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/tmp is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/tmp did not return any result")
    return return_value


def _1_1_8_red():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_9_red():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_10_red():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_11_red():
    return_value = list()
    success, error = check('mount | grep /var/log')
    if success:
        return_value.append('/var/log is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/log did not return any result")
    return return_value


def _1_1_12_red():
    return_value = list()
    success, error = check('mount | grep /var/log/audit')
    if success:
        return_value.append('/var/log/audit is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log/audit is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep /var/log/audit did not return any result")
    return return_value


def _1_1_13_red():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        return_value.append('/home is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/home is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /home did not return any result")
    return return_value


def _1_1_14_red():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        success, error = check("mount | grep -E '\s/home\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /home')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/home\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /home')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /home')
        return_value.append('FAIL')
        return_value.append(
            "/home does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_15_red():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_16_red():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nosuid is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_17_red():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_18_red():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nodev = [drive for drive in success.splitlines()
                 if 'nodev' not in drive]
        if not nodev:
            return_value.append('nodev is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nodev is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nodev" set\n'
            for n in nodev:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_19_red():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nosuid = [drive for drive in success.splitlines()
                  if 'nosuid' not in drive]
        if not nosuid:
            return_value.append('nosuid is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nosuid is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nosuid" set\n'
            for n in nosuid:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_20_red():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        noexec = [drive for drive in success.splitlines()
                  if 'noexec' not in drive]
        if not noexec:
            return_value.append('noexec is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('noexec is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "noexec" set\n'
            for n in noexec:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_21_red():
    return_value = list()
    success, error = check(
        "df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null")
    if not success:
        return_value.append('sticky bit set on w-w directories')
        return_value.append('PASS')
        return_value.append(
            "running df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null confirms that all world writable directories have the sticky variable set")
    else:
        return_value.append('directories without sticky bit found')
        return_value.append('FAIL')
        return_value.append(
            'The following directories does not have their sticky bit set\n' + success)
    return return_value


def _1_1_22_red():
    return_value = list()
    success, error = check('systemctl is-enabled autofs | grep enabled')
    if error:
        return_value.append('automounting could not be checked')
        return_value.append('CHEK')
        return_value.append(error)
    else:
        if 'enabled' in success:
            return_value.append('automounting is enabled')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            return_value.append('automounting is disabled')
            return_value.append('PASS')
            return_value.append(success)
    return return_value


def _1_1_23_red():
    return_value = list()
    success, error = check('modprobe -n -v usb-storage')
    if 'insmod' in success:
        return_value.append('usb-storage can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep usb-storage')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('usb-storage cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('usb-storage is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('usb-storage mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


"""
Definitions of Functions that perform SUSE checks against benchmarks
return_value[0] = result
return_value[1] = PASS/FAIL/CHEK
return_value[2] = success/error message
Goto line "156" in order to view definition of test()
"""


def _1_1_1_1_sus():
    return_value = list()
    success, error = check('modprobe -n -v cramfs')
    if 'insmod' in success:
        return_value.append('cramfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep cramfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('cramfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('cramfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('cramfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_2_sus():
    return_value = list()
    success, error = check('modprobe -n -v freevxfs')
    if 'insmod' in success:
        return_value.append('freevxfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep freevxfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('freevxfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('freevxfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('freevxfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_3_sus():
    return_value = list()
    success, error = check('modprobe -n -v jffs2')
    if 'insmod' in success:
        return_value.append('jffs2 can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep jffs2')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('jffs2 cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('jffs2 is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('jffs2 mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_4_sus():
    return_value = list()
    success, error = check('modprobe -n -v hfs')
    if 'insmod' in success:
        return_value.append('hfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_5_sus():
    return_value = list()
    success, error = check('modprobe -n -v hfsplus')
    if 'insmod' in success:
        return_value.append('hfsplus can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfsplus')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfsplus cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfsplus is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfsplus mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_6_sus():
    return_value = list()
    success, error = check('modprobe -n -v squashfs')
    if 'insmod' in success:
        return_value.append('squashfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep squashfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('squashfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('squashfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('squashfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_7_sus():
    return_value = list()
    success, error = check('modprobe -n -v udf')
    if 'insmod' in success:
        return_value.append('udf can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep udf')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('udf cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('udf is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('udf mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_8_sus():
    return_value = list()
    success, error = check('modprobe -n -v vfat')
    if 'insmod' in success:
        return_value.append('vfat can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep vfat')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('vfat cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('vfat is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('vfat mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_2_sus():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        return_value.append('/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/tmp is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/tmp\s'\ndid not return any result")
    return return_value


def _1_1_3_sus():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nodev did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nodev is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_4_sus():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nosuid did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nosuid is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_5_sus():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v noexec did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('noexec is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_6_sus():
    return_value = list()
    success, error = check("mount | grep -E '\s/var\s'")
    if success:
        return_value.append('/var is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/var\s' did not return any result")
    return return_value


def _1_1_7_sus():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        return_value.append('/var/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/tmp is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/tmp did not return any result")
    return return_value


def _1_1_8_sus():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_9_sus():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_10_sus():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_11_sus():
    return_value = list()
    success, error = check('mount | grep /var/log')
    if success:
        return_value.append('/var/log is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/log did not return any result")
    return return_value


def _1_1_12_sus():
    return_value = list()
    success, error = check('mount | grep /var/log/audit')
    if success:
        return_value.append('/var/log/audit is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log/audit is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep /var/log/audit did not return any result")
    return return_value


def _1_1_13_sus():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        return_value.append('/home is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/home is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /home did not return any result")
    return return_value


def _1_1_14_sus():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        success, error = check("mount | grep -E '\s/home\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /home')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/home\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /home')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /home')
        return_value.append('FAIL')
        return_value.append(
            "/home does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_15_sus():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_16_sus():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nosuid is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_17_sus():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_18_sus():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nodev = [drive for drive in success.splitlines()
                 if 'nodev' not in drive]
        if not nodev:
            return_value.append('nodev is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nodev is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nodev" set\n'
            for n in nodev:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_19_sus():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nosuid = [drive for drive in success.splitlines()
                  if 'nosuid' not in drive]
        if not nosuid:
            return_value.append('nosuid is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nosuid is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nosuid" set\n'
            for n in nosuid:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_20_sus():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        noexec = [drive for drive in success.splitlines()
                  if 'noexec' not in drive]
        if not noexec:
            return_value.append('noexec is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('noexec is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "noexec" set\n'
            for n in noexec:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_21_sus():
    return_value = list()
    success, error = check(
        "df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null")
    if not success:
        return_value.append('sticky bit set on w-w directories')
        return_value.append('PASS')
        return_value.append(
            "running df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null confirms that all world writable directories have the sticky variable set")
    else:
        return_value.append('directories without sticky bit found')
        return_value.append('FAIL')
        return_value.append(
            'The following directories does not have their sticky bit set\n' + success)
    return return_value


def _1_1_22_sus():
    return_value = list()
    success, error = check('systemctl is-enabled autofs | grep enabled')
    if error:
        return_value.append('automounting could not be checked')
        return_value.append('CHEK')
        return_value.append(error)
    else:
        if 'enabled' in success:
            return_value.append('automounting is enabled')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            return_value.append('automounting is disabled')
            return_value.append('PASS')
            return_value.append(success)
    return return_value


"""
Definitions of Functions that perform Ubuntu checks against benchmarks
return_value[0] = result
return_value[1] = PASS/FAIL/CHEK
return_value[2] = success/error message
Goto line "156" in order to view definition of test()
"""


def _1_1_1_1_ubu():
    return_value = list()
    success, error = check('modprobe -n -v cramfs')
    if 'insmod' in success:
        return_value.append('cramfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep cramfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('cramfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('cramfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('cramfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_2_ubu():
    return_value = list()
    success, error = check('modprobe -n -v freevxfs')
    if 'insmod' in success:
        return_value.append('freevxfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep freevxfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('freevxfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('freevxfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('freevxfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_3_ubu():
    return_value = list()
    success, error = check('modprobe -n -v jffs2')
    if 'insmod' in success:
        return_value.append('jffs2 can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep jffs2')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('jffs2 cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('jffs2 is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('jffs2 mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_4_ubu():
    return_value = list()
    success, error = check('modprobe -n -v hfs')
    if 'insmod' in success:
        return_value.append('hfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_5_ubu():
    return_value = list()
    success, error = check('modprobe -n -v hfsplus')
    if 'insmod' in success:
        return_value.append('hfsplus can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep hfsplus')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('hfsplus cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('hfsplus is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('hfsplus mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_6_ubu():
    return_value = list()
    success, error = check('modprobe -n -v squashfs')
    if 'insmod' in success:
        return_value.append('squashfs can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep squashfs')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('squashfs cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('squashfs is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('squashfs mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_7_ubu():
    return_value = list()
    success, error = check('modprobe -n -v udf')
    if 'insmod' in success:
        return_value.append('udf can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep udf')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('udf cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('udf is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('udf mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_1_8_ubu():
    return_value = list()
    success, error = check('grep -i vfat /etc/fstab')
    if success:
        return_value.append('vfat is mounted')
        return_value.append('CHEK')
        return_value.append(success)
    else:
        success, error = check('modprobe -n -v vfat')
        if 'insmod' in success:
            return_value.append('vfat can be mounted')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            result_success = success
            result_error = error
            success, error = check('lsmod | grep vfat')
            if 'install /bin/true' in result_success or 'not found in directory' in result_error:
                if not success:
                    return_value.append('vfat cannot be mounted')
                    return_value.append('PASS')
                    return_value.append(
                        result_success if result_success else result_error)
                else:
                    return_value.append('vfat is mounted')
                    return_value.append('FAIL')
                    return_value.append(
                        result_success if result_success else result_error + '\n' + success)
            else:
                return_value.append('vfat mount status undetermined')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


def _1_1_2_ubu():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        return_value.append('/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('/tmp is not configured')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_3_ubu():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nodev did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nodev is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_4_ubu():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v nosuid did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('nosuid is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_5_ubu():
    return_value = list()
    success, error = check("mount | grep -E '\s/tmp\s'")
    if success:
        success, error = check("mount | grep -E '\s/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/tmp\s' | grep -v noexec did not return anything")
    else:
        success, error = check('systemctl is-enabled tmp.mount')
        return_value.append('noexec is not set on /tmp')
        return_value.append('FAIL')
        return_value.append(error)
    return return_value


def _1_1_6_ubu():
    return_value = list()
    success, error = check("mount | grep -E '\s/var\s'")
    if success:
        return_value.append('/var is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep -E '\s/var\s' did not return any result")
    return return_value


def _1_1_7_ubu():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        return_value.append('/var/tmp is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/tmp is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/tmp did not return any result")
    return return_value


def _1_1_8_ubu():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_9_ubu():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_10_ubu():
    return_value = list()
    success, error = check('mount | grep /var/tmp')
    if success:
        success, error = check(
            "mount | grep -E '\s/var/tmp\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /var/tmp')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/var/tmp\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /var/tmp')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /var/tmp')
        return_value.append('FAIL')
        return_value.append(
            "/var/tmp does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_11_ubu():
    return_value = list()
    success, error = check('mount | grep /var/log')
    if success:
        return_value.append('/var/log is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /var/log did not return any result")
    return return_value


def _1_1_12_ubu():
    return_value = list()
    success, error = check('mount | grep /var/log/audit')
    if success:
        return_value.append('/var/log/audit is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/var/log/audit is not configured')
        return_value.append('FAIL')
        return_value.append(
            "mount | grep /var/log/audit did not return any result")
    return return_value


def _1_1_13_ubu():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        return_value.append('/home is configured')
        return_value.append('PASS')
        return_value.append(success)
    else:
        return_value.append('/home is not configured')
        return_value.append('FAIL')
        return_value.append("mount | grep /home did not return any result")
    return return_value


def _1_1_14_ubu():
    return_value = list()
    success, error = check('mount | grep /home')
    if success:
        success, error = check("mount | grep -E '\s/home\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /home')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/home\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /home')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /home')
        return_value.append('FAIL')
        return_value.append(
            "/home does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_15_ubu():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nodev")
        if not success and not error:
            return_value.append('nodev is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nodev did not return anything")
        else:
            return_value.append('nodev is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('nodev is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nodev cannot be set on a partition that does not exist")
    return return_value


def _1_1_16_ubu():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v nosuid")
        if not success and not error:
            return_value.append('nosuid is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v nosuid did not return anything")
        else:
            return_value.append('nosuid is not set on /dev/shm')
            return_value.append('PASS')
            return_value.append(success if success else error)
    else:
        return_value.append('nosuid is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. nosuid cannot be set on a partition that does not exist")
    return return_value


def _1_1_17_ubu():
    return_value = list()
    success, error = check('mount | grep /dev/shm')
    if success:
        success, error = check(
            "mount | grep -E '\s/dev/shm\s' | grep -v noexec")
        if not success and not error:
            return_value.append('noexec is set on /dev/shm')
            return_value.append('PASS')
            return_value.append(
                "mount | grep -E '\s/dev/shm\s' | grep -v noexec did not return anything")
        else:
            return_value.append('noexec is not set on /dev/shm')
            return_value.append('FAIL')
            return_value.append(success if success else error)
    else:
        return_value.append('noexec is not set on /dev/shm')
        return_value.append('FAIL')
        return_value.append(
            "/dev/shm does not exist. noexec cannot be set on a partition that does not exist")
    return return_value


def _1_1_18_ubu():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nodev = [drive for drive in success.splitlines()
                 if 'nodev' not in drive]
        if not nodev:
            return_value.append('nodev is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nodev is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nodev" set\n'
            for n in nodev:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_19_ubu():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        nosuid = [drive for drive in success.splitlines()
                  if 'nosuid' not in drive]
        if not nosuid:
            return_value.append('nosuid is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('nosuid is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "nosuid" set\n'
            for n in nosuid:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_20_ubu():
    return_value = list()
    success, error = check("mount | grep -e '/media/'")
    if success:
        noexec = [drive for drive in success.splitlines()
                  if 'noexec' not in drive]
        if not noexec:
            return_value.append('noexec is set on all removable drives')
            return_value.append('PASS')
            return_value.append(success)
        else:
            return_value.append('noexec is not set on all removable drives')
            return_value.append('FAIL')
            result = 'The following removable storage media does not have "noexec" set\n'
            for n in noexec:
                result += n + '\n'
            return_value.append(result)
    else:
        return_value.append('No mounted media found')
        return_value.append('PASS')
        return_value.append("mount | grep -e '/media/' returned no result")
    return return_value


def _1_1_21_ubu():
    return_value = list()
    success, error = check(
        "df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null")
    if not success:
        return_value.append('sticky bit set on w-w directories')
        return_value.append('PASS')
        return_value.append(
            "running df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null confirms that all world writable directories have the sticky variable set")
    else:
        return_value.append('directories without sticky bit found')
        return_value.append('FAIL')
        return_value.append(
            'The following directories does not have their sticky bit set\n' + success)
    return return_value


def _1_1_22_ubu():
    return_value = list()
    success, error = check('systemctl is-enabled autofs | grep enabled')
    if error:
        return_value.append('automounting could not be checked')
        return_value.append('CHEK')
        return_value.append(error)
    else:
        if 'enabled' in success:
            return_value.append('automounting is enabled')
            return_value.append('FAIL')
            return_value.append(success)
        else:
            return_value.append('automounting is disabled')
            return_value.append('PASS')
            return_value.append(success)
    return return_value


def _1_1_23_ubu():
    return_value = list()
    success, error = check('modprobe -n -v usb-storage')
    if 'insmod' in success:
        return_value.append('usb-storage can be mounted')
        return_value.append('FAIL')
        return_value.append(success)
    else:
        result_success = success
        result_error = error
        success, error = check('lsmod | grep usb-storage')
        if 'install /bin/true' in result_success or 'not found in directory' in result_error:
            if not success:
                return_value.append('usb-storage cannot be mounted')
                return_value.append('PASS')
                return_value.append(
                    result_success if result_success else result_error)
            else:
                return_value.append('usb-storage is mounted')
                return_value.append('FAIL')
                return_value.append(
                    result_success if result_success else result_error + '\n' + success)
        else:
            return_value.append('usb-storage mount status undetermined')
            return_value.append('PASS')
            return_value.append(
                result_success if result_success else result_error + '\n' + success + '\n' + error)
    return return_value


# function to call necessary recommendation benchmarks
# i (current benchmark number) and l (total benchmarks scored)
# are only used when output is not required verbose-ly
# i.e. to print progressBar
def test(r, file_path, dist, i=None, l=None):
    start = time()

    return_value = eval('_' + r[0].replace('.', '_') + '_' + dist + '()')

    # return_score is 2 when test has passed (1) AND the test is scored (1)
    return_score = 0
    if 'PASS' == return_value[1] and r[1]:
        return_score = 2
    elif 'PASS' == return_value[1]:
        return_score = 1

    # if verbose output is needed | else print progressBar
    if i == None and l == None:
        if r[1]:
            print_success(r[0], return_value[0], return_value[1]) if return_score == 2 else print_fail(
                r[0], return_value[0], return_value[1])
        else:
            print_neutral(r[0], return_value[
                          0], return_value[1])
    else:
        printProgressBar(i, l, prefix='Progress:',
                         suffix='Complete', autosize=True) if i == l else printProgressBar(i, l, prefix=r[0] + ' (' + str(i) + '/' + str(l) + ')',
                                                                                           suffix='Complete', autosize=True)

    # writing findings to .SeBAz file
    return_value.insert(0, r[0])
    return_value.append(str(time() - start))
    with open(file_path, 'a', newline='') as csvfile:
        csvwriter = writer(csvfile, dialect='excel')
        csvwriter.writerow(return_value)

    # returning score
    return return_score


if __name__ == "__main__":
    exit('Please run ./SeBAz -h')
