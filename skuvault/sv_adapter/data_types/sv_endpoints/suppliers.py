from ._base_endpoint import EndpointWrapper
from datetime import timedelta
import logging
import time


class Handle(EndpointWrapper):
	__ENDPOINT_NAME__ = "suppliers"

	def __init__(self):
		super().__init__()
		# ENDPOINTS
		self.createSuppliers = self.__SV_WRITE__.createSuppliers

	# DQL METHODS
	def _get(self, **kwargs):
		return self.__SV_READ__.getSuppliers.paged(**kwargs)

	# DML METHODS
	def _send(self, product_list):
		"""Extracts suppliers from a product list and creates new ones."""
		logger = logging.getLogger(__name__)
		existing_sv_suppliers_ = set([s["Name"].upper() for s in self.get_now().values()])
		# Extract all SupplierName's from the list of products
		all_suppliers_in_product_list_ = list()
		for one_product_ in product_list:
			for one_supplier_ in one_product_["SupplierInfo"]:
				all_suppliers_in_product_list_.append(one_supplier_["SupplierName"].upper())
		all_suppliers_in_product_list_ = set(all_suppliers_in_product_list_)
		# Determine which SupplierName's in the list do not exist inside SkuVault.
		suppliers_to_send = [s_ for s_ in all_suppliers_in_product_list_ if s_ not in existing_sv_suppliers_]

		# Send missing Suppliers to SkuVault.
		for s_ in suppliers_to_send:
			new_s_ = self.createSuppliers.new()
			new_s_.update(**{
				"EmailTemplateMessage": "",
				"EmailTemplateSubject": "",
				"Emails": [],
				"Name": s_
			})
		self.createSuppliers.send_all_skuvault()
		if len(suppliers_to_send) > 0:
			logger.info("Waiting 30 seconds to allow new Suppliers to be created.")
			time.sleep(30)
Suppliers = Handle
