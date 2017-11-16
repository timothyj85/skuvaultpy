"""These models are used for posting data to SkUVault for create/updates. To update a model, just replace the json for 
that item type with the newer model."""
from enum import Enum
__PROPERTY_FORMATTER__ = '\t\tself.{0} = kwargs.get("{0}", None)'


class EndpointMetadata(Enum):
	syncOnlineSales = {"OrderTotal": 0, "SaleState": "String", "CheckoutStatus": "String", "OrderId": "String", "MarketplaceId": "String", "ShippingInfo": {"Country": "String", "Line2": "String", "ShippingClass": "String", "ShippingCarrier": "String", "PhoneNumber": "String", "CompanyName": "String", "Email": "String", "Region": "String", "ShippingStatus": "String", "Postal": "String", "LastName": "String", "City": "String", "FirstName": "String", "Line1": "String"}, "OrderDateUtc": "0001-01-01T00:00:00.0000000Z", "ItemSkus": [{"UnitPrice": 0, "Quantity": 1, "Sku": "String"}], "FulfilledItems": [{"UnitPrice": 0, "Quantity": 1, "Sku": "String"}], "Notes": "String", "PaymentStatus": "String"}
	setItemQuantities = {"LocationCode": "String", "Quantity": 0, "WarehouseId": 0, "Sku": "String"}
	createProducts = {"ShortDescription": "String", "AllowCreateAp": False, "Classification": "String", "LongDescription": "String", "SupplierInfo": [{"SupplierName": "Unknown", "LeadTime": 5, "Cost": 0.0, "SupplierPartNumber": "String", "isActive": False, "isPrimary": False}], "Attributes": {"AttributeName": "AttributeValue"}, "ReorderPoint": 0, "Statuses": ["String"], "WeightUnit": "String", "Pictures": ["http://www.example.com/image.jpg"], "Brand": "String", "Weight": 0, "RetailPrice": 0.0, "Note": "String", "SalePrice": 0.0, "Cost": 0.0, "VariationParentSku": "String", "MinimumOrderQuantity": 0, "MinimumOrderQuantityInfo": "String", "PartNumber": "String", "Sku": "String", "Description": "String", "Code": "String"}
	updateProducts = {"SalePrice": 0.0, "ShortDescription": "String", "Weight": 0.0, "Description": "String", "WeightUnit": "String", "Code": "String", "Brand": "String", "Sku": "String", "Classification": "String", "MinimumOrderQuantityInfo": "String", "Cost": 0.0, "RetailPrice": 0.0, "Pictures": ["http://www.example.com/image.jpg"], "PartNumber": "String", "Note": "String", "Statuses": ["String"], "LongDescription": "String", "ReorderPoint": 0, "Attributes": {"AttributeName": "AttributeValue"}, "MinimumOrderQuantity": 0, "SupplierInfo": [{"isActive": True, "SupplierPartNumber": "String", "Cost": 0.0, "isPrimary": True, "SupplierName": "String", "LeadTime": 0}], "VariationParentSku": "String"}
	createBrands = {"Name": "String"}
	createPO = {"LineItems": [{"QuantityTo3PL": 0, "SKU": "String", "PublicNotes": "String", "Variant": "String", "Cost": 0, "Identifier": "String", "PrivateNotes": "String", "Quantity": 1}], "Payments": [{"PaymentName": "String", "Amount": 0, "Note": "String"}], "TrackingInfo": "String", "ArrivalDueDate": "0001-01-01T00:00:00.0000000Z", "ShipToAddress": "String", "OrderCancelDate": "0001-01-01T00:00:00.0000000Z", "PaymentStatus": "String", "OrderDate": "0001-01-01T00:00:00.0000000Z", "SupplierName": "String", "ShipToWarehouse": "String", "PoNumber": "String", "UserToken": "String", "RequestedShipDate": "0001-01-01T00:00:00.0000000Z", "SentStatus": "String", "TenantToken": "String", "TermsName": "String", "ShippingCarrierClass": {"ClassName": "String", "CarrierName": "String"}, "PrivateNotes": "String", "PublicNotes": "String"}
	createSuppliers = {"EmailTemplateMessage": "String", "Name": "String", "EmailTemplateSubject": "String", "Emails": ["String"]}
	syncShippedSaleAndRemoveItems = {"FulfilledItems": [{"Quantity": 1, "Sku": "String", "UnitPrice": 0} ], "ItemSkus": [ { "Quantity": 1, "Sku": "String", "UnitPrice": 0 } ], "Notes": "String", "OrderDateUtc": "0001-01-01T00:00:00.0000000Z", "OrderId": "String", "OrderTotal": 0, "ShippingInfo": { "City": "String", "CompanyName": "String", "Country": "String", "Email": "String", "FirstName": "String", "LastName": "String", "Line1": "String", "Line2": "String", "PhoneNumber": "String", "Postal": "String", "Region": "String", "ShippingCarrier": "String", "ShippingClass": "String" }, "TenantToken": "String", "UserToken": "String", "WarehouseId": 0}
	updateExternalWarehouseQuantities = {"Quantities": [{"InStockQuantity": 0, "InboundQuantity": 0, "ReserveQuantity": 0, "Sku": "String", "TotalQuantity": 0, "TransferQuantity": 0}], "TenantToken": "String", "UserToken": "String", "WarehouseId": "String"}
	addItemBulk = {"Code": "String", "LocationCode": "String", "Quantity": 0, "Reason": "String", "Sku": "String", "WarehouseId": 0}


def get_item_class_def(model):
	"""Not using this but kept it because it's rather cool!"""
	_model_def = [
		"class Item(JsonSerializable):",
		"\tdef __init__(self, **kwargs):",
	]
	_model_def.extend([__PROPERTY_FORMATTER__.format(k) for k in model])
	_model_def.extend([
		"\t\tfor k, v in kwargs.items():",
		"\t\t\tsetattr(self, k, v)",
	])
	return "\n".join(_model_def)


def get_item_class_keys(endpoint):
	return getattr(EndpointMetadata, endpoint).value


if __name__ == "__main__":
	all_model_definitions = dict()
	for m in EndpointMetadata:
		all_model_definitions[m.name] = get_item_class_def(m.value)
	for name, model in all_model_definitions.items():
		one_class = exec(model)
		print(one_class)
