# a way to realize quik query_filling
<br><b>some tips:</b><br>
<br>用于填写问卷星的问卷，填空题需要修改questions.json文件，性别题选第一个，其他单选多选题随机选，点击后再选择功能待拓展。<br>
<br>.json文件的键是问题关键字，如“姓名”“学号”“专业”“电话”“mail”“联系方式”等，这个只能根据自我需求尽量完善可能出现的问题；后来改动过程中将问卷链接link也放到这个文件中了，主要是避免繁琐和避免修改源码。<br>
<br>需要注意的是，某些值应该写数字，不能用字符串，如电话号码。<br>
<br><b>about time:</b><br>
<br>采用的是24小时制，开始运行前通过修改query_filling.py中hold.hold(h,m,s)的参数设定开始填写的时间，示例用的是18,0,0；<br>
<br><b>announcement:</b><br>
<br>本人才疏学浅，有不妥之处敬请指出和谅解，我会尽快改正。<br>
