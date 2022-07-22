from leapp.actors import Actor
from leapp.libraries.actor import scanvendorrepofiles
from leapp.models import CustomTargetRepository, CustomTargetRepositoryFile, ActiveVendorList
from leapp.tags import FactsPhaseTag, IPUWorkflowTag
from leapp.libraries.stdlib import api


class ScanVendorRepofiles(Actor):
    """ """

    name = "scan_vendor_repofiles"
    consumes = (ActiveVendorList)
    produces = (CustomTargetRepository, CustomTargetRepositoryFile)
    tags = (FactsPhaseTag.After, IPUWorkflowTag)

    def process(self):
        scanvendorrepofiles.process()
