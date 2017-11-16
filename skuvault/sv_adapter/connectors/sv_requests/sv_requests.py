"""
REF: https://blogs.technet.microsoft.com/nettracer/2010/06/03/things-that-you-may-want-to-know-about-tcp-keepalives
This custom session was created because SkuVault requires tcp keep-alive tokens to be sent at least 1 time
every 2 minutes. Trying to monkey-patch requests did not work out, so the solution that finally worked was to use
the default http.client module.
"""
from .sv_requests_low_level import SessionManager, FleshWound


def post(url, json=None, timeout=None, headers=None):
	"""Stand-in replacement for Requests that implements http.client to use custom sockets. Only does the main things 
	I want from requests, not a true 1:1 replacement."""
	_NUM_RETRIES = 3

	for retry in range(1, _NUM_RETRIES + 1):
		# FleshWound = Try Again, FatalException = Exit program, otherwise log and continue.
		try:
			return SessionManager.post(url=url, json=json, timeout=timeout, headers=headers)
		except FleshWound:
			print("it's just a flesh wound...")
			continue
	raise Exception("Unhandled exception encountered after {} retries to SV API!".format(_NUM_RETRIES))
