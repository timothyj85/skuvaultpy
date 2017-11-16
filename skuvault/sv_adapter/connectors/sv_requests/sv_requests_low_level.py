"""
	requests module has been switched out for a custom http adapter when connecting to the SkuVault API. The main issue 
	with the SkuVault API is in regards to the TCP timeouts of 1.5 minutes. At this time, requests does not have a 
	way to customize the socket for Windows machines. self.conn.sock.ioctl is Windows only way to customize the tcp 
	socket. For other operating systems a different method will need to be implemented.
"""
from urllib.parse import urlparse
from io import BytesIO
import http.client
import json as js
import traceback
import logging
import socket
import time
import gzip
import json
KEEP_ALIVE_INTERVAL_MS = 3000
KEEP_ALIVE_TIME = 45000
KEEP_ALIVE_ENABLE = 1
DEFAULT_TIMEOUT = 900
__LOGGER_NAME__ = "skuvault.sv_adapter.connectors.sv_requests.models"
logging.getLogger(__LOGGER_NAME__).setLevel(logging.INFO)


def singleton(cls):
	"""auto-init class"""
	return cls()


class Request:
	def __init__(self, conn):
		_response = conn.getresponse()
		self.info = _response.info()
		self.reason = _response.reason
		self.status_code = _response.status
		# self.raw_bytes = _response.readall()
		self.raw = _response.read()

	@property
	def text(self):
		if self.info.get('data-Encoding') == 'gzip':
			buf = BytesIO(self.raw)
			f = gzip.GzipFile(fileobj=buf)
			raw_bytes = f.read()
		else:
			raw_bytes = self.raw
		return raw_bytes.decode("UTF-8")

	@property
	def json(self):
		try:
			dict_data = js.loads(self.text)
			return dict_data
		except:
			raise Exception("Json decoding error with: {}\n\n{}".format(self.raw, traceback.format_exc()))


class CustomSession:
	"""Connects to SkuVault with custom socket... Allows for very long requests utilizing tcp keep-alive packets to 
	ensure SkuVault's IIS server doesn't close the connection."""
	def __init__(self, url, timeout=900):
		self.conn = None
		self.url = url
		self.timeout = timeout
		self.hostname = urlparse(url).hostname

	def connect(self):
		self.conn = http.client.HTTPSConnection(host=self.hostname, timeout=self.timeout or DEFAULT_TIMEOUT)
		self.conn.connect()
		self.conn.sock.ioctl(socket.SIO_KEEPALIVE_VALS, (KEEP_ALIVE_ENABLE, KEEP_ALIVE_TIME, KEEP_ALIVE_INTERVAL_MS))
		self.conn.sock.do_handshake()

	def send(self, payload, headers, method="POST"):
		"""Can use connection for multiple requests."""
		self.conn.request(method=method, url=self.url, body=payload, headers=headers)
		response = Request(conn=self.conn)
		return response

	def close(self):
		self.conn.close()


class _SessionManager:
	__HANDLES__ = dict()

	def post(self, url, json, timeout=None, headers=None):
		_payload = js.dumps(json).encode("utf-8")
		_base_headers = {
			"Content-Type": "application/json; charset=utf-8",
			"Accept": "application/json",
			"Connection": "keep-alive",
			"Accept-Encoding": "gzip",
			# "data-Length": str(len(_payload)),  # works, but unnecessary
		}
		_base_headers.update(headers or {})

		session = CustomSession(url)
		session.connect()
		response = session.send(payload=_payload, headers=_base_headers)
		response_status_handler(response=response, url=url, payload=json, headers=_base_headers)
		session.close()  # future: keep table of connections for re-use to avoid handshake.

		return response
SessionManager = _SessionManager()


class FleshWound(Exception):
	def __init__(self, message="It's just a flesh wound! We can recover from this.", **kwargs):
		super(Exception, self).__init__(message)
		self.log_messages = kwargs

	@property
	def text(self):
		return "\n".join(["{}: {}".format(k, v) for k, v in self.log_messages])


class FatalException(Exception):
	def __init__(self, message="Fatal response from SkuVault, requesting program shuts down.", **kwargs):
		super(Exception, self).__init__(message)
		self.log_messages = kwargs

	@property
	def text(self):
		return "\n".join(["{}: {}".format(k, v) for k, v in self.log_messages])


def response_status_handler(response, url, payload, headers):
	"""Provides generic logging method for SV API. Raises a 'flesh wound' if retry is possible, or fatal error if
	program should exit. payload will be logged at info level."""
	logger = logging.getLogger(__LOGGER_NAME__)
	_payload = dict()
	if isinstance(payload, dict):
		bad_keys = ["USERTOKEN", "TENANTTOKEN", "EMAIL", "PASSWORD"]
		_payload = {k: v for k, v in payload.items() if k.upper() not in bad_keys}
	payload_string = "; ".join(["{}: {}".format(k, v) for k, v in _payload.items()])
	logger.info("URL: {}; Status Code: {};".format(url, response.status_code))
	# ONLY OUTPUT UP TO 10k CHARACTERS OF PAYLOAD STRING.
	if len(payload_string) > 10000:
		payload_string = payload_string[0:9998] + "..."
	if "GETTOKENS" not in url.upper():
		logger.info("HTTP DATA SENT TO SKUVAULT:\n\t{}".format(payload_string))
		logger.info("RECEIVED A '{}' CHARACTER LENGTH RESPONSE FROM THE SKUVAULT API.".format(len(response.text)))
		if "Errors" in response.json and len(response.json["Errors"]) > 0:
			logger.warning("RECEIVED SOME ERRORS FROM SKUVAULT API:\n{}".format(response.json["Errors"]))
		logger.debug("FULL SKUVAULT RESPONSE:\n\t{}".format(response.text))
	if response.status_code in (200, 202, 409):
		pass  # 200: OK, 202: Accepted, 409: Conflict(not a big deal)
	elif response.status_code == 429:
		logger.info("Throttled by SkuVault API. Pausing for 60 seconds.")
		time.sleep(61)
		raise FleshWound("Throttled; ready for retry.")
	elif response.status_code in (401, 403, 404):
		logger.critical("Authentication error with SkuVault API!")
		raise FatalException(http_status_code=response.status_code)
	elif response.status_code == 400:
		logger.critical("Bad request!")
		raise FatalException(http_status_code=response.status_code)
	elif response.status_code == 500:
		logger.critical("Internal server error. Check request for errors!")
		raise FatalException(http_status_code=response.status_code)
	else:
		raise Exception("Encountered unknown error with api.")
