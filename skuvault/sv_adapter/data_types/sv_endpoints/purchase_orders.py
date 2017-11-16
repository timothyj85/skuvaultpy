from ._base_endpoint import EndpointWrapper
from datetime import datetime, timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "purchase_orders"

	def __init__(self):
		super().__init__()
		# Endpoints
		self.createPO = self.__SV_WRITE__.createPO

	# DQL METHODS
	def _get(self, ModifiedAfterDateTimeUtc, ModifiedBeforeDateTimeUtc, **kwargs):
		after_dt_str = from_utc_dt.isoformat()
		before_dt_str = to_utc_dt.isoformat()
		all_pos = list()
		# DOWNLOAD ALL ORDERS (COMPLETED EXCLUDED BY DEFAULT)
		all_pos.extend(
			self.__SV_READ__.getPOs.paged(ModifiedAfterDateTimeUtc=after_dt_str, ModifiedBeforeDateTimeUtc=before_dt_str)
		)
		# DOWNLOAD ALL ORDERS (ONLY GETTING COMPLETED)
		all_pos.extend(
			self.__SV_READ__.getPOs.paged(ModifiedAfterDateTimeUtc=from_utc, ModifiedBeforeDateTimeUtc=to_utc, status="Completed")
		)

	# DML METHODS
	def _send(self, **kwargs):
		raise NotImplementedError("This method is not yet available for '{}'".format(self.__ENDPOINT_NAME__))
PurchaseOrders = Handle


# TODO: Verify that isoformat() will provide the correct datetime.
