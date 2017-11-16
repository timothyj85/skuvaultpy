from ...data_types.utils._item_model_gen import get_item_class_keys
from ...connectors.sv_requests import sv_requests as requests
from skuvault import svexceptions, utils
from copy import deepcopy
import logging


# region: abstract base for sv api endpoints
class BaseForAllRequests:
	"""Inherited by DML & DQL request types"""
	__SV_BASE_URL__ = "https://app.skuvault.com/api"
	__TENANT_TOKEN__ = None
	__USER_TOKEN__ = None
	__DOMAIN__ = ""
	__OBJECT_LIST_KEY__ = None
	__LIMIT_PER_CALL__ = 1
	__MAX_GETS__ = 2147483648
	__MAX_POSTS__ = 2147483648
	__TIMEOUT__ = None
	SkuVault = None  # Reference added during init

	def __init__(self):
		self.__ENDPOINT__ = self.__class__.__name__[1:]  # remove leading underscore

	@property
	def url(self):
		return "{}/{}/{}".format(self.__SV_BASE_URL__, self.__DOMAIN__, self.__ENDPOINT__)

	@property
	def headers(self):
		"""Standard headers are set inside of sv_requests. Override thsi method with custom headers if needed and they 
		will be combined with the standard headers."""
		return None

	@property
	def auth_url(self):
		return "{}/{}".format(self.__SV_BASE_URL__, "getTokens")

	@property
	def base_payload(self):
		"""Override if needed."""
		return dict()

	def sv_login(self, username, password):
		data = {
			"Email": username,
			"Password": password,
		}
		response = requests.post(url=self.auth_url, json=data)
		if response.status_code == 200:
			json_response = response.json
			if json_response["TenantToken"]:
				BaseForAllRequests.__TENANT_TOKEN__ = json_response["TenantToken"]
				BaseForAllRequests.__USER_TOKEN__ = json_response["UserToken"]
				return json_response
			else:
				raise utils.slow_close_console(msg="Bad SV credentials!!", exit_code=1)

	def _sv_post(self, **payload):
		if not BaseForAllRequests.__USER_TOKEN__ or not BaseForAllRequests.__TENANT_TOKEN__:
			raise PermissionError("Must log in before making requests!")

		_payload = self.base_payload
		_payload.update(payload)
		_payload.update({
			"UserToken": self.__USER_TOKEN__,
			"TenantToken": self.__TENANT_TOKEN__,
		})
		_payload = {k: v for k, v in _payload.items() if v is not None}  # remove null values
		return requests.post(url=self.url, json=_payload, timeout=self.__TIMEOUT__, headers=self.headers)
# endregion


# region: getting data from skuvault
class DqlRequest(BaseForAllRequests):
	"""Getting data from SkuVault API. 
	NOTE: If you set __OBJECT_LIST_KEY__ the method will dig down into that object to find 
	the object list result."""
	__PAGE_NUM_KEY__ = "PageNumber"
	__PAGE_SIZE_KEY__ = "PageSize"

	def __init__(self):
		super().__init__()

	def paged(self, **post_body_params):
		result = list()
		for page_num in range(0, self.__MAX_GETS__):
			post_body_params.update({
				self.__PAGE_SIZE_KEY__: self.__LIMIT_PER_CALL__,
				self.__PAGE_NUM_KEY__: page_num,
			})
			response_list = self.single_get(**post_body_params) or list()
			if isinstance(response_list, list):
				result += response_list
			elif isinstance(response_list, dict):
				result += list(response_list.items())
			if len(response_list) < self.__LIMIT_PER_CALL__:
				break
		return result

	def single_get(self, **post_body_params):
		raw_response = self._sv_post(**post_body_params)
		response_obj = raw_response.json
		if isinstance(response_obj, dict) and self.__OBJECT_LIST_KEY__ is not None:
			response_obj = response_obj.get(self.__OBJECT_LIST_KEY__)
		return response_obj
