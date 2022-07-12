from leapp.actors import Actor
from leapp.libraries.actor import scanvendorrepofiles
from leapp.models import CustomTargetRepository, TargetSystemType, ActiveVendorList
from leapp.tags import FactsPhaseTag, IPUWorkflowTag
from leapp.libraries.stdlib import api


class ScanVendorRepofiles(Actor):
    """ """

    name = "scan_vendor_repofiles"
    consumes = (TargetSystemType, ActiveVendorList)
    produces = CustomTargetRepository
    tags = (FactsPhaseTag.After, IPUWorkflowTag)

    def process(self):
        type_message = next(api.consume(TargetSystemType), None)
        if not type_message:
            api.current_logger().info(
                ("The current configuration does not provide a target system type, assuming stable")
            )
            target_type = "stable"
        else:
            target_type = type_message.system_type

        scanvendorrepofiles.process(target_type)
