from ._base_endpoint import EndpointWrapper
from datetime import datetime, timedelta
import logging


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "sales"

	def __init__(self):
		super().__init__()
		# Endpoints
		self.syncOnlineSales = self.__SV_WRITE__.syncOnlineSales
		self.syncShippedSaleAndRemoveItems = self.__SV_WRITE__.syncShippedSaleAndRemoveItems

	# DQL METHODS
	def _get(self, from_dt, to_dt, **kwargs):
		return self.__SV_READ__.get_sales_for_date_range(from_dt, to_dt)

	# DML METHODS
	def _send(self, sales_list):
		"""SyncOnlineSale handles de-duplication to simplify this method."""
		logger = logging.getLogger(__name__)
		logger.info("Sending '{}' sales to SkuVault.".format(len(sales_list)))
		for s_ in sales_list:
			sale_ = self.syncOnlineSales.new()
			sale_.update(**s_)
		self.syncOnlineSales.send_all_skuvault()
Sales = Handle
