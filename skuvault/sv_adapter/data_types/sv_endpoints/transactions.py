from ._base_endpoint import EndpointWrapper
from datetime import timedelta


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "transactions"

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	# DQL METHODS
	def _get(self, **kwargs):
		return self.__SV_READ__.get_transactions_for_date_range(**kwargs)

	# DML METHODS
	def _send(self, **kwargs):
		raise NotImplementedError("This method is not yet available for '{}'".format(self.__ENDPOINT_NAME__))
Transactions = Handle


# TODO: Untested
