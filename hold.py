import time
class hold():
    def __init__(self,hour,minute,second):
        time_tuple=time.localtime(time.time())#3、4、5分别代表时分秒
        hourGap=hour-time_tuple[3]
        minuteGap=minute-time_tuple[4]
        secondGap=second-time_tuple[5]
        holdTime=hourGap*3600+minuteGap*60+secondGap
        print(holdTime)
        time.sleep(holdTime)
        return None