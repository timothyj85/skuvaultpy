from ._base_endpoint import EndpointWrapper
from datetime import timedelta
import logging
import time


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "products"

	def __init__(self):
		super().__init__()
		# ENDPOINTS
		self.createProducts = self.__SV_WRITE__.createProducts
		self.updateProducts = self.__SV_WRITE__.updateProducts

	# DQL METHODS
	def _get(self, **kwargs):
		return self.__SV_READ__.getProducts.paged(**kwargs)

	# DML METHODS
	def _send(self, product_list, create_products, update_products):
		"""Usage: Pass in a list of models ready to send to SkuVault and they will be sent appropriately."""
		logger = logging.getLogger(__name__)
		classified_products = self.__UTILITIES__.classify_products(pl=product_list, ex_pl=self.get_now())

		if create_products:
			logger.info("Sending '{}' new products to SkuVault.".format(len(classified_products["new"])))
			for p_ in classified_products["new"]:
				new_p_ = self.createProducts.new()
				new_p_.update(**p_)
			if len(classified_products["new"]) > 0:
				logger.info("Waiting 30 seconds to allow new Products to be created.")
				time.sleep(30)
			self.createProducts.send_all_skuvault()

		if update_products:
			logger.info("Sending '{}' product updates to SkuVault.".format(len(classified_products["exists"])))
			for p_ in classified_products["exists"]:
				ex_p = self.updateProducts.new()
				ex_p.update(**p_)
			self.updateProducts.send_all_skuvault()

	def syncProducts(self, product_list, create_brands, create_suppliers, create_products, update_products):
		"""Helper method to send products... Creates Suppliers; Creates Brands; Creates / Updates Products."""
		logger = logging.getLogger(__name__)
		logger.info("Syncing '{}' products to SkuVault.".format(len(product_list)))

		# replace invalid classifications with General since classes can't be created yet
		valid_classifications = [c_["Name"].upper() for c_ in self.SkuVault.classifications.get_now().values()]
		for p in product_list:
			if p["Classification"].upper() not in valid_classifications:
				p["Classification"] = "General"

		valid_products = self.__UTILITIES__.get_valid_products_for_sync_and_verbose_log_(product_list)

		if create_brands:
			self.SkuVault.brands.send(product_list=valid_products)

		if create_suppliers:
			self.SkuVault.suppliers.send(product_list=valid_products)

		self.send(
			product_list=valid_products,
			create_products=create_products,
			update_products=update_products,
		)
Products = Handle
