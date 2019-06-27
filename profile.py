from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from pynput.keyboard import Key, Controller



class Bot:
    XPATHS = {
        'loginEmail': "//input[@id='email']",
        'loginBtn': "//input[@value='Log In']",
        'loginPass': "//input[@id='pass']",
        'accountSetting': "//div[text()='Account Settings']",
        'logoutBtn': "//span[text()='Log Out']",
        'acceptMutualFrndRequest':"//div[@class='clearfix _42ef' and .//span/a]//button[@class='_42ft _4jy0 _4jy3 _4jy1 selected _51sy']",
        'acceptRandomFrndRequest' : "//div[@class='clearfix _42ef' and .//span/a]//button[@class='_42ft _4jy0 FriendRequestAdd addButton _4jy3 _4jy1 selected _51sy']",            # rqst_random_ppl = "//div[@class='clearfix _42ef']//button[@class='_42ft _4jy0 FriendRequestAdd addButton _4jy3 _4jy1 selected _51sy']"
        'notificationTab':"//div[@class='_2n_9' and .//text()='Notifications']",
        'notificationList':"//a[@class='_33e _1_0e']",
        'frndSearchFirstResult':"//div[@class='_6v_0']",
        'friendsBtn':"//a[@role='button']//span[text()='Friends']",
        'commentBtnPost':"//a[@role='button' and text()='Comment']",
        'likeBtnPost':"//a[@role='button' and text()='Like']",
        'homePageLikePosts':"//a[@class=' _6a-y _3l2t  _18vj']",
        'timelineImageIcon':"(//input[@type='file'])[3]",
        'timelinePostBtn':"//button[@data-testid='react-composer-post-button']",
        'timelineOption1':"//span[@class='_1vp5']",
        'timelineOption2':"(//span[@class='_5qtp'])[1]",
        'timelineOption3':"(//div[@class='_1mf _1mj'])[1]",


    }

    ACTIONS={
        "scrollDown":"window.scrollTo(0, document.body.scrollHeight);",
        "scrollTop":"window.scrollTo(0, 0);"
    }

    MISC = {
        'url': "https://www.facebook.com/",
        'chromePath': 'chromedriver.exe', 
        'Hi_page': 'https://www.facebook.com/HI.global.page/?brand_redir=256197435586', 
        'Medecin_page': 'https://www.facebook.com/fr.mdm',
        'img_path':'email.png', 
        'accept_frnd_req_url':'https://www.facebook.com/friends/requests/?fcref=jwl', 
        'notification_page':'https://www.facebook.com/notifications', 
        'friend_search':"https://www.facebook.com/search/str/__FRIEND__/keywords_search?epa=SEARCH_BOX", 
        
        }

    PAGE_LOAD_TIME = 600
    WAIT_TIME = 100

    def __init__(self, setting_options=None,email=None,password=None):
        self.setting_options = setting_options
        self.driver = webdriver.Chrome(
                                    chrome_options=self.setting_options, executable_path=Bot.MISC['chromePath'])

        self.driver.set_page_load_timeout(Bot.PAGE_LOAD_TIME)
        self.wait = WebDriverWait(self.driver, Bot.WAIT_TIME)
        self.keyboard = Controller()
        self.email=email
        self.password=password


    @classmethod
    def change_page_load_time(cls, time):
        cls.PAGE_LOAD_TIME = time

    @classmethod
    def change_wait_time(cls, time):
        cls.WAIT_TIME = time


    def facebook_login(self):
        self.driver.get(Bot.MISC['url'])
        self.wait.until(EC.presence_of_element_located(
    (By.XPATH, Bot.XPATHS['loginEmail'])))
        self.driver.find_element_by_xpath(
                                        Bot.XPATHS['loginEmail']).send_keys(self.email)
        self.driver.find_element_by_xpath(
                                        Bot.XPATHS['loginBtn']).send_keys(self.password)
        self.driver.find_element_by_xpath(Bot.XPATHS['loginPass']).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        print("Successfully Logged In Facebook")

    def go_home(self):
        print("Reaching HomePage")
        self.driver.get(Bot.MISC['url'])

    def logout(self):
        self.go_home()
        print("Logging Out")
        self.wait.until(EC.presence_of_element_located(
    (By.XPATH, Bot.XPATHS['accountSetting'])))
        self.driver.find_element_by_xpath(Bot.XPATHS['accountSetting']).click()
        self.wait.until(EC.presence_of_element_located(
    (By.XPATH, Bot.XPATHS['logoutBtn'])))
        sleep(1)
        self.driver.find_element_by_xpath(
                                        Bot.XPATHS['logoutBtn']).click()
    def accept_friend_request(self):
        self.driver.get(Bot.MISC['accept_frnd_req_url'])
        self.wait.until(EC.presence_of_element_located(
        (By.XPATH, Bot.XPATHS['acceptMutualFrndRequest'])))
        friend_requests = self.driver.find_elements_by_xpath(Bot.XPATHS['acceptMutualFrndRequest'])
        totalRequests = len(friend_requests)
        if totalRequests > 5:
            friend_requests = friend_requests[:3]
        print("Total Friend Requests with Mutual Friends are: ", totalRequests)
        i = 1
        print("Accepting 5 Friend Requests..for testing purpose")
        for req in friend_requests:
            req.click()

            timeDelay = random.randrange(5, 10)  # Change Delay###############
            sleep(timeDelay)
            print("Accepted Requests: ", i)
            i += 1

        print("Sucessfuly Accepted Available Requests.")

    def add_random_ppl(self):
        print("Adding 5 People by requesting people with mutual friends.")

        
        self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, Bot.XPATHS['acceptRandomFrndRequest'])))
        add_friends = self.driver.find_elements_by_xpath(Bot.XPATHS['acceptRandomFrndRequest'])
        print("Found "+str(len(add_friends)) +
            " people with mutual Friends. Adding!!!")
        i = 1
        for req in add_friends:
            req.click()
            timeDelay = random.randrange(5, 10)  # Change Delay###############
            sleep(timeDelay)
            print("ADDED PEOPLE: ", i)
            i += 1

            if i > 2:
                break
        print("Sucessfuly Requested 5 People.")
    
    def press_down_enter():
        self.keyboard.press(Key.down)
        sleep(0.5)
        self.keyboard.press(Key.down)
        sleep(0.5)
        self.keyboard.press(Key.down)
        sleep(0.5)
        self.keyboard.press(Key.down)
        sleep(0.5)
        self.keyboard.press(Key.down)
        sleep(0.5)
        self.keyboard.press(Key.enter)

    def check_notifications(self):
        self.go_home()
        print("Randomly Checking Friends Notifications.")
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH,Bot.XPATHS['notificationTab'] )))
        self.driver.find_element_by_xpath(
        Bot.XPATHS['notificationTab'] ).click()
        sleep(2)
        self.driver.get(Bot.MISC['notification_page'])
        notification_hrefs = self.driver.find_elements_by_xpath(Bot.XPATHS['notificationList'])
        notification_hrefs = [n.get_attribute('href') for n in notification_hrefs]
        shuffle(notification_hrefs)
        notification_hrefs = notification_hrefs[:4]
        typee = ''
        for n in notification_hrefs:
            self.driver.get(n)
            sleep(6)
            print("Checking Notifications !!!")

    def unfriend(self,friend_name):
        self.driver.get(Bot.MISC['friend_search'].replace('__FRIEND__',friend_name))
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, Bot.XPATHS['frndSearchFirstResult'])))

        try:
            print("click 1")
            self.driver.find_element_by_xpath("(//div[@class='_6v_0']/a)[1]").click()
            sleep(5)
        except:
            pass

        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, Bot.XPATHS['friendsBtn'])))
        self.driver.find_element_by_xpath(Bot.XPATHS['friendsBtn']).click()
        dc = ActionChains(self.driver)

        frndbtn = self.driver.find_element_by_xpath(Bot.XPATHS['friendsBtn'])
        dc.move_to_element(frndbtn).move_by_offset(0, 0).click().perform()
        sleep(1)
        dc.release().perform()

        self.press_down_enter()
        print("Successfully Unfriended and Unfollowed")

    def like_post(self,postlink):
        self.driver.get(link)
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, Bot.XPATHS['commentBtnPost'])))
        sleep(3)
        likes = self.driver.find_elements_by_xpath(
            Bot.XPATHS['likeBtnPost'])
        for l in likes:
            try:
                l.click()
                break
            except:
                continue
        print("Successfully Liked")

    def comment_post(self,postlink,postcomment):
        self.driver.get(link)
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, Bot.XPATHS['commentBtnPost'])))
        sleep(3)
        comments = self.driver.find_elements_by_xpath(
                        Bot.XPATHS['commentBtnPost'])
        sleep(1)
        for c in comments:
            try:
                c.click()
                break
            except:
                continue
        for char in postcomment:
            self.keyboard.type(char)
            sleep(0.12)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)


        sleep(random.randrange(3, 5))
        print("Successfully Commented")

    def scroll_bottom(self,times=3):
        for i in range(time):
            print("Scrolling..")

            self.driver.execute_script(
                Bot.ACTIONS['scrollDown'])
            sleep(3)
    
    def scroll_top(self):
        self.driver.execute_script(Bot.ACTIONS['scrollTop'])

    def like_random_posts_on_homepage(self,num_like=3):
        self.go_home()
        self.scroll_bottom()
        like_divs = self.driver.find_elements_by_xpath(
                            Bot.XPATHS['homePageLikePosts'])
        print("Randomly Liking Posts")
        l = 0
        for like in like_divs:
            sleep(random.randrange(2, 3))
            l += 1
            try:
                like.click()
            except:
                l -= 1
                continue
            print("Liked a Post")
            if l > num_like:
                break
    
    
    def comment_random_posts_on_homepage(self,num_comment=3,comment=""):
        self.go_home()
        self.scroll_bottom()

        comment_divs = self.driver.find_elements_by_xpath(
            Bot.XPATHS['commentBtnPost'])
        print("Randomly Commenting Posts")
        t = 1

        for comment in comment_divs:
            t += 1
            try:
                comment.click()
            except:
                t -= 1
                continue
            sleep(1)
            for char in comment:
                keyboard.type(char)
                sleep(0.12)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            sleep(random.randrange(3, 5))
            print("Successfully Commented on ", t)
            if t > num_comment:
                break
    
    def gather_data_email_password(self,filepath):
        df = pd.read_excel(open(filepath, 'rb'), sheet_name='Sheet1')
        self.email=list(df['EMAIL'])[0]
        self.password=list(df['PASSWORD'])[0]
    
    def post_on_timeline(self,imgpath,post):
        self.go_home()
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, Bot.XPATHS['timelineOption1'])))
        driver.find_element_by_xpath(Bot.XPATHS['timelineOption1']).click()
        sleep(2)
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, Bot.XPATHS['timelineOption2'])))
        driver.find_element_by_xpath(
            Bot.XPATHS['timelineOption2']).click()  # Create Post##########
        sleep(1)

        print("Posting!!!!   ")
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, Bot.XPATHS['timelineImageIcon'])))

        photo = driver.find_element_by_xpath(Bot.XPATHS['timelineImageIcon'])
        photo.send_keys(imgpath)
        sleep(3)

        driver.find_element_by_xpath(Bot.XPATHS['timelineOption3']).click()
        sleep(1)
        for char in post:
            keyboard.type(char)
            sleep(0.12)
        print("Successfully Post on Timeline")



if __name__ == "__main__":
    fbdriver=Bot()
    fbdriver.facebook_login()
    





        












