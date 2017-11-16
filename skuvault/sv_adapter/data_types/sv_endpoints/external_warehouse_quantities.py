"""Not auto-initialized should be accessed through 'external_warehouses' Handle and not directly!"""
from ._base_endpoint import EndpointWrapper
from datetime import timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "external_warehouse_quantities"

	def __init__(self, warehouse_code, warehouse_id):
		super().__init__()
		# ENDPOINTS
		self.warehouse_code = warehouse_code
		self.warehouse_id = warehouse_id
		self.updateExternalWarehouseQuantities = self.__SV_WRITE__.updateExternalWarehouseQuantities(self.warehouse_id)

	# DQL METHODS
	def _get(self, **kwargs):
		# add warehouse_id to HTTP POST params
		kwargs["WarehouseId"] = self.warehouse_id
		return self.__SV_READ__.getExternalWarehouseQuantities.single_get(**kwargs)

	# DML METHODS
	def _send(self, **kwargs):
		raise NotImplementedError("This method is not yet available for '{}'".format(self.__ENDPOINT_NAME__))
