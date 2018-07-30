
==================================
Auditd Formula
==================================

The Linux Audit system provides a way to track security-relevant information on
your system. Based on pre-configured rules, Audit generates log entries to
record as much information about the events that are happening on your system
as possible. This information is crucial for mission-critical environments to
determine the violator of the security policy and the actions they performed.
Audit does not provide additional security to your system; rather, it can be
used to discover violations of security policies used on your system.
These violations can further be prevented by additional security
measures such as SELinux.

Please, be aware of one *feature*.
If you enable auditd.rules.rules.privileged it will dynamically generate a list
of binaries which have suid/sgid bit for all mounted file systems which do not
have **nosuid** or **noexec** mount option (except the *special* file systems
such as **sysfs**, **nsfs**, **cgroup**, **proc** and so one).
The list of such *special* file systems can be configured
with auditd:rules:filter_fs pillar.

It was done because it is nearly impossible to create that list manually. It
always will differ from one installation to another.
This behavior can not be changed but it can be extended manually by putting
necessary rules into the **rule_list** list.

Also it is possible to add paths which will be filtered in search. It implements
the idea of *white lists* but on a directory level, not for a particular file.
It can be configured with auditd:rules:filter_paths pillar.


Sample Metadata
===============

Single auditd service

.. code-block:: yaml
  auditd:
    service:
      enabled: true
      log_file: /var/log/audit/audit.log
      log_format: NOLOG
      log_group: root
      priority_boost: 4
      flush: INCREMENTAL
      freq: 20
      num_logs: 5
      disp_qos: lossy
      dispatcher: /sbin/audispd
      name_format: HOSTNAME
      max_log_file: 6
      max_log_file_action: ROTATE
      space_left: 75
      space_left_action: SYSLOG
      action_mail_acct: root
      admin_space_left: 50
      admin_space_left_action: SUSPEND
      disk_full_action: SUSPEND
      disk_error_action: SUSPEND
      tcp_listen_queue: 5
      tcp_max_per_addr: 1
      tcp_client_max_idle: 0
      enable_krb5: 'no'
      krb5_principal: auditd
    audisp:
      enabled: true
    rules:
      options:
        enabled: 0
        bufsize: 8192
      rules:
        1:
          key: some_rule_key
          enabled: true
          rule_list:
            - '-w /etc/passwd -p wa'
            - '-a always,exit -F arch=b64 -S mount'

Auditd service with syslog plugin configuration

.. code-block:: yaml

  auditd:
    service:
      enabled: true
      log_format: NOLOG
      ...
    audisp:
      enabled: true
      plugins:
        syslog:
          active: 'yes'
          direction: out
          path: builtin_syslog
          type: builtin
          args: 'LOG_INFO LOG_LOCAL6'
          format: string

References
=========
https://github.com/linux-audit/audit-documentation/wiki
https://linux-audit.com
https://github.com/linux-audit/audit-userspace

Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use GitHub issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-auditd/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

You should also subscribe to mailing list (salt-formulas@freelists.org):

    https://www.freelists.org/list/salt-formulas

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net
