clearpart --all --initlabel
bootloader --append="console=ttyS0 quiet" --timeout=1

part biosboot --size=1
part /boot --size=512 --fstype ext4 --label=Boot --asprimary

part pv.01 --size 5000
volgroup HostVG pv.01
logvol /config --vgname=HostVG --size=64 --name=Config --fstype=ext4
logvol none --vgname=HostVG --size=4000 --name=ImagePool --thinpool --chunksize=128 --metadatasize=4
logvol / --vgname=HostVG --size=3000 --name=Image-0.0 --thin --poolname=ImagePool --fstype=ext4 --fsoptions=discard

# We assume that no overprovisioning is happening
#logvol swap --vgname=HostVG --fstype=swap --size=1024