from ._base_endpoint import EndpointWrapper
from datetime import timedelta
import logging
import time


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "brands"

	def __init__(self):
		super().__init__()
		# ENDPOINTS
		self.createBrands = self.__SV_WRITE__.createBrands

	# DQL METHODS
	def _get(self, **kwargs):
		return self.__SV_READ__.getBrands.paged()

	# DML METHODS
	def _send(self, product_list):
		"""Extracts brands from a product list and creates new ones."""
		logger = logging.getLogger(__name__)
		existing_sv_brands_ = set([b["Name"].upper() for b in self.get_now().values()])
		# tgj 10/24/2017: Unknown is not returned in getBrands api call
		brands_in_payload = set([p_["Brand"].upper() for p_ in product_list if p_["Brand"].upper() != "UNKNOWN"])
		brands_to_send = [b_ for b_ in brands_in_payload if b_ not in existing_sv_brands_]

		for b_ in brands_to_send:
			new_brand_ = self.createBrands.new()
			new_brand_.update(Name=b_)
		self.createBrands.send_all_skuvault()
		if len(brands_to_send) > 0:
			self.reset_refresh_datetime()
			logger.info("Waiting 30 seconds to allow new Brands to be created.")
			time.sleep(30)
Brands = Handle
