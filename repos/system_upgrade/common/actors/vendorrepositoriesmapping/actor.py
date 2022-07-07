from leapp.actors import Actor
from leapp.libraries.common.repomaputils import scan_vendor_repomaps, VENDOR_REPOMAP_DIR
from leapp.models import VendorRepositoriesMapCollection
from leapp.tags import FactsPhaseTag, IPUWorkflowTag
from leapp.libraries.stdlib import api


class VendorRepositoriesMapping(Actor):
    """
    Scan the vendor repository mapping files and provide the data to other actors.
    """

    name = "vendor_repositories_mapping"
    consumes = ()
    produces = (VendorRepositoriesMapCollection,)
    tags = (IPUWorkflowTag, FactsPhaseTag)

    def process(self):
        vendor_repomap_collection = scan_vendor_repomaps(VENDOR_REPOMAP_DIR)
        api.produce(vendor_repomap_collection)
