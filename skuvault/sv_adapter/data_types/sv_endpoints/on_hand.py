from ._base_endpoint import EndpointWrapper
from datetime import timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "on_hand"

	def __init__(self):
		super().__init__()
		# ENDPOINTS
		self.setItemQuantities = self.__SV_WRITE__.setItemQuantities
		self.addItemBulk = self.__SV_WRITE__.addItemBulk

	# DQL METHODS
	def _get(self, **kwargs):
		return self.__SV_READ__.getInventoryByLocation.paged(**kwargs)

	# DML METHODS
	def _send(self, **kwargs):
		raise NotImplementedError("This method is not yet available for '{}'".format(self.__ENDPOINT_NAME__))
OnHand = Handle
