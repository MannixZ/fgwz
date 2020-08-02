import logging

import allure
from selenium.webdriver.common.by import By


def handle_black(func):
    logging.basicConfig(level=logging.INFO)
    def wrapper(*args, **kwargs):  # *args 代表不带关键字参数-例如:value，**kwargs 代表带关键字参数-例如:value=1
        _black_list = [
            (By.XPATH, "//*[@resource-id='com.xueqiu.android:id/iv_close']")
        ]
        from xueqiu_app.page.base_page import BasePage  # 为了解决循环导入的问题，因为BasePage也导入了handle_black，所以把该导入语句放到该位置上
        instance: BasePage = args[0]  # : BasePage 为 instance 变量的类型，args[0]相当于类函数库的实例变量self
        try:
            logging.info("run " + func.__name__ + "\n args: \n" + repr(args[1: ]) + "\n" + repr(kwargs))
            element = func(*args, **kwargs)
            _error_num = 0
            instance.set_implicitly_wait(3)
            return element
        except Exception as e:
            instance.screenshot("tmp.png")  # 执行错误进行截图
            with open("tmp.png", "rb") as f:
                content = f.read()
            allure.attach(content, attachment_type=allure.attachment_type.PNG)  # 以附件的形式放到allure 报告中
            logging.error("element not found, handle black list")
            instance.set_implicitly_wait(1)
            # 如果没找到，就进行黑名单处理
            if instance._error_num > instance._max_err_num:
                # 如果 erro 次数大于指定次数，清空 error 次数并报异常
                instance._error_num = 0
                raise e
            instance._error_num += 1
            for ele in _black_list:
                # 对黑名单进行点击
                eles = instance.finds(ele)
                if len(eles) > 0:
                    eles[0].click()
                    return wrapper(*args, **kwargs)
            raise ValueError("元素不在黑名单中")
    return wrapper