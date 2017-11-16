class MissingToolConfigurationException(Exception):
	"""Toolconfig not found for this tool / instance.
		EXIT CODE: FUTURE
	"""
	pass


class MissingSkuVaultCredentialsException(Exception):
	"""SkuVault credentials not found for this tool / instance.
		EXIT CODE: FUTURE
	"""
	pass


class BadSvApiCredentialsException(Exception):
	"""SkuVault credentials have been found, but seem to be rejected by SkuVault API.
		EXIT CODE: FUTURE
	"""
	pass


class CorruptedInstallation(Exception):
	"""Missing registry keys or other details that should be available to a valid installation.
	The installer should be re-ran, followed by rebooting the machine.
		EXIT CODE: FUTURE
	"""
	pass
