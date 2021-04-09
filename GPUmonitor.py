import logging
import argparse
import time

from selenium import webdriver

URL = "https://slack.com/workspace-signin"


formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)

class GPUmonitor():
    def __init__(self, url):
        self.url = url
        
    def open_driver(self):
        # prepare web driver
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        # self.options.add_argument("--disable-popup-blocking")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.url)
        self.driver.implicitly_wait(100)


    def close_driver(self):
        self.driver.close()

    def quit_driver(self):
        self.quit_driver()


    def to_slack_start(self, workspace="", email="", password="", message=""):
        self.workspace_url = "https://" + workspace + ".slack.com/"

        # Open a driver
        self.open_driver()

        try:
            self.driver.find_element_by_class_name("c-input_text").send_keys(workspace)
            self.driver.find_element_by_class_name("c-button--large").click()
            self.driver.find_element_by_id("email").send_keys(email)
            self.driver.find_element_by_id("password").send_keys(password)
            self.driver.find_element_by_id("signin_btn").click()
            self.driver.get(self.workspace_url)
            self.driver.get(self.workspace_url)

            self.driver.switch_to.alert.dismiss()

            self.driver.find_element_by_class_name("p-channel_sidebar__channel--im-you").click()

            print(message)
            self.driver.find_element_by_class_name("ql-editor").send_keys(message)
            # self.driver.find_element_by_class_name("c-texty_input__button--send")
        except:
            logging.warning("slack workspace [{}] not found".format(workspace))

        time.sleep(100)

        # Quit the driver
        self.quit_driver()
        return

if __name__ == "__main__":
    # define argments
    p = argparse.ArgumentParser()
    p.add_argument("--url", default=URL)
    p.add_argument("--slack_workspace", default="")
    p.add_argument("--email", default="")
    p.add_argument("--password", default="")
    p.add_argument("--message", default="")
    

    # parse argments
    args = p.parse_args()   

    # Build a GPUmonitor instance 
    gpumonitor = GPUmonitor(
        url=args.url
    )

    # GPU monitoring start
    gpumonitor.to_slack_start(
        workspace=args.slack_workspace,
        email=args.email,
        password=args.password,
        message=args.message
    )