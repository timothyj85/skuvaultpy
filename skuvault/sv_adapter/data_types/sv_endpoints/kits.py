from ._base_endpoint import EndpointWrapper
from datetime import timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "kits"

	def __init__(self):
		super().__init__()

	# DQL METHODS
	def _get(self, **kwargs):
		return self.__SV_READ__.getKits.paged(**kwargs)

	# DML METHODS
	def _send(self, **kwargs):
		raise NotImplementedError("This method is not yet available for '{}'".format(self.__ENDPOINT_NAME__))
Kits = Handle
