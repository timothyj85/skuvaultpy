from .tools.sv_endpoint_models import BaseForAllRequests, DqlRequest
from .tools import svsupportfunctions as svs
import logging


class __login(BaseForAllRequests):
	"""sv_auth.sv_login(username, password before making any other requests!"""
	def __init__(self):
		super().__init__()
_login = __login()
login = _login.sv_login


class _getProducts(DqlRequest):
	__DOMAIN__ = "products"
	__LIMIT_PER_CALL__ = 10000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Products"

	def __init__(self):
		super().__init__()
getProducts = _getProducts()


class _getAvailableQuantities(DqlRequest):
	__DOMAIN__ = "inventory"
	__LIMIT_PER_CALL__ = 5000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Items"

	def __init__(self):
		super().__init__()
getAvailableQuantities = _getAvailableQuantities()


class _getInventoryByLocation(DqlRequest):
	__DOMAIN__ = "inventory"
	__LIMIT_PER_CALL__ = 1000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Items"

	def __init__(self):
		super().__init__()
getInventoryByLocation = _getInventoryByLocation()


class _getExternalWarehouses(DqlRequest):
	__DOMAIN__ = "inventory"
	__LIMIT_PER_CALL__ = 1000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Warehouses"
	__MAX_GETS__ = 1

	def __init__(self):
		super().__init__()
getExternalWarehouses = _getExternalWarehouses()


class _getExternalWarehouseQuantities(DqlRequest):
	__DOMAIN__ = "inventory"
	__LIMIT_PER_CALL__ = 100000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Quantities"
	__MAX_POSTS__ = 1  # Only 1 POST!
	__MAX_GETS__ = 1  # Only 1 GET also!

	@property
	def base_payload(self):
		return {
			"PageSize": 100000
		}

	def __init__(self):
		super().__init__()
getExternalWarehouseQuantities = _getExternalWarehouseQuantities()


class _getItemQuantities(DqlRequest):
	__DOMAIN__ = "inventory"
	__LIMIT_PER_CALL__ = 10000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Brands"

	def __init__(self):
		super().__init__()
getItemQuantities = _getItemQuantities()


class _getBrands(DqlRequest):
	__DOMAIN__ = "products"
	__LIMIT_PER_CALL__ = 1000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Brands"

	def __init__(self):
		super().__init__()
getBrands = _getBrands()


class _getSuppliers(DqlRequest):
	__DOMAIN__ = "products"
	__LIMIT_PER_CALL__ = 1000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Suppliers"

	def __init__(self):
		super().__init__()
getSuppliers = _getSuppliers()


class _getClassifications(DqlRequest):
	__DOMAIN__ = "products"
	__LIMIT_PER_CALL__ = 1000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Classifications"

	def __init__(self):
		super().__init__()
getClassifications = _getClassifications()


class _getKits(DqlRequest):
	__DOMAIN__ = "products"
	__LIMIT_PER_CALL__ = 10000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Kits"

	def __init__(self):
		super().__init__()
getKits = _getKits()


class _getTransactions(DqlRequest):
	__DOMAIN__ = "inventory"
	__LIMIT_PER_CALL__ = 10000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Transactions"

	def __init__(self):
		super().__init__()
getTransactions = _getTransactions()


class _getSales(DqlRequest):
	__DOMAIN__ = "sales"
	__LIMIT_PER_CALL__ = 10000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Sales"

	def __init__(self):
		super().__init__()
getSales = _getSales()


class _getSalesByDate(DqlRequest):
	"""Only accepts a range of 7 days at a time! Use the helper method below!"""
	__DOMAIN__ = "sales"
	__LIMIT_PER_CALL__ = 10000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "Sales"

	def __init__(self):
		super().__init__()
getSalesByDate = _getSalesByDate()


class _getPOs(DqlRequest):
	"""Will not return Completed purchase orders unless you pass Status=Completed then it will only return them."""
	__DOMAIN__ = "purchaseorders"
	__LIMIT_PER_CALL__ = 10000
	__TIMEOUT__ = None
	__OBJECT_LIST_KEY__ = "PurchaseOrders"

	def __init__(self):
		super().__init__()
getPOs = _getPOs()


def get_sales_for_date_range(date_range_start_datetime, date_range_end_datetime):
	"""Can only request 1 week at a time so must do some magic to get sales for a date range."""
	logger = logging.getLogger(__name__)
	logger.debug("Getting sales data for date range {} - {}.".format(date_range_start_datetime, date_range_end_datetime))

	sales_list = list()
	for s, e in svs.query_range_generator(date_range_start_datetime, date_range_end_datetime, max_query_interval=7):
		sales_list += getSalesByDate.paged(FromDate=s.strftime("%Y-%m-%dT%H:%M:%S.0000000Z"), ToDate=e.strftime("%Y-%m-%dT%H:%M:%S.0000000Z"))
	return sales_list


def get_transactions_for_date_range(date_range_start_datetime, date_range_end_datetime):
	"""Can only request 1 week at a time so must do some magic to get transactions for a date range."""
	logger = logging.getLogger(__name__)
	logger.debug("Getting transactions data for date range {} - {}.".format(date_range_start_datetime, date_range_end_datetime))

	transactions_list = list()
	for s, e in svs.query_range_generator(date_range_start_datetime, date_range_end_datetime, max_query_interval=7):
		transactions_list += getTransactions.paged(FromDate=s.strftime("%Y-%m-%dT%H:%M:%S.0000000Z"), ToDate=e.strftime("%Y-%m-%dT%H:%M:%S.0000000Z"))
	return transactions_list
