import pytest
import yaml

from xueqiu_app.page.app import App


class TestMarket:
    def setup(self):
        self.app = App()

    def load_data(self):
        with open("./data.yml", encoding='utf-8') as f:
            result = yaml.safe_load(f)
        return result

    @pytest.mark.parametrize("stock_name", load_data("此处填写任意值代替self"))  # 装饰器特性，在类函数中的第一个数会传self
    def test_search(self, stock_name):
        search = self.app.start().goto_main().goto_market().goto_search()
        search.search(stock_name)
        assert search.is_choose(stock_name)

