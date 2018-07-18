"""
Module for finding executable files with suid or sgid bit.
It was implemented in opposite to using __salt__[cmd.run](find)
due to complexity of filter logic in audit rules template.
"""

import multiprocessing.dummy
import functools
import logging
import stat
import os
import salt.utils

log = logging.getLogger(__name__)

def __virtual__():
    if salt.utils.is_windows():
        return False
    return 'auditd'

def _find_privileged_files(path, filtered=None, mounts=None):
    """Find executable files with suid or sbig bit.
    The function accepts list of paths wich will be skiped in search.
    """

    mounts = mounts or []
    filtered = filtered or []
    e_bits = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    s_bits = stat.S_ISUID | stat.S_ISGID

    for root, dirs, files in os.walk(path, topdown=True):
        if (root in mounts and root != path) or root in filtered:
            # Filter all mount points which lies down of the path
            # (implements the `-xdev` of the find command),
            # as well as all "filtered" paths (`-prune`/`-not`).
            dirs[:] = []
            files[:] = []
        for fname in files:
            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue
            mode = os.stat(fpath).st_mode
            if (mode & e_bits) and (mode & s_bits):
                yield fpath

def find_privileged(filter_fs=None, filter_paths=None, filter_mounts=True):

    filter_fs = filter_fs or []
    filtered = filter_paths or []
    mounts = []

    for part, mount_opts in __salt__['mount.active']().items():
        if mount_opts['fstype'] in filter_fs:
            # Must be skipped according to the fstype filter.
            log.debug("Add '%s' to filtered (filtered fs)", part)
            filtered.append(part)
            continue
        if filter_mounts:
            if set(['noexec', 'nosuid']) & set(mount_opts['opts']):
                # It has noexec/nosuid option in mount options.
                # Must be skipped.
                log.debug("Add '%s' to filtered (mount options)", part)
                filtered.append(part)
                continue
        if part == '/':
            continue
        mounts.append(part)

    # Collect all directories for parallel scanning
    scan_dirs = ['/'+d for d in os.listdir('/') if os.path.isdir('/'+d)]

    # Add all mount points into the scan dirs list
    for mount_point in mounts:
        if mount_point in scan_dirs:
            # It is already in the scan list
            continue
        if any([mount_point.startswith(f) for f in filtered]):
            # Such mount point must be skipped
            # (implements `-prune`/`-not` behavior of the find command)
            continue
        scan_dirs.append(mount_point)

    pool = multiprocessing.dummy.Pool(len(scan_dirs))
    find = functools.partial(_find_privileged_files,
                             filtered=filtered,
                             mounts=mounts)

    p = pool.map_async(find, scan_dirs)

    return sorted([item for res in p.get() for item in res])
