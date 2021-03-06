# -*- coding: utf-8 -*-
from schematics.types import StringType, MD5Type
from uuid import uuid4
from zope.interface import implementer, Interface
from schematics.types.compound import (
    ModelType,
)

from openprocurement.api.constants import (
    SANDBOX_MODE,
)
from openprocurement.api.models.common import (
    Period,
)
from openprocurement.api.models.auction_models import (
    Organization,
)
from openprocurement.api.models.schematics_extender import (
    IsoDateTimeType,
    ListType,
    Model,
)
from openprocurement.contracting.core.models import (
    Contract as BaseContract,
    ProcuringEntity,
)
from openprocurement.contracting.ceasefire import constants

from .roles import (
    MILESTONE_ROLES,
    CONTRACT_ROLES,
)


class ICeasefireMilestone(Interface):
    """Contract marker interface
    """


@implementer(ICeasefireMilestone)
class Milestone(Model):
    """Contract milestone
    """
    class Options:
        roles = MILESTONE_ROLES

    # named so to not override built-in method name
    id = MD5Type(required=True, default=lambda: uuid4().hex)
    dateMet = IsoDateTimeType()
    dateModified = IsoDateTimeType()
    description = StringType()
    dueDate = IsoDateTimeType()
    status = StringType(choices=constants.MILESTONE_STATUSES)
    title = StringType()
    type_ = StringType(choices=constants.MILESTONE_TYPES, serialized_name='type')


class ICeasefireContract(Interface):
    """Contract marker interface
    """


@implementer(ICeasefireContract)
class Contract(BaseContract):
    """Common Contract
    """

    class Options:
        roles = CONTRACT_ROLES

    awardID = StringType(required=True)  # overridden to make required
    suppliers = ListType(ModelType(Organization), required=True)
    contractID = StringType(required=True)  # overridden to make required
    dateSigned = IsoDateTimeType(required=True)  # overridden to make required
    contractType = StringType(required=True)  # must be generated by databridge
    milestones = ListType(ModelType(Milestone))  # generated automatically
    period = ModelType(Period)
    procuringEntity = ModelType(ProcuringEntity)  # overridden to make not required
    status = StringType(choices=constants.CONTRACT_STATUSES, default=constants.DEFAULT_CONTRACT_STATUS)
    type_ = StringType(serialized_name='type')
    merchandisingObject = StringType()  # id of related lot

    create_accreditation = 5
    edit_accreditation = 6
    _internal_type = 'ceasefire'
    if SANDBOX_MODE:
        sandbox_parameters = StringType()
