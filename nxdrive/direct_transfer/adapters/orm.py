from logging import getLogger

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    JSON,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import mapper, relationship

from ..domain import model
from .. import constants

log = getLogger(__name__)

metadata = MetaData()

transfer = Table(
    "transfer",
    metadata,
    Column("uid", Integer, primary_key=True, autoincrement=True),
    Column("state", Enum(constants.SessionState), default=constants.SessionState.DRAFT),
    Column("priority", Integer, default=0),
)

# transfer_item = Table(
#     "transfer_item",
#     metadata,
#     Column("uid", Integer, primary_key=True, autoincrement=True),
#     Column("size", Integer),
#     Column("is_file", Boolean),
#     Column("transferred", Boolean),
#     Column("state", Enum(constants.TransferStatus)),
#     Column("remote_ref", Text),
#     Column("remote_path", Text),
#     Column("local_path", Text),
#     Column("batch", JSON),
#     Column("doctype", String(32)),
# )

# transfer_item_action = Table(
#     "transfer_item_action",
#     metadata,
#     Column("uid", Integer, primary_key=True, autoincrement=True),
#     Column("transfer_id", ForeignKey("transfer.uid")),
#     Column("transfer_item_id", ForeignKey("transfer_item.uid")),
#     Column("action", Enum(constants.TransferAction)),
# )

# transfer_item_error = Table(
#     "transfer_item_error",
#     metadata,
#     Column("uid", Integer, primary_key=True, autoincrement=True),
#     Column("transfer_item_id", ForeignKey("transfer_item.uid")),
#     Column("error_count", Integer),
#     Column("error_count_total", Integer),
#     Column("last_error", Text),
# )


def start_mappers():
    log.info("Starting mappers")
    transfer_mapper = mapper(model.Transfer, transfer)
    # transfer_item_mapper = mapper(
    #     model.TransferItem,
    #     transfer_item,
    #     properties={"transfer": relationship(transfer_mapper)},
    # )
    # mapper(
    #     model.TransferItemAction,
    #     transfer_item_action,
    #     properties={"transfer_item": relationship(transfer_item_mapper)},
    # )
