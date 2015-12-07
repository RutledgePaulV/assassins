from unittest import TestCase, TestSuite
import unittest

from Helpers.encryption import *


class TestClass(TestCase):

	SALT = '$$5+&zvh8*vtl895^g-qv7$#usbmmd2g^8&!%ng)i1t^4@i@h!'

	def test_encryption_to_decryption(self):
		pk = '1'

		encrypted = encrypt_to_link(pk, self.SALT)

		decrypted = decrypt_to_original(encrypted, self.SALT)

		assert pk == decrypted


if __name__ == '__main__':
	unittest.main()