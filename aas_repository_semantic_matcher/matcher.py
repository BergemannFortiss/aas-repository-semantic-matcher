import dataclasses
from typing import Optional, Dict, Set

from basyx.aas import model
from basyx.aas.util import traversal
import aas_python_http_client as aas_client

import xmlization


@dataclasses.dataclass
class SemanticIndexElement:
    """
    A Semantic Index Element

    :attr: semantically_identified_referable: The Referable that the semanticID is
        attached to
    :attr: parent_identifiable: The Identifiable that is the parent of the Referable.
        Typically, a Submodel. If the semantic ID is attached to the Submodel itsself,
        `semantically_identified_referable` and `parent_identifiable` will both point
        to the Submodel
    :attr: parent_asset_administration_shell: The Asset Administration Shell that
        contains the Identifiable that contains the Referable the semanticID is
        attached to, if it exists
    """
    semantically_identified_referable: model.Referable
    parent_identifiable: model.Identifier
    parent_asset_administration_shell: Optional[model.Identifier] = None

    def __hash__(self):
        return hash((self.semantically_identified_referable, self.parent_identifiable))


class AASRepositoryMatcher:
    def __init__(self, repository_endpoint: str):
        self.repository_endpoint: str = repository_endpoint
        self.semantic_id_index: Dict[model.ExternalReference, Set[SemanticIndexElement]] = {}

        self._api_configuration = aas_client.Configuration()
        self._api_configuration.host = self.repository_endpoint
        self._api_client = aas_client.ApiClient(self._api_configuration)
        self._submodel_repo_client = aas_client.SubmodelRepositoryAPIApi(self._api_client)

        print("Indexing, please wait")
        self.index_repository_server()
        print("Index complete")

    def _add_semantic_id_to_index(
            self,
            semantic_id: model.Key,
            referable: model.Referable,
            parent_identifiable: model.Identifier,
            parent_aas: Optional[model.Identifier] = None
    ):
        """
        Adds a semanticID's Key to the index
        """
        if self.semantic_id_index.get(semantic_id) is None:
            self.semantic_id_index[semantic_id] = {
                SemanticIndexElement(
                    referable,
                    parent_identifiable,
                    parent_aas
                )
            }
            return
        else:
            self.semantic_id_index[semantic_id].add(
                SemanticIndexElement(
                    referable,
                    parent_identifiable,
                    parent_aas
                )
            )

    def _index_semantic_ids_in_submodel(
            self,
            submodel: model.Submodel,
            submodel_identifier: model.Identifier,
            aas_identifier: Optional[model.Identifier] = None
    ):
        if submodel.semantic_id is not None:
            for key in submodel.semantic_id.key:
                self._add_semantic_id_to_index(
                    semantic_id=key,
                    referable=submodel,
                    parent_identifiable=submodel_identifier,
                    parent_aas=aas_identifier
                )
        for submodel_element in traversal.walk_submodel(submodel):
            if submodel_element.semantic_id:
                for key in submodel_element.semantic_id.key:
                    self._add_semantic_id_to_index(
                        semantic_id=key,
                        referable=submodel_element,
                        parent_identifiable=submodel_identifier,
                        parent_aas=aas_identifier
                    )

    def _add_submodel_to_semantic_id_index(self, submodel: model.Submodel):
        submodel_identifier: model.Identifier = submodel.id
        self._index_semantic_ids_in_submodel(
            submodel=submodel,
            submodel_identifier=submodel_identifier,
            aas_identifier=None
        )

    def index_repository_server(self):
        # Here's the idea:
        # Reset the semantic_id_index
        # Get all Submodels from the Repository
        # Walk each submodel
        # Add each SubmodelElement to the Index
        self.semantic_id_index = {}
        for submodel in self._submodel_repo_client.get_all_submodels().result:
            self._add_submodel_to_semantic_id_index(submodel)

    def print_matches(self):
        # Here's the idea:
        # Each key of the semantic_id_index is the set of semantically equivalent SubmodelElements
        # (Under the assumption of only exact matching)
        for key, value in self.semantic_id_index.items():
            print(key)
            for i in value:
                print(f"\t{i}")

    def matches_to_xml(self) -> str:
        # Write the semantic_id_index to the standardized XML string
        root = xmlization.create_root()
        for index_key, index_elements in self.semantic_id_index.items():
            link = xmlization.add_link(
                root,
                link_type="Equivalence",
                comment="tbd"  # Todo
            )
            for index_element in index_elements:
                xmlization.add_element(
                    link=link,
                    element_id="todo",  # Todo: Determine idShort Path of the Element
                    name=f"{index_element.semantically_identified_referable.__class__.__name__}",
                    model="tbd",  # Todo
                    tool="BaSyx"
                )
        return xmlization.write_xml_to_string(root)


if __name__ == "__main__":
    matcher = AASRepositoryMatcher("http://localhost:8080/api/v3.0")
    print(matcher.matches_to_xml())
