import os

from leapp.libraries.stdlib import api

AWS_MAP = {
    'el7_pkg': 'rh-amazon-rhui-client',
    'el8_pkg': 'rh-amazon-rhui-client',
    'leapp_pkg': 'leapp-rhui-aws',
    'leapp_pkg_repo': 'leapp-aws.repo'
}

AWS_MAP_SAP = {
    'el7_pkg': 'rh-amazon-rhui-client-sap-bundle',
    'el8_pkg': 'rh-amazon-rhui-client-sap-bundle-e4s',
    'leapp_pkg': 'leapp-rhui-aws-sap-e4s',
    'leapp_pkg_repo': 'leapp-aws-sap-e4s.repo'
}

AZURE_MAP = {
    'el7_pkg': 'rhui-azure-rhel7',
    'el8_pkg': 'rhui-azure-rhel8',
    'agent_pkg': 'WALinuxAgent',
    'leapp_pkg': 'leapp-rhui-azure',
    'leapp_pkg_repo': 'leapp-azure.repo'
}

AZURE_MAP_SAP = {
    'el7_pkg': 'rhui-azure-rhel7-base-sap-ha',
    'el8_pkg': 'rhui-azure-rhel8-sap-ha',
    'agent_pkg': 'WALinuxAgent',
    'leapp_pkg': 'leapp-rhui-azure-sap',
    'leapp_pkg_repo': 'leapp-azure-sap.repo'
}

# for the moment the only difference in RHUI package naming is on ARM
AWS_MAP_AARCH64 = dict(AWS_MAP, el7_pkg='rh-amazon-rhui-client-arm')

RHUI_CLOUD_MAP = {
    'x86_64': {
        'aws': AWS_MAP,
        'aws-sap-e4s': AWS_MAP_SAP,
        'azure': AZURE_MAP,
        'azure-sap': AZURE_MAP_SAP,
    },
    'aarch64': {
        'aws': AWS_MAP_AARCH64,
        'aws-sap-e4s': AWS_MAP_SAP,
        'azure': AZURE_MAP,
        'azure-sap': AZURE_MAP_SAP,
    },
    'ppc64le': {
        'aws': AWS_MAP,
        'aws-sap-e4s': AWS_MAP_SAP,
        'azure': AZURE_MAP,
        'azure-sap': AZURE_MAP_SAP,
    },
    's390x': {
        'aws': AWS_MAP,
        'aws-sap-e4s': AWS_MAP_SAP,
        'azure': AZURE_MAP,
        'azure-sap': AZURE_MAP_SAP,
    },
}

# when on AWS, we need also Python2 version of "Amazon-id" dnf plugin which is served by
# "leapp-rhui-aws" rpm package (please note this package is not in any RH official repository
# but only in "rhui-client-config-*" repo)
# IMPORTANT: Deprecated DNF_PLUGIN_PATH
DNF_PLUGIN_PATH = '/usr/lib/python2.7/site-packages/dnf-plugins/'
YUM_REPOS_PATH = '/etc/yum.repos.d'

RHUI_PKI_DIR = '/etc/pki/rhui'
RHUI_PKI_PRODUCT_DIR = os.path.join(RHUI_PKI_DIR, 'product')
RHUI_PKI_PRIVATE_DIR = os.path.join(RHUI_PKI_DIR, 'private')

AWS_DNF_PLUGIN_NAME = 'amazon-id.py'

# these files are provided by special Leapp rpms (per cloud) and
# are delivered into "repos/system_upgrade/el7toel8/files/rhui/<PROVIDER>


def gen_rhui_files_map():

    arch = api.current_actor().configuration.architecture

    return {
        'aws': [
            ('rhui-client-config-server-8.crt', RHUI_PKI_PRODUCT_DIR),
            ('rhui-client-config-server-8.key', RHUI_PKI_DIR),
            ('content-rhel8.crt', RHUI_PKI_PRODUCT_DIR),
            ('content-rhel8.key', RHUI_PKI_DIR),
            ('cdn.redhat.com-chain.crt', RHUI_PKI_DIR),
            (AWS_DNF_PLUGIN_NAME, DNF_PLUGIN_PATH),
            (RHUI_CLOUD_MAP[arch]['aws']['leapp_pkg_repo'], YUM_REPOS_PATH)
        ],
        'aws-sap-e4s': [
            ('rhui-client-config-server-8-sap-bundle.crt', RHUI_PKI_PRODUCT_DIR),
            ('rhui-client-config-server-8-sap-bundle.key', RHUI_PKI_DIR),
            ('content-rhel8-sap.crt', RHUI_PKI_PRODUCT_DIR),
            ('content-rhel8-sap.key', RHUI_PKI_DIR),
            ('cdn.redhat.com-chain.crt', RHUI_PKI_DIR),
            (AWS_DNF_PLUGIN_NAME, DNF_PLUGIN_PATH),
            (RHUI_CLOUD_MAP[arch]['aws-sap-e4s']['leapp_pkg_repo'], YUM_REPOS_PATH)
        ],
        'azure': [
            ('content.crt', RHUI_PKI_PRODUCT_DIR),
            ('key.pem', RHUI_PKI_PRIVATE_DIR),
            (RHUI_CLOUD_MAP[arch]['azure']['leapp_pkg_repo'], YUM_REPOS_PATH)
        ],
        'azure-sap': [
            ('content-rhel8-sap-ha.crt', RHUI_PKI_PRODUCT_DIR),
            ('key-rhel8-sap-ha.pem', RHUI_PKI_DIR),
            (RHUI_CLOUD_MAP[arch]['azure-sap']['leapp_pkg_repo'], YUM_REPOS_PATH)
        ],
    }


def copy_rhui_data(context, provider):

    rhui_dir = api.get_common_folder_path('rhui')
    data_dir = os.path.join(rhui_dir, provider)

    context.call(['mkdir', '-p', RHUI_PKI_PRODUCT_DIR])
    context.call(['mkdir', '-p', RHUI_PKI_PRIVATE_DIR])

    for path_ in gen_rhui_files_map().get(provider, ()):
        context.copy_to(os.path.join(data_dir, path_[0]), path_[1])
