from ._base_endpoint import EndpointWrapper
from datetime import timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "available"

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	# DQL METHODS
	def _get(self, **kwargs):
		"""No filtering implemented yet."""
		return self.__SV_READ__.getAvailableQuantities.paged(ModifiedAfterDateTimeUtc=self.last_refresh_datetime.strftime("%Y-%m-%dT%H:%M:%S.0000000Z"))

	# DML METHODS
	def _send(self, **kwargs):
		raise NotImplementedError("This method is not yet available for '{}'".format(self.__ENDPOINT_NAME__))
AvailableQuantity = Handle
