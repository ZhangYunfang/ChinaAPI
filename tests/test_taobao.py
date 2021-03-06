# coding=utf-8
from unittest import TestCase
from chinaapi.taobao.open import Client, App
from chinaapi.exceptions import ApiError


class TaobaoTest(TestCase):
    """
    # 使用这里公开的app：
    https://github.com/jimboybo/itaobox/blob/083e66bdce899ff8b9ea8be5fd9280529c4ee216/u/system/config/app_config.php
    注意：不同的app会有不同的权限，所以测试如果不成功，有可能是权限不足（详细原因可以查看返回的ApiError错误信息）
    """

    def setUp(self):
        self.app = App('21532233', '1d5f36785a0bfb84952a69c5dd3203fd')
        self.client = Client(self.app)

    def test_session(self):
        self.client = Client(self.app, 'session')
        self.assertEqual(self.client.session, 'session')
        self.client.session = 'session2'
        self.assertEqual(self.client.session, 'session2')

    def test_is_retry_error(self):
        self.assertTrue(self.client._is_retry_error(ApiError('', 0, '', 'ism.demo-error')))
        self.assertFalse(self.client._is_retry_error(ApiError('', 0, '', 'other_error')))

    def test_item_cats_get(self):
        r = self.client.itemcats.get(cids=14)
        self.assertEqual(14, r.item_cats.item_cat[0].cid)

    def test_shop_cats_list_get(self):
        r = self.client.shopcats.list.get(cids=14)
        self.assertEqual(68, len(r.shop_cats.shop_cat))

    def test_not_exist_api(self):
        with self.assertRaises(ApiError) as cm:
            self.client.not_exist_api.get()
        self.assertEqual('Invalid method', cm.exception.message)