#!/bin/bash

yum install -y http://repo.almalinux.org/elevate/elevate-release-latest-el7.noarch.rpm
yum install -y leapp-upgrade leapp-data-almalinux

git clone -b 3rd_parties --single-branch https://github.com/prilr/leapp-repository.git /root/leapp-repository

rsync -a /root/leapp-repository/repos/system_upgrade /etc/leapp/repos.d/system_upgrade
yes | cp -R /root/leapp-repository/repos/system_upgrade/cloudlinux /etc/leapp/repos.d/system_upgrade/cloudlinux

yes | cp -R /etc/leapp/repos.d/system_upgrade/common/files/prod-certs/8.4 /etc/leapp/repos.d/system_upgrade/common/files/prod-certs/8.6

git clone -b 3rd_parties --single-branch https://github.com/prilr/leapp-data.git /root/leapp-data
rsync -a /root/leapp-data/files/cloudlinux/ /etc/leapp/files/

rmmod floppy pata_acpi btrfs
echo PermitRootLogin yes | tee -a /etc/ssh/sshd_config
leapp answer --add --section remove_pam_pkcs11_module_check.confirm=True
leapp answer --add --section select_target_system_type.select=stable

echo -e "\nYou now can run \"leapp upgrade\"!\n"