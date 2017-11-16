"""Gets the list of external warehouses.
NOTE: Doubles as method for getting an External Warehouse instance."""
from .external_warehouse_quantities import Handle as ExtWh
from ._base_endpoint import EndpointWrapper
from datetime import timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "external_warehouses"

	def __init__(self):
		super().__init__()

		# tracks loaded ext wh instances
		self._instances = dict()

	# DQL METHODS
	def _get(self, **kwargs):
		return self.__SV_READ__.getExternalWarehouses.single_get()

	def send_all_skuvault(self):
		for _inst in self._instances.values():
			_inst.send_all_skuvault()

	def get_external_warehouse(self, warehouse_id=None, warehouse_code=None):
		ext_whs = list(self.get_now().values())
		if warehouse_code is None and warehouse_id is None:
			raise ValueError("Either warehouse_code or warehouse_id is required!")

		if warehouse_code is not None:
			matches = [w["Id"] for w in ext_whs if w["Code"] == warehouse_code]
			if not matches:
				raise ValueError("External WarehouseCode '{}' is not valid for this account!".format(warehouse_code))
			warehouse_id = matches[0]
		else:
			matches = [w["Id"] for w in ext_whs if w["Id"] == warehouse_id]
			if not matches:
				raise ValueError("External WarehouseId '{}' is not valid for this account!".format(warehouse_id))
			warehouse_code = matches[0]

		if warehouse_id not in self._instances:
			self._instances[warehouse_id] = ExtWh(
				warehouse_code=warehouse_code,
				warehouse_id=warehouse_id
			)
		return self._instances[warehouse_id]
ExternalWarehouses = Handle
