from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json,random,hold

#we need a special finction to help circulate here
def opeDiv(i):
    lst=list(obj.keys())#获取可以填写的项目
    #step1
    div=driver.find_element(By.ID,"div"+str(i))
    #step2
    typeDiv=div.get_attribute("type")
    #step3
    if typeDiv=="1":
        #operate as the text input-send_keys(content)
        node=driver.find_element(By.XPATH,'//input[@id="q%s"]'%str(i))
        for i in lst:
            if i in div.text:
                node.send_keys(obj[i])
                break
            else:
                continue
        return
    elif typeDiv=="3":
        #operate as the radio input-click()
        node=driver.find_element(By.XPATH,'//*[@id="div%s"]/div[2]/div[1]/span/a'%str(i))
        node.click()
    elif typeDiv=="4":
        #operate as the checkbox input-click()
        node1=driver.find_element(By.XPATH,'//*[@id="div%s"]/div[2]/div[%d]/span/a'%(str(i),random.randint(1,4)))
        #上面的节点是以四个多选项为例进行的，并且选择的选项是随机的
        node1.click()
    else:
        return

def write():
    #通过问卷url获取并打开
    driver.get(link)
    #try filling the query, if not accessible, fill in by hand
    for i in range(1,13):   #这里实际上可以通过爬虫确定问题数目减少循环次数
        try:
            opeDiv(i)
        except:
            continue
    try:
        nodeOn=driver.find_element(By.XPATH,'//*[@id="ctlNext"]')
        nodeOn.click()#提交，这一条一般是不变的
    except:
        pass
    try:    #尝试点击验证，这个不耽误时间，停留0.1秒就够了
        time.sleep(0.5)#必要的间歇时间，没有的话可能找不到节点
        try:
            element = driver.find_element(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[1]')
            element.click()#点击确认验证
        except:
            pass
        yanz = driver.find_element(By.XPATH,'//*[@id="SM_BTN_1"]/div[1]/div[4]')
        yanz.click()#点击验证按钮
        print("end time:%d"%time.localtime(time.time())[5])
        print("已点击验证按钮!")#time.localtime(time.time())[5]#到这一步只需要2秒钟
        time.sleep(5)
    except:
        time.sleep(60)#为了防止出现任何可能的bug，人工盯防，一旦出现停止程序手动  填写  或  验证
        pass
    #下面需要一个判断是否填写成功的方法，当然前台运行浏览器时可以直观看到
    try:
        feedback=driver.find_element(By.XPATH,'//*[@id="divdsc"]')
        print(feedback.text)
    except:
        pass
    time.sleep(5)

#预加载浏览器，加快提交速度
def openChrome():
    d = webdriver.Chrome(options=option)
    d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    d.get(link)
    return d

def setOption():
    opt = webdriver.ChromeOptions()
    #opt.add_argument("headless")
    #加速优化
    opt.add_argument("--disable-images")
    option.add_argument("--disable-javascript")
    #优化页面加载策略
    opt.page_load_strategy='eager'   #这一项可能会出现问题，大多数是网络问题，更换网络即可
    #绕过问卷星的防selenium设置
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('useAutomationExtension', False)
    #以安卓系统的微信浏览器为请求头，模拟微信环境[这里解决的是“只能通过微信填写”这个问题]
    opt.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255"')
    return opt

global driver,obj,link,option

obj=json.load(open("questions.json","r",encoding="utf-8"))  #读取json文件获取要填写的信息
link=obj["link"]  #嵌入链接
option=setOption()
driver=openChrome() #预加载浏览器

#function main()
if __name__=="__main__":
    try:
        hold.hold(18,0,0)
    except:
        pass
    print("start time:%d"%time.localtime(time.time())[5])
    while True:
        try:
            write()
            break
        except:
            time.sleep(0.2) #这里也可以pass，我主要考虑系统延迟问题需要不断刷新
            continue
    time.sleep(60)

