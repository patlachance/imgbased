#!/usr/bin/env python
# vim: et ts=4 sw=4 sts=4

import unittest
import sh
import logging


# Increase the capture length of python-sh to show complete errors
sh.ErrorReturnCode.truncate_cap = 999999

log = logging.info


class TestImgbased(unittest.TestCase):
    def test_imgbase(self):
        from sh import imgbase, lvm

        # All subsequent imgbase calls include the debug arg
        imgbase = imgbase.bake("--debug")

        log("Using %s" % imgbase)
        log(imgbase("--version"))

        log("Existing LVM layout")
        log(lvm.pvs())
        log(lvm.vgs())
        log(lvm.lvs())

        assert "HostVG" in lvm.vgs()

        assert "Image-0.0" in imgbase.layout()

        # Check that a current layer exists
        imgbase.layer("--current")


class TestEnvironment(unittest.TestCase):
    def test_selinux_denials(self):
        """Looking for SELinux AVC denials
        """
        from sh import getenforce
        assert getenforce().strip() in ["Enforcing", "Permissive"]
        # assert not grep("denied", "/var/log/audit.log")

    def test_relevant_packages(self):
        """Looking for mandatory packages
        """
        from sh import which
        for app in ["df", "du", "diff", "lvm"]:
            assert which(app)

    def test_mounts(self):
        """Check presence of relevant mount points
        """
        from sh import findmnt

        mnt_opt = lambda o, p: findmnt("-no", o, p, _ok_code=[1]).strip()

        assert mnt_opt("SOURCE", "/tmp") == "tmpfs", \
            "/tmp is not a tmpfs"

        assert mnt_opt("SOURCE", "/etc") == "", \
            "/etc is not on /"

        assert mnt_opt("SOURCE", "/var") != "", \
            "/var is not a separate device"

        assert "discard" in mnt_opt("OPTIONS", "/"), \
            "/ is not mounted with the discard option"
