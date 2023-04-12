from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json,random,hold

#we need a special finction to help circulate here
def opeDiv(i,driver,obj):
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

def write(link,driver,obj):
    #通过问卷url获取并打开
    driver.get(link)
    #try filling the query, if not accessible, fill in by hand
    for i in range(1,13):   #这里实际上可以通过爬虫确定问题数目减少循环次数
        try:
            opeDiv(i,driver,obj)
        except:
            continue
    nodeOn=driver.find_element(By.XPATH,'//*[@id="ctlNext"]')
    nodeOn.click()#提交，这一条一般是不变的
    try:#尝试点击验证，这个不耽误时间，停留0.1秒就够了
        time.sleep(0.5)#必要的间歇时间，没有的话可能找不到节点
        element = driver.find_element(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[1]')
        element.click()#点击确认验证
        yanz = driver.find_element(By.XPATH,'//*[@id="SM_BTN_1"]/div[1]/div[4]')
        yanz.click()#点击验证按钮
        print("end time:%d"%time.localtime(time.time())[5])
        print("已点击验证按钮!")#time.localtime(time.time())[5]#到这一步只需要2秒钟
        time.sleep(5)
    except:
        time.sleep(60)#为了防止出现任何可能的bug，人工盯防，一旦出现停止程序手动  填写  或  验证
        pass
    #下面需要一个判断是否填写成功的方法，当然前台运行浏览器时可以直观看到
    feedback=driver.find_element(By.XPATH,'//*[@id="divdsc"]')
    print(feedback.text)
    time.sleep(5)

#预加载浏览器，加快提交速度
def openChrome():
    option = webdriver.ChromeOptions()
    #可以补充一个后台运行的插件，这样会更快，同样后面需要另一个插件判定是否填写成功
    #option.add_argument("headless")
    #加速优化
    option.add_argument("--disable-images")
    option.add_argument("--disable-javascript")
    #优化页面加载策略
    option.page_load_strategy='eager'   #这一项可能会出现问题，大多数是网络问题，更换网络即可
    #绕过问卷星的防selenium设置
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    return driver
    
#function main()
if __name__=="__main__":
    obj=json.load(open("questions.json","r",encoding="utf-8"))#读取json文件获取要填写的信息
    driver=openChrome()#预加载浏览器
    link=input("THE LINK OF THE QUERY:\n")  #嵌入链接
    try:
        hold.hold(18,0,0)
    except:
        pass
    print("start time:%d"%time.localtime(time.time())[5])
    while True:
        try:
            write(link,driver,obj)
            break
        except:
            time.sleep(0.2) #这里也可以pass，我主要考虑系统延迟问题需要不断刷新
            continue
    time.sleep(30)

