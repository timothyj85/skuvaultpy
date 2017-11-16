"""This class is used by Simple Tools that only need access to one instance of SkuVault.
It will automatically log in when the module is imported."""
from .connectors.tools.sv_endpoint_models import BaseForAllRequests, DmlRequest
from .data_types.sv_endpoints import _base_endpoint
from skuvault import svexceptions, utils
from .connectors.sv_read import login
import logging
import os


from .data_types.sv_endpoints.available import AvailableQuantity
from .data_types.sv_endpoints.brands import Brands
from .data_types.sv_endpoints.classifications import Classifications
from .data_types.sv_endpoints.kits import Kits
from .data_types.sv_endpoints.on_hand import OnHand
from .data_types.sv_endpoints.products import Products
from .data_types.sv_endpoints.purchase_orders import PurchaseOrders
from .data_types.sv_endpoints.sales import Sales
from .data_types.sv_endpoints.suppliers import Suppliers
from .data_types.sv_endpoints.external_warehouses import ExternalWarehouses


def _load_credentials(endpoint, username, password):
	if endpoint.lower() not in ["app", "qa", "staging"]:
		endpoint = "app"
	BaseForAllRequests.__SV_BASE_URL__ = "https://{}.skuvault.com/api".format(e).lower().strip()

	creds = login(username, password)
	tt, ut = (creds["TenantToken"], creds["UserToken"])


class _SvConnector:
	def __init__(self, username, password, endpoint="app"):
		# INIT ABSTRACT CLASSES
		_load_credentials(endpoint, username, password)
		BaseForAllRequests.SkuVault = self
		_base_endpoint.EndpointWrapper.SkuVault = self
		
		# DOMAINS
		self.available = AvailableQuantity()
		self.kits = Kits()
		self.on_hand = OnHand()
		self.products = Products()
		self.suppliers = Suppliers()
		self.classifications = Classifications()
		self.brands = Brands()
		self.sales = Sales()
		self.purchase_orders = PurchaseOrders()
		self.external_warehouses = ExternalWarehouses()

	def send_all_pending(self):
		"""Flushes create/updates to SkuVault for any pending data types."""
		logger = logging.getLogger(__name__)
		logger.info("Found '{}' total pending endpoints to send to SkuVault.".format(
			len(DmlRequest.__PENDING_REQUESTS__)
		))
		while len(DmlRequest.__PENDING_REQUESTS__) > 0:
			endpoint = DmlRequest.__PENDING_REQUESTS__.pop(0)
			logger.info("Sending pending requests for '{}'. '{}' more pending.".format(
				endpoint.__class__.__name__, len(DmlRequest.__PENDING_REQUESTS__)
			))
			endpoint.send_all_skuvault()
	