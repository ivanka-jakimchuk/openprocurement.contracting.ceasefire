# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    APIResource,
    context_unpack,
    json_view,
)
from openprocurement.contracting.core.utils import (
    apply_patch,
    contractingresource,
)
from openprocurement.contracting.ceasefire.constants import (
    CONTRACT_TYPE,
    ENDPOINTS,
)
from openprocurement.contracting.core.validation import (
    validate_patch_contract_data,
)
from openprocurement.contracting.core.interfaces import (
    IContractManager,
)


@contractingresource(
    name='Ceasefire contracts',
    path=ENDPOINTS['contracts'],
    collection_path=ENDPOINTS['contracts_collection'],
    contractType=CONTRACT_TYPE)
class CeasefireContractResource(APIResource):

    @json_view(permission='view_contract')
    def get(self):
        return {'data': self.request.context.serialize("view")}

    @json_view(
        permission='edit_contract',
        validators=(validate_patch_contract_data,)
    )
    def patch(self):
        manager = self.request.registry.getAdapter(self.request.context, IContractManager)
        manager.change_contract(self.request)
        if apply_patch(self.request):
            self.LOGGER.info(
                'Updated ceasefire contract {}'.format(
                    self.request.context.id
                ),
                extra=context_unpack(
                    self.request,
                    {'MESSAGE_ID': 'ceasefire_contract_patch'}
                    )
                )
            return {'data': self.request.context.serialize()}