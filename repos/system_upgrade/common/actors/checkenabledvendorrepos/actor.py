from leapp.actors import Actor
from leapp.libraries.stdlib import api
from leapp.models import (
    RepositoriesFacts,
    VendorRepositoriesMapCollection,
    ActiveVendorList,
)
from leapp.tags import FactsPhaseTag, IPUWorkflowTag


class CheckEnabledVendorRepos(Actor):
    """
    No documentation has been provided for the check_enabled_vendor_repos actor.
    """

    name = "check_enabled_vendor_repos"
    consumes = (RepositoriesFacts, VendorRepositoriesMapCollection)
    produces = ActiveVendorList
    tags = (FactsPhaseTag, IPUWorkflowTag)

    def process(self):
        vendor_mapping_data = {}
        active_vendors = []

        # Make a dict for easy lookup of repoid -> vendor name.
        for map_coll in api.consume(VendorRepositoriesMapCollection):
            for map in map_coll.maps:
                for repo in map.repositories:
                    # Cut the .csv, keep only the vendor name.
                    vendor_mapping_data[repo.from_repoid] = map.file[:-4]

        # Is the repo listed in the vendor map as from_repoid present on the system?
        for repos in api.consume(RepositoriesFacts):
            for repo_file in repos.repositories:
                for repo in repo_file.data:
                    if repo.repoid in vendor_mapping_data:
                        # If the vendor's repository is present in the system, count the vendor as active.
                        active_vendors.append(vendor_mapping_data[repo.repoid])

        api.produce(ActiveVendorList(data=active_vendors))
