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

	def test_volume_is_bool(self):
		test = myCrawler.isBool("False")

		self.assertIsInstance(test, type(True))


	def test_num_page_is_int(self):
		test = myCrawler.isInt("1")

		self.assertIsInstance(test, int)

		test = myCrawler.isInt("one")
		self.assertIsInstance(test, int)


	def test_calculater_volume_valid_int(self):
		test = myCrawler.calculate_volume("q")

		self.assertIsInstance(test, float)

	def test_calculate_volume(self):
		test_data = ["0", "1", "3", "4", "5"]
		test = myCrawler.calculate_volume(test_data)

		self.assertIsInstance(test, float)
		self.assertEqual(test, 0)


	def test_division_by_zero(self):
		test_data = [0, 0, 0]
		test = myCrawler.calculate_volume(test_data)

		self.assertEqual(test, 0)


	def test_convert_meters_to_mm(self):
		test_data = ["2.5m", "6.7M", "34MM"]

		test = myCrawler.convert_to_mm(test_data)

		self.assertEqual(test, [2500, 6700, 34])


	def test_convert_mm_has_valid_string(self):
		test_data = ["M", "Z", "34\""]

		test = myCrawler.convert_to_mm(test_data)

		self.assertEqual(test, [0, 0, 34])


	def test_strip_dimensions(self):
		test_data = ["(W)2400, (L)3400,, test (t)1000"]
		test = myCrawler.strip_dimensions(test_data)

		self.assertEqual(test, ["2400, 3400,, test 1000"])


	def test_get_dimensions(self):
		test_data = "this test (W)2400, some random noise (L)3400,, test (t)1000"

		test = myCrawler.get_dimensions(test_data)

		# we always return in the order of L W T
		self.assertEqual(test, [3400.0, 2400.0, 1000.0])


	def test_get_pack_size_lowercase(self):
		test_data = "Contains a pack of 4"

		test = myCrawler.extract_pack_size(test_data)

		self.assertEqual(test, 4)

	def test_get_pack_size_uppercase(self):
		test_data = "CONTAINS A PACK OF 5 PEICES OF WOOD"
		test = myCrawler.extract_pack_size(test_data)

		self.assertEqual(test, 5)


	def test_no_pack_size(self):
		test_data = "this produce has no pack size"
		test = myCrawler.extract_pack_size(test_data)

		self.assertEqual(test, False)


	def test_missing_json_file(self):
		test = myCrawler.extract_details("path/does/not/exist", True)

		self.assertEqual(test, False)

	def test_price_is_valid_float(self):
		test = myCrawler.price_is_valid("this is a price 24.88 for a test")

		self.assertEqual(test, 24.88)
