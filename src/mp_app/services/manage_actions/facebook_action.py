import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.mp_app.constants import config
from typing import Union, List
from src.mp_app.common.log import logger


class FacebookAction:
    def __init__(self, driver_instance: object):
        self.base_url = "https://www.facebook.com"
        self.driver = driver_instance.driver
        self.profile_name = driver_instance.profile_name
        self.wait = WebDriverWait(self.driver, 50)

    def post(self, url: str, content: Union[str, List, None], path_images: Union[str, List, None]):
        try:
            self.driver.get(url)
            logger.info(f"✅ Post start", extra=self.profile_name)
            time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
            popup_upload_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, ".//span[@dir='auto']//span[text()='Ảnh/video']")))
            popup_upload_element.click()
            time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))

            if content:
                text_input_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//div[@role='textbox']")))
                if isinstance(content, str):
                    content = content
                else:
                    content = random.choice(content)
                text_input_element.send_keys(content)
                logger.info(f"👉 Write content: {content}", extra=self.profile_name)
                time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))

            if path_images:
                if isinstance(path_images, str):
                    path_images = [path_images]
                for path_image in path_images:
                    image_input_element = self.driver.find_element(
                        By.XPATH,
                        ".//form[@method='POST']//input[@accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv']",
                    )
                    image_input_element.send_keys(path_image)
                    time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                    logger.info(f"👉 Upload image: {path_image}", extra=self.profile_name)
            post_button_element = self.driver.find_element(By.XPATH, ".//span[@dir='auto']//span[text()='Đăng']")
            self.driver.execute_script("arguments[0].click();", post_button_element)
            logger.info(f"✅ Post done", extra=self.profile_name)
            time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
        except Exception as ex:
            logger.error(f"❌ Error: {ex}", extra=self.profile_name, exc_info=True)

    def comment_newfeed(self, url: str, content: Union[str, List, None], path_images: Union[str, List, None], num_comments: int = 20):
        try:
            self.driver.get(url)
            logger.info(f"✅ Comment start", extra=self.profile_name)
            time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
            feed_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='feed']")))
            logger.info(f"👉 Load done: {feed_element.is_displayed()}", extra=self.profile_name)
            for i in range(1, num_comments):
                logger.info(f"👉 Comment on post: {i}", extra=self.profile_name)
                try:
                    # new feed personal
                    post_element = feed_element.find_element(By.XPATH, f"./div/div[{i}]")
                except:
                    # new feed group
                    post_element = feed_element.find_element(By.XPATH, f"./div[{i}]")
                    # ignore empty element in group
                    if i == 1:
                        continue
                print(post_element)
                self.driver.execute_script("return arguments[0].scrollIntoView();", post_element)
                time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                try:
                    # self.wait.until(EC.visibility_of_element_located((By.XPATH, post_element.get_attribute("xpath"))))
                    text_input_element = post_element.find_element(By.XPATH, ".//div[@aria-label='Viết bình luận']")
                    text_input_element.click()
                    time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                    # try:
                    #     post_element = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                    #     time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                    #     text_input_element = post_element.find_element(By.XPATH, ".//div[@aria-label='Viết bình luận']/p")
                    #     print(post_element)
                    # except:
                    #     pass
                except Exception as ex:
                    logger.warning(f"⚠️ Warning: {ex}", extra=self.profile_name)
                    continue
                if content and path_images:
                    if isinstance(path_images, str):
                        path_images = [path_images]
                    if isinstance(content, str):
                        content_post = content
                    else:
                        content_post = random.choice(content)
                    for path_image in path_images:
                        text_input_element.send_keys(content_post)
                        logger.info(f"👉 Write content: {content}", extra=self.profile_name)
                        time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                        print(post_element)
                        image_input_element = post_element.find_element(By.TAG_NAME, "input")
                        image_input_element.send_keys(path_image)
                        time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                        logger.info(f"👉 Upload image: {path_image}", extra=self.profile_name)
                        post_button_element = post_element.find_element(By.XPATH, ".//div[@aria-label='Bình luận']")
                        self.driver.execute_script("arguments[0].click();", post_button_element)
                        time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                elif content:
                    if isinstance(content, str):
                        content = content
                    else:
                        content = random.choice(content)
                    text_input_element.send_keys(content)
                    logger.info(f"👉 Write content: {content}", extra=self.profile_name)
                    time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                    post_button_element = post_element.find_element(By.XPATH, ".//div[@aria-label='Bình luận']")
                    self.driver.execute_script("arguments[0].click();", post_button_element)
                    time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))
                logger.info(f"✅ Comment done post: {i}", extra=self.profile_name)
        except Exception as ex:
            logger.error(f"❌ Error: {ex}", extra=self.profile_name, exc_info=True)
