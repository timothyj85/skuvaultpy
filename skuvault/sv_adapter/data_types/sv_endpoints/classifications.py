from ._base_endpoint import EndpointWrapper
from datetime import timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "classifications"

	def __init__(self):
		super().__init__()

	# DQL METHODS
	def _get(self, **kwargs):
		"""No filtering implemented yet."""
		return self.__SV_READ__.getClassifications.paged()

	# DML METHODS
	def _send(self, **kwargs):
		raise NotImplementedError("SkuVault API does not allow creation of Classifications yet!")
Classifications = Handle
