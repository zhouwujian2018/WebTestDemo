from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import pytest
import yaml


class TestDemo:

    def setup(self):
        self.webdriver = webdriver.Chrome(r'D:\Download\chromedriver.exe')
        self.webdriver.maximize_window()
        self.webdriver.get("https://cn.bing.com/")

    def test_case(self):
        PublicCase("search_demo.yaml",self.webdriver).run()

    def teardown(self):
        self.webdriver.quit()
        pass


class PublicCase:
    def __init__(self, path,driver:WebDriver):
        self.driver = driver
        with open(path, encoding='utf-8') as f:
            self.steps = yaml.safe_load(f)

    def __find_element(self,step:dict):
        global element
        if "id" in step.keys():
            element = self.driver.find_element_by_id(step["id"])
        elif "xpath" in step.keys():
            element = self.driver.find_element_by_xpath(step["xpath"])
        elif "css" in step.keys():
            element = self.driver.find_element_by_css_selector(step["css"])
        elif "tag" in step.keys():
            element = self.driver.find_element_by_tag_name(step["tag"])
        else:
            print('模板中没有定义', step.keys())
        return element

    def run(self):
        for step in self.steps:
            if isinstance(step, dict):
                # 元素定位
                self.element = self.__find_element(step)
                # 操作
                if "input" in step.keys():
                    self.element.send_keys(step["input"])
                elif "get" in step.keys():
                    elements = self.driver.find_elements(By.XPATH, step["get"])
                    for el in elements:
                        text = el.text
                        print(text)
                elif "winds" in step.keys():
                    cur_handle = self.driver.current_window_handle
                    try:
                        handles = self.driver.window_handles
                        for handle in handles:
                            if handle != cur_handle:
                                self.driver.switch_to.window(handle)
                                break
                    except:
                        print(self.driver.title)
                elif "frame" in step.keys():
                    self.driver.switch_to.frame(step["frame"])
                else:
                    self.element.click()
