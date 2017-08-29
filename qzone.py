#coding=utf-8
from selenium import webdriver
import sys, time, pickle, requests, re
from lxml import etree

#将utf-8转为默认编码

stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf-8')

class Qzone(object):
    def __init__(self):
        self.friendUrl = 'https://user.qzone.qq.com/xxxx/311'
        self.myUrl = 'https://user.qzone.qq.com/xxxx/main'
        self.url = 'https://qzone.qq.com/'
        self.currentPage = 1
        self.nextPage = True
        self.frame = True

    def getCookies(self):
        # driver = webdriver.Firefox()
        driver = webdriver.PhantomJS()
        driver.get(self.url)
        time.sleep(2)
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        time.sleep(1)
        #usernmae
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys('xxxxxx')
        #password
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('xxxxxx')
        time.sleep(1)
        # driver.find_element_by_id('go').click()
        driver.find_element_by_id('login_button').click()
        time.sleep(4)
        # driver.find_element_by_id('nav_bar_main').click()
        driver.implicitly_wait(3)
        #get cookies
        cookies = driver.get_cookies()
        for cookie in cookies:
            # print cookie
            driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry') if k in cookie})

        # pickle.dump(cookie, open('qzone.pkl', 'wb'))
        print 'storing cookies finished....'
        print driver.page_source
        # login = driver.find_element_by_xpath('//a[@href="#signin"]')

    def nextPage(self, driver, page):
        #go to next page
        print 'find next page....'
        driver.find_element_by_xpath("//input[@class='textinput']").clear()
        driver.find_element_by_xpath("//input[@class='textinput']").send_keys(page)
        time.sleep(1)
        driver.find_element_by_xpath("//button[contains(.,'确定')]").click()

    def getContent(self):
        #login....
        print 'starting phantomJs....'
        # print 'starting Firefox.....'
        lTime = time.time()
        # driver = webdriver.Firefox()
        driver = webdriver.PhantomJS()
        driver.get(self.url)
        # time.sleep(2)
        print 'start login...'
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        time.sleep(0.5)
        #username
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys('xxxxx')
        #password
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('xxxxx')
        time.sleep(0.5)
        # driver.find_element_by_id('go').click()
        driver.find_element_by_id('login_button').click()
        time.sleep(2)
        lEndTime = time.time()
        print 'login finished...'
        print 'login page %s time: %s' % (self.currentPage, lEndTime - lTime)
        #-------------content------------
        #timeout
        driver.set_page_load_timeout(5)
        #main get friend url
        try:
            driver.get(self.friendUrl)
        except Exception as e:
            pass
        finally:
            #the first page need to weitch to frame.others don't need
            for i in range(27):
                if i == 0:
                    pTime = time.time()
                    time.sleep(0.6)
                    driver.switch_to.frame('app_canvas_frame')
                else:
                    pTime = time.time()
                time.sleep(0.8)
                content = driver.page_source
                self.to_txt(content, i)
                pEndTime = time.time()
                print 'get friend page %s cost time:%s' % (self.currentPage, pEndTime - pTime)
                # to next page
                print 'find next page %s....' % str(i+2)
                driver.find_element_by_xpath("//input[@class='textinput']").clear()
                driver.find_element_by_xpath("//input[@class='textinput']").send_keys(str(i+2))
                time.sleep(1)
                driver.find_element_by_xpath("//button[contains(.,'确定')]").click()
                time.sleep(3)

    def to_txt(self, content, num):
        print 'starting to txt...'
        # content = etree.HTML(content)
        #[0]content,[1]timestamp.[2][3]upvote person and it's url.[4]list of comments.
        # p = re.compile('<li class="feed ".*?<div class="bd".*?<pre.*?class="content">(.*?)</pre>'+\
        #'.*?<div class="ft".*?<a.*?title="(.*?)".*?<div class="feed_like.*?<a href="(.*?)".*?tit'+\
        #'le="(.*?)".*?<div class="comments_content">(.*?)<div class="comments_poster_bd comments_poster_default"', re.S)
        p = re.compile('<li class="feed ".*?<div class="bd".*?<pre.*?class="content">(.*?)</pre>'+\
        '.*?<div class="ft".*?<a.*?title="(.*?)".*?<div class="feed_like')
        # strinfo = re.compile('<img.*?>')
        allSS = p.findall(content)
        with open('qzone.txt', 'a') as f:
            for item in allSS:
                f.write('%s, %s\n' % (item[1], item[0]))
        print 'write %s finished...' % num

    def fix_text(self, file_name):
        print 'starting to fix test....'
        strinfo = re.compile('<img.*?>')
        with open(file_name, 'r') as f:
            print 'reading....'
            items = f.readlines()
            print 'whole ShuoShuo:%s' % len(items)
            with open('qzone01.txt', 'w') as fw:
                print 'writing.....'
                for item in items:
                    if 'img' in item:
                        fw.write(strinfo.sub('',item))
                    else:
                        fw.write(item)
        print 'fix finished...'

    def test(self):
        #login....
        print 'starting phantomJs....'
        lTime = time.time()
        driver = webdriver.Firefox()
        # driver = webdriver.PhantomJS()
        driver.get(self.url)
        # time.sleep(2)
        print 'start login...'
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        time.sleep(0.5)
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys('xxxxx')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('xxxxxx')
        time.sleep(0.5)
        # driver.find_element_by_id('go').click()
        driver.find_element_by_id('login_button').click()
        time.sleep(2)
        lEndTime = time.time()
        print 'login finished...'
        print 'login page %s time: %s' % (self.currentPage, lEndTime - lTime)
        #-------------content------------
        pTime = time.time()
        driver.get(self.friendUrl)
        time.sleep(0.6)
        driver.switch_to.frame('app_canvas_frame')
        time.sleep(0.6)
        # print driver.page_source
        print 'find next page....'
        driver.find_element_by_xpath("//input[@class='textinput']").clear()
        driver.find_element_by_xpath("//input[@class='textinput']").send_keys(2)
        time.sleep(1)
        driver.find_element_by_xpath("//button[contains(.,'确定')]").click()

    def run(self):
        self.fix_text('qzone.txt')
        # self.to_txt(self.getContent())
        # self.test()
        # self.getContent()

if __name__ == '__main__':
    q = Qzone()
    q.run()
