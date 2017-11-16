"""Use these when reading from SkuVault. They wrap local cache access with the SkuVault adapter."""
from enum import Enum

from .sv_endpoints import available, kits, on_hand, products, suppliers, classifications, brands, sales, purchase_orders


class SkuVaultDataTypeEnum(Enum):
	SALES = 1
	ON_HAND = 2
	AVAILABLE = 3
	PRODUCTS = 4
	CLASSIFICATIONS = 5
	BRANDS = 6
	KITS = 7
	SUPPLIERS = 8
	PURCHASE_ORDERS = 9


def get_safe_data_type_string(e):
	"""Tries to accept both string and enums"""
	types = [en.name.lower() for en in SkuVaultDataTypeEnum]
	if isinstance(e, Enum):
		e = e.name
	elif isinstance(e, str) and "." in e:
		e = ".".split(e)[1]
	e = str(e).lower()
	if e in types:
		return e
	raise Exception("Unknown data type requested: {}".format(e))


def get_endpoint(e):
	safe_e = get_safe_data_type_string(e)
	types = {
		"sales": sales.Handle,
		"on_hand": on_hand.Handle,
		"available": available.Handle,
		"products": products.Handle,
		"classifications": classifications.Handle,
		"brands": brands.Handle,
		"kits": kits.Handle,
		"suppliers": suppliers.Handle,
		"purchase_orders": purchase_orders.Handle,
	}
	endpoint = types[safe_e]
	return endpoint
