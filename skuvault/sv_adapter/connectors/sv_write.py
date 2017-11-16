from .tools.sv_endpoint_models import DmlRequest


class _createProducts(DmlRequest):
	__LIMIT_PER_CALL__ = 100
	__TIMEOUT__ = None
	__DOMAIN__ = "products"
	__OBJECT_LIST_KEY__ = "Items"

	def __init__(self):
		super().__init__()
createProducts = _createProducts()


class _updateProducts(DmlRequest):
	__LIMIT_PER_CALL__ = 100
	__TIMEOUT__ = None
	__DOMAIN__ = "products"
	__OBJECT_LIST_KEY__ = "Items"
	__ALL_SKUS__ = list()

	def filter_one_item(self, obj_list, one_item):
		if len(self.__ALL_SKUS__) == 0:
			# GET A LIST OF ALL SKUS
			for obj_id, obj in self.SkuVault.products.get_now().items():
				self.__ALL_SKUS__.append(obj["Sku"])
		# ONLY SEND AN UPDATE IF THE SKU EXISTS IN SKU VAULT!
		if one_item.Sku in self.__ALL_SKUS__:
			obj_list.append(one_item.serializable)

	def __init__(self):
		super().__init__()
updateProducts = _updateProducts()


class _createSuppliers(DmlRequest):
	__LIMIT_PER_CALL__ = 100
	__TIMEOUT__ = None
	__DOMAIN__ = "products"
	__OBJECT_LIST_KEY__ = "Suppliers"

	def __init__(self):
		super().__init__()
createSuppliers = _createSuppliers()


class _syncOnlineSales(DmlRequest):
	__LIMIT_PER_CALL__ = 25
	__TIMEOUT__ = None
	__DOMAIN__ = "sales"
	__OBJECT_LIST_KEY__ = "Sales"

	def __init__(self):
		super().__init__()
syncOnlineSales = _syncOnlineSales()


class _createBrands(DmlRequest):
	__LIMIT_PER_CALL__ = 100
	__TIMEOUT__ = None
	__DOMAIN__ = "products"
	__OBJECT_LIST_KEY__ = "Brands"

	def __init__(self):
		super().__init__()
createBrands = _createBrands()


class _addItemBulk(DmlRequest):
	__LIMIT_PER_CALL__ = 100
	__TIMEOUT__ = None
	__DOMAIN__ = "inventory"
	__OBJECT_LIST_KEY__ = "Items"

	def __init__(self):
		super().__init__()
addItemBulk = _addItemBulk()


class _setItemQuantities(DmlRequest):
	__LIMIT_PER_CALL__ = 100
	__TIMEOUT__ = None
	__DOMAIN__ = "inventory"
	__OBJECT_LIST_KEY__ = "Items"

	def __init__(self):
		super().__init__()
setItemQuantities = _setItemQuantities()


class _createPO(DmlRequest):
	__LIMIT_PER_CALL__ = 1
	__TIMEOUT__ = None
	__DOMAIN__ = "purchaseorders"
	__OBJECT_LIST_KEY__ = None

	def __init__(self):
		super().__init__()
createPO = _createPO()


class _syncShippedSaleAndRemoveItems(DmlRequest):
	__LIMIT_PER_CALL__ = 1
	__TIMEOUT__ = None
	__DOMAIN__ = "sales"
	__OBJECT_LIST_KEY__ = None

	def __init__(self):
		super().__init__()
syncShippedSaleAndRemoveItems = _syncShippedSaleAndRemoveItems()


class _updateExternalWarehouseQuantities(DmlRequest):
	__LIMIT_PER_CALL__ = 100000
	__TIMEOUT__ = None
	__DOMAIN__ = "inventory"
	__OBJECT_LIST_KEY__ = "Quantities"

	@property
	def base_payload(self):
		return {
			"WarehouseId": self.warehouse_id
		}

	def __init__(self, warehouse_id):
		self.warehouse_id = warehouse_id
		super().__init__()
updateExternalWarehouseQuantities = _updateExternalWarehouseQuantities  # READ: THIS IS NOT AUTO-INITIALIZED
