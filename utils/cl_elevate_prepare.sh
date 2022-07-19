#!/bin/bash

yum install -y http://repo.almalinux.org/elevate/elevate-release-latest-el7.noarch.rpm
yum install -y leapp-upgrade leapp-data-almalinux git nano

git clone -b cloudlinux --single-branch https://github.com/prilr/leapp-repository.git /root/leapp-repository-cloudlinux
git clone -b 3rd_parties --single-branch https://github.com/prilr/leapp-repository.git /root/leapp-repository-3rd_parties

yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/libraries/config/version.py /etc/leapp/repos.d/system_upgrade/common/libraries/config/version.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/actors/ipuworkflowconfig/libraries/ipuworkflowconfig.py /etc/leapp/repos.d/system_upgrade/common/actors/ipuworkflowconfig/libraries/ipuworkflowconfig.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/actors/redhatsignedrpmscanner/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/redhatsignedrpmscanner/actor.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/models/targetsystemtype.py /etc/leapp/repos.d/system_upgrade/common/models/targetsystemtype.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/actors/scancustomrepofile/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/scancustomrepofile/actor.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/actors/scancustomrepofile/libraries/scancustomrepofile.py /etc/leapp/repos.d/system_upgrade/common/actors/scancustomrepofile/libraries/scancustomrepofile.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/actors/setuptargetrepos/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/setuptargetrepos/actor.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/actors/networkmanagerupdateconnections/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/networkmanagerupdateconnections/actor.py
yes | cp -f /root/leapp-repository-cloudlinux/repos/system_upgrade/common/actors/networkmanagerupdateconnections/tools/nm-update-client-ids.py /etc/leapp/repos.d/system_upgrade/common/actors/networkmanagerupdateconnections/tools/nm-update-client-ids.py

mkdir /etc/leapp/repos.d/system_upgrade/common/actors/checkenabledvendorrepos
mkdir -p /etc/leapp/repos.d/system_upgrade/common/actors/scanvendorrepofiles/libraries
mkdir /etc/leapp/repos.d/system_upgrade/common/actors/vendorrepositoriesmapping

yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/actors/checkenabledvendorrepos/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/checkenabledvendorrepos/actor.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/actors/peseventsscanner/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/peseventsscanner/actor.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/actors/peseventsscanner/libraries/peseventsscanner.py /etc/leapp/repos.d/system_upgrade/common/actors/peseventsscanner/libraries/peseventsscanner.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/actors/repositoriesmapping/libraries/repositoriesmapping.py /etc/leapp/repos.d/system_upgrade/common/actors/repositoriesmapping/libraries/repositoriesmapping.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/actors/scanvendorrepofiles/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/scanvendorrepofiles/actor.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/actors/scanvendorrepofiles/libraries/scanvendorrepofiles.py /etc/leapp/repos.d/system_upgrade/common/actors/scanvendorrepofiles/libraries/scanvendorrepofiles.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/actors/vendorrepositoriesmapping/actor.py /etc/leapp/repos.d/system_upgrade/common/actors/vendorrepositoriesmapping/actor.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/libraries/repomaputils.py /etc/leapp/repos.d/system_upgrade/common/libraries/repomaputils.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/models/activevendorlist.py /etc/leapp/repos.d/system_upgrade/common/models/activevendorlist.py
yes | cp -f /root/leapp-repository-3rd_parties/repos/system_upgrade/common/models/repositoriesmap.py /etc/leapp/repos.d/system_upgrade/common/models/repositoriesmap.py

yes | cp -R /etc/leapp/repos.d/system_upgrade/common/files/prod-certs/8.4 /etc/leapp/repos.d/system_upgrade/common/files/prod-certs/8.6
yes | cp -R /root/leapp-repository-cloudlinux/repos/system_upgrade/cloudlinux /etc/leapp/repos.d/system_upgrade/cloudlinux

git clone -b 3rd_parties --single-branch https://github.com/prilr/leapp-data.git /root/leapp-data
rsync -a /root/leapp-data/files/cloudlinux/ /etc/leapp/files/

LEAPP_DEVEL_USE_PERSISTENT_PACKAGE_CACHE=1
LEAPP_DEVEL_TARGET_PRODUCT_TYPE=ga
# LEAPP_DEVEL_RPMS_ALL_SIGNED=1

rmmod floppy pata_acpi btrfs
echo PermitRootLogin yes | tee -a /etc/ssh/sshd_config
leapp answer --add --section remove_pam_pkcs11_module_check.confirm=True
leapp answer --add --section select_target_system_type.select=stable

echo -e "\nYou now can run \"leapp upgrade\"!\n"