# endregion


# region: creating / updating data in skuvault
class OneItem:
	"""Represents a single object in the payload... 
	ie: If the payload contains a list then this is one item in that list."""
	def __init__(self, **kwargs):
		for k, v in kwargs.items():
			setattr(self, k, None)

	def update(self, **kwargs):
		for k, v in kwargs.items():
			setattr(self, k, v)

	@property
	def serializable(self):
		"""Return dictionary of non-null values."""
		my_attributes = {i: self.__getattribute__(i) for i in self.__dict__.keys() if i[:1] != '_' and self.__getattribute__(i) is not None}
		return deepcopy(my_attributes)


class DmlRequest(BaseForAllRequests):
	__PENDING_REQUESTS__ = list()  # class-level tracking of what needs to be sent to SV.

	"""Updating or creating data with SkuVault API."""
	def __init__(self, **kwargs):
		super().__init__()
		self._data = list()
		_payload_keys = get_item_class_keys(self.__ENDPOINT__)
		self.__ITEM_CLASS__ = lambda: OneItem(**_payload_keys)

	def new(self):
		"""Returns one empty model"""
		_new_item = self.__ITEM_CLASS__()
		self._data.append(_new_item)
		if self not in DmlRequest.__PENDING_REQUESTS__:
			DmlRequest.__PENDING_REQUESTS__.append(self)
		return _new_item

	@property
	def items(self):
		for item in self._data:
			yield item

	@items.setter
	def items(self, items_list):
		self._data = items_list

	@property
	def count(self):
		return len(self._data)

	def add_item(self, item):
		self._data.append(item)

	def deserialize_msg_and_add_item(self, item_dict):
		"""Helps queue save time parsing write messages."""
		_item_proper = self.new()
		_item_proper.update(**item_dict)

	def filter_one_item(self, obj_list, one_item):
		"""If you need to pre-filter items add this method to your class."""
		obj_list.append(one_item.serializable)

	def items_payload_generator(self, limit=None):
		"""Items are only be iterated over one time; that's why they're popped rather than plain iteration."""
		logger = logging.getLogger(__name__)
		if limit is None:
			limit = self.__LIMIT_PER_CALL__
		sent = 0
		_one_payload = list()
		while len(self._data) > 0:
			if sent >= self.__MAX_POSTS__:
				logger.debug("Maximum posts for '{}' reached: {}".format(self.__ENDPOINT__, self.__MAX_POSTS__))
				return
			_one_item = self._data.pop(0)
			self.filter_one_item(_one_payload, _one_item)
			if len(_one_payload) == limit:
				yield _one_payload
				sent += 1
				_one_payload = list()

		if len(_one_payload) > 0:
			yield _one_payload
			sent += 1

	def send_all_skuvault(self, **kwargs):
		"""Iterates over items and sends to SkuVault."""
		logger = logging.getLogger(__name__)
		logger.info("Found '{}' items pending for this endpoint '{}'.".format(len(self._data), self.__ENDPOINT__))
		if len(self._data) == 0:
			return
		results = list()
		for _obj_list in self.items_payload_generator(**kwargs):
			if self.__OBJECT_LIST_KEY__ is not None:
				post_body = {self.__OBJECT_LIST_KEY__: _obj_list}
			# FIXME: Ugly code alert:
			elif self.__OBJECT_LIST_KEY__ is None and self.__LIMIT_PER_CALL__ == 1 and len(_obj_list) == 1:
				post_body = _obj_list[0]
			else:
				raise NotImplementedError("Payload definition is not handled by existing method!\nObj:{}\nKey:{}\nLimit: {}\nItems: {}".format(
					_obj_list, self.__OBJECT_LIST_KEY__, self.__LIMIT_PER_CALL__, len(_obj_list)
				))
			result = self._sv_post(**post_body)
			results.append(result)
		return len(results)  # return count of successful payloads sent
# endregion
