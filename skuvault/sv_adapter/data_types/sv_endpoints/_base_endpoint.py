from ....input_output.output._utils import convert
from ....input_output.output._utils import utils
from ...connectors import sv_read, sv_write
from datetime import datetime, timedelta
import os


class EndpointWrapper:
	"""Base class for data models."""
	__SV_READ__ = sv_read
	__SV_WRITE__ = sv_write
	__SV_IO__ = None  # shared reference to SvApi
	__CONVERSIONS__ = convert
	__UTILITIES__ = utils
	__API_TOKENS__ = dict()
	__ENDPOINT_NAME__ = None
	SkuVault = None  # Endpoints are initialized by the SkuVaultAdapter module

	def __init__(self, sv_base, api_tokens, **kwargs):
		EndpointWrapper.SkuVault = sv_base
		self.api_tokens = api_tokens
		self._data_type = e
		self._kwargs = kwargs
		EndpointWrapper.__SV_IO__ = _SvApiIO()
		self.synchronized_name = "{}_synced".format(self.__ENDPOINT_NAME__).lower()
		self.modified = False
		self._handle = EndpointWrapper.__SV_IO__.get_data_handle(
			e=self._data_type,
			name=self.__ENDPOINT_NAME__,
		)

	def get(self, **kwargs):
		"""Reserved for hooking into method; endpoints use _get()"""
		return self._get(**kwargs)

	def send(self, **kwargs):
		"""Reserved for hooking into method; endpoints use _send()"""
		self._send(**kwargs)

	def _get(self, **kwargs):
		raise NotImplementedError("Get not implemented for '{}'".format(self.__ENDPOINT_NAME__))
	
	def _send(self, **kwargs):
		raise NotImplementedError("Send is not yet available for '{}'".format(self.__ENDPOINT_NAME__))
