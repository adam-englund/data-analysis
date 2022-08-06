import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Browse:
    
    ################################################################################
    def __init__(self):
        from selenium.webdriver.chrome.service import Service as ChromeService
        options = Options()
        options.headless = True
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"+\
            " (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
        options.add_argument("window-size=1400,600")
        options.add_argument("--incognito")
        prefs = {"profile.managed_default_content_settings.images": 2} # don't load images
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                           options=options)
      
    ################################################################################    
    def close(self):
        self.driver.close()
        self.driver.quit()

    ################################################################################
    def get(self, url):
        self.driver.get(url)
        time.sleep(random.randint(2, 8))

    ################################################################################
    def find_by_css(self, css_selector):
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)
        

    ################################################################################
    # def get_proxy():
    #     """ Adapted from https://stackoverflow.com/questions/59409418/how-to-rotate-selenium-webrowser-ip-address """
    #     options = Options()
    #     options.headless = True
    #     options.add_argument("window-size=700,600")
    #     driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    #     clear_output()
        
    #     try:
    #         driver.get("https://sslproxies.org/")
    #         table = driver.find_elements_by_tag_name("table")[0]
    #         df = pd.read_html(table.get_attribute("outerHTML"))[0]
    #         df = df.iloc[np.where(~np.isnan(df["Port"]))[0],:] # ignore nans

    #         ips = df["IP Address"].values
    #         ports = df["Port"].astype("int").values

    #         driver.quit()
    #         proxies = list()
    #         for i in range(len(ips)):
    #             proxies.append("{}:{}".format(ips[i], ports[i]))
    #         i = random.randint(0, len(proxies)-1)
    #         return proxies[i]
    #     except Exception as e:
    #         driver.close()
    #         driver.quit()
    #         raise e
