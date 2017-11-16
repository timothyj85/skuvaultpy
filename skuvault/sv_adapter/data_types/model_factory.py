"""Use these when writing to SkuVault."""
from enum import Enum

from ..connectors import sv_write


class SkuVaultDataTypeEnum(Enum):
	syncOnlineSales = 1
	setItemQuantities = 2
	createProducts = 3
	updateProducts = 4
	createBrands = 5
	createPO = 6
	createSuppliers = 7
	syncShippedSaleAndRemoveItems = 8


def get_safe_data_type_string(e):
	"""Tries to accept both string and enums"""
	types = [e.name.lower() for e in SkuVaultDataTypeEnum]
	if isinstance(e, Enum):
		e = e.name
	elif isinstance(e, str) and "." in e:
		e = ".".split(e)[1]
	e = str(e).lower()
	if e in types:
		return e
	raise Exception("Unknown data type requested: {}".format(e))


def get_model_factory(e):
	safe_e = get_safe_data_type_string(e)
	types = {
		"synconlinesales": sv_write.syncOnlineSales,
		"setitemquantities": sv_write.setItemQuantities,
		"createproducts": sv_write.createProducts,
		"updateproducts": sv_write.updateProducts,
		"createsuppliers": sv_write.createSuppliers,
		"createbrands": sv_write.createBrands,
		"createpo": sv_write.createPO,
		"syncshippedsaleandremoveitems": sv_write.syncShippedSaleAndRemoveItems,
	}
	return types[safe_e]
