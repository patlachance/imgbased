
#
# Packages
#
%packages --excludedocs --ignoremissing
@core

# Only available in Fedora 20+
#anaconda-core
#anaconda-tui

# lvm - for sure
lvm2

# config generic == hostonly, this is needed
# to support make a generic image (do not keep lvm informations in the image)
dracut-config-generic

# EFI support
grub2-efi
shim
efibootmgr

# Configuration management
#puppet
#salt

# Some tools
vim-minimal
augeas
tmux
%end