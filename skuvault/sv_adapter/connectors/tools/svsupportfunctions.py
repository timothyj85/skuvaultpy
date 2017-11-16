from datetime import datetime, timedelta
import logging


def query_range_generator(ds, de, max_query_interval=7):
	"""Generates date range intervals less than or equal to the max_days parameter."""
	if ds > de:
		ds, de = de, ds
	total_days = timedelta(de - ds).days
	if not total_days > max_query_interval:
		yield ds, de
	else:
		list_of_days = [(ds + timedelta(i)) for i in range(0, total_days + 1)]
		while len(list_of_days) > 0:
			start_date, end_date = None, None
			start_date = list_of_days.pop(0)
			while len(list_of_days) > 0:
				end_date = list_of_days.pop(0)
				if (end_date - start_date).days == max_query_interval:
					break
			if end_date is None:
				end_date = start_date
			yield start_date, datetime(year=end_date.year, month=end_date.month, day=end_date.day, hour=23, minute=59, second=59)
