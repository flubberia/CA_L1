__author__ = 'sineriya'
import unittest
import main

# -*- coding: utf-8 -*-


class TestXml(unittest.TestCase):
    def test_parse_xml(self):
        print('1')
        res = [main.Bank('Банк', 'https:/', '//*[@id="selectByB"]/tr[2]/td[2]', '//*[@id="selectByB"]/tr[2]/td[3]')]
        self.assertEqual(main.parse_xml("test_inp.xml"), res)

    def test_get_data_from_url(self):
        print('2')
        bank = main.Bank('Банк', 'privatbank', '//*[@id="selectByB"]/tr[2]/td[2]', '//*[@id="selectByB"]/tr[2]/td[3]')
        money1 = main.get_data_from_url(bank, True)
        self.assertEqual(money1, main.Money("20", "22"))

if __name__ == "__main__":
    unittest.main()