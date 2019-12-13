import microbit
import time
class AnimBlock():
    def __init__(self,ranges=[],times=[],data=[],type="Linear"):
        self.type = type
        self.ranges = ranges        
        self.times = times        
        self.data = data
    def getDefaultValue(self):
        return self.data[0]
    def interpolateLinear(self,range,v1,v2):
        return  (v1 * (1.0 - range) + v2 * range)
    def getValue(self,anim,time):
        rangesCount = len(self.ranges)
        timesCount = len(self.times)
        dataCount = len(self.data)
        if(self.type != "NONE" and dataCount > 1):
            if(anim >=0 and anim < rangesCount):
                anim_range = self.ranges[anim]
            else:
                return self.data[0]
            if(anim_range[0] != anim_range[1]):
                pos = anim_range[0]
                nStart = anim_range[0]
                nEnd = anim_range[1]
                if(time >= self.times[nEnd]):
                    return self.data[nEnd]
                elif(time <= self.times[nStart]):
                    return self.data[nStart]

                pos = self.binarySearchForIndex(time,nStart,nEnd,self.times) or pos
                t1 = self.times[pos]
                t2 = self.times[pos+1]
                r = (time - t1) / (t2 - t1)
                vType = self.type
                if(vType == "Linear"):
                    return self.interpolateLinear(r, self.data[pos], self.data[pos+1])
            else:
                return self.data[anim_range[0]]
        else:
            return self.data[0]
    def addKey(self,time,data):
        index = self.getNextKeyIndex(1,time)
    def binarySearchForIndex(self,value,nStart,nEnd,values):
        pos = None
        while(True):
            if(nStart >= nEnd):
                pos = nStart
                break
            if(((nStart + nEnd)%2) == 1 ):
                nMid = (nStart + nEnd - 1)/2
            else:
                nMid = (nStart + nEnd)/2
            nMid = int(nMid)
            startP = (values[nMid])
            endP = (values[nMid + 1])
                    
            if(startP <= value and value < endP ):
                pos = nMid
                break
            elif(value < startP ):
                nEnd = nMid
            elif(value >= endP):
                nStart = nMid+1
        return pos
    def getNextKeyIndex(self,anim,time):
        rangesCount = len(self.ranges)
        timesCount = len(self.times)
        dataCount = len(self.data)
        if(self.type != "NONE" and dataCount > 1):
            if(anim >=0 and anim < rangesCount):
                anim_range = self.ranges[anim]
            else:
                return
            if(anim_range[0] != anim_range[1]):
                pos = anim_range[0]
                nStart = anim_range[0]
                nEnd = anim_range[1]
                if(time >= self.times[nEnd]):
                    return nEnd
                pos = self.binarySearchForIndex(time,nStart,nEnd,self.times) or pos
                for i in range(pos-1, anim_range[0],-1):
                    if(self.times[i]>=time):
                        pos = i
                    else:
                        break
                return pos
        else:
            if((self.times[0] != None) and (self.times[0] >= time) ):
                return 0
        def setRangeByIndex(self,index,rangeFirst,rangeSecond):
            if(not self.ranges[index]):
                self.ranges[index] = []
            self.ranges[index] = [rangeFirst,rangeSecond]
class Timer():
    def __init__(self,timerManager,callback):
        self.timerManager = timerManager
        self.enabled = True
        self.callback = callback
        self.dueTime = None
        self.period = None
        self.enabled = False
        self.delta = None
        self.lastTick = 0
        self.MAX_TIMER_DUE_TIME = 30*24*60*60*1000
    def change(self,dueTime=None,period=None):
        self.dueTime = dueTime
        self.period = period
        if(dueTime == None):
            self.timerManager.removeTimer(self)
        else:
            self.lastTick = self.timerManager.getTicksMS() + dueTime - (period or 0)
            self.timerManager.addTimer(self)
    def tick(self,tick_count):
        if(not tick_count):
            tick_count = self.timerManager.getTicksMS()
        lastTick = self.lastTick
        if( (tick_count-lastTick)>=(self.period or 0) or ((tick_count<lastTick) and ((tick_count+self.MAX_TIMER_DUE_TIME)<lastTick))):
            self.delta = tick_count - lastTick
            self.lastTick = tick_count
            if(self.period == None):
                self.timerManager.removeTimer(self)
            # do activation
            if(self.callback):
                self.callback(self)
            return True
    def getDelta(self,max_delta=None):
        max_delta = max_delta or (self.period or 10000) * 2
        if(self.delta):
            if(max_delta > self.delta):
                return self.delta
            else:
                return max_delta
        else:
            return 0
class TimeManager():
    def __init__(self):
        self.timers = []
    def run(self):
        while True:
            last_tick = self.getTicksMS()
            self.last_tick = last_tick
            for index in range(len(self.timers)):
                timer = self.timers[index]
                if(timer.enabled):
                    timer.tick(last_tick)
    def addTimer(self,timer):
        if(not timer or self.isExisted(timer)):
            return
        timer.enabled = True
        self.timers.append(timer)
    def removeTimer(self,timer):
        if(not timer or not self.isExisted(timer)):
            return
        timer.enabled = False
        self.timers.remove(timer)
    def isExisted(self,timer):
        if(not timer):
            return False
        for index in range(len(self.timers)):
            if(self.timers[index] == timer):
                return True
    def getTicksMS(self):
        return time.ticks_ms()
def callback(t):
    if(t):
        delta = t.getDelta()
        microbit.display.scroll(delta)
timer_manager = TimeManager()
timer = Timer(timer_manager,callback)
timer.change(0,5000)
timer_manager.run()