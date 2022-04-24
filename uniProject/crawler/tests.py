from django.test import TestCase
from . import myCrawler


class testCrawler(TestCase):
	def test_search_string_is_not_empty(self):
		test = myCrawler.parseSearchString("")

		self.assertIsNot(test, "")

	def test_search_is_string(self):
		test = myCrawler.parseSearchString(1)

		self.assertIsInstance(test, str)

	def test_search_is_not_none(self):
		test = myCrawler.parseSearchString(None)

		self.assertIsNot(test, None)


	def test_search_special_chars(self):
		test = myCrawler.parseSearchString("\"test")
		self.assertIsNot(test, "\"test")

		test = myCrawler.parseSearchString("% or test")
		self.assertIsNot(test, "% or test")

	def test_new_page_is_bool(self):
		test = myCrawler.isBool("True")

		self.assertIsInstance(test, type(True))

	def test_volume_is_boo(self)
		test = myCrawler.isBool("False")

		self.assertIsInstance(test, type(True))

