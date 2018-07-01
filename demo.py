# -*- coding: utf-8 -*-
"""
记录登录
"""
import dbctrl.saveobject
import timecontrol
import pubcore
import pubdefines
import pubglobalmanager
import math
import time

import threading

class CDemo(dbctrl.saveobject.CSaveData):

    
    CountNum = 120
    isCount = True
    timeout = False
    begin = False
    restart = False
    isrestart = False
    isgameover = False
    pscore = -1
    score1 = 0
    score2 = 0
    score3 = 0


    def GetKey(self):
        return "loginrecord"

    def Init(self):
        super(CDemo, self).Init()
        self.CheckTimer()

    def CheckTimer(self):
        timecontrol.Remove_Call_Out("loginrecord")
        pubdefines.FormatPrint("历史排行榜第一 %s" % self.m_Data.get("score1", 0))
        pubdefines.FormatPrint("历史排行榜第二 %s" % self.m_Data.get("score2", 0))
        pubdefines.FormatPrint("历史排行榜第三 %s" % self.m_Data.get("score3", 0))
        timecontrol.Call_Out(pubcore.Functor(self.CheckTimer), 300, "loginrecord")

    def NewItem(self):
        #self.m_Data.setdefault("total", 0)
        self.m_Data.setdefault("score1",0)
        self.m_Data.setdefault("score2",0)
        self.m_Data.setdefault("score3",0)
        #self.m_Data["total"] += 1
        self.score1 = self.m_Data["score1"]
        self.score2 = self.m_Data["score2"]
        self.score3 = self.m_Data["score3"]
        
        #self.m_Data["score1"] = 0
        #self.m_Data["score2"] = 0
        #self.m_Data["score3"] = 0
        
        self.Save()

    def CalPos(self, oClient, dData):
        self.begin = dData["BeginCountDown"]
        self.restart = dData["Restart"]
        self.isgameover = dData["isgameover"]
        self.pscore = dData["pscore"]

        
       
        

        if self.restart:
           pubdefines.FormatPrint("restart")
           self.CountNum = 120
           self.isrestart = True
        
        
        if self.begin:
           #pubdefines.FormatPrint("开始传输数据")
           dReturn = {
                 "action": "show",
                 "Count" : self.CountNum ,
                 "timeout": self.timeout ,
                 "isrestart": self.isrestart,
                 "score1":self.m_Data["score1"],
                 "score2":self.m_Data["score2"],
                 "score3":self.m_Data["score3"]

             }
           oClient.Send(dReturn)
           if self.restart:
              self.isrestart = True
           if self.restart== False:
              self.isrestart = False
                
           if self.isCount:
              pubdefines.FormatPrint("开始Timer")
              t = threading.Timer(1.0, self.CountDown)
              t.start()  

           self.isCount = False
           
           if self.pscore != -1:
              if self.pscore >= self.score1:
                 self.m_Data["score3"] = self.score2
                 self.m_Data["score2"] = self.score1
                 self.m_Data["score1"] = self.pscore
                 self.Save()
                 self.pscore = -1
              elif self.pscore >= self.score2:
                 self.m_Data["score3"] =self.score2
                 self.m_Data["score2"] = self.pscore
                 self.Save()
                 self.pscore = -1
              elif self.pscore >= self.score3:
                 self.m_Data["score3"] = self.pscore
                 self.Save()
                 self.pscore = -1
              else:
                 self.pscore = -1

          

    def CountDown(self):
        
            #pubdefines.FormatPrint("CountDown")
            self.CountNum = self.CountNum-1
            global t
            t = threading.Timer(1.0,self.CountDown)
            t.start()
            if self.CountNum == 0: # 计时停止时间
               pubdefines.FormatPrint("timeout")
               t.cancel()
               self.timeout = True
            if self.isgameover: # 游戏结束
               pubdefines.FormatPrint("gameover")
               t.cancel()
               
           



def Init():
    if pubglobalmanager.GetGlobalManager("demo"):
        return
    oManger = CDemo()
    pubglobalmanager.SetGlobalManager("demo", oManger)
    oManger.Init()
    
    

def Record():
    pubglobalmanager.CallManagerFunc("demo", "NewItem")

def OnCommand(oClient, dData):
    pubglobalmanager.CallManagerFunc("demo", "CalPos", oClient, dData)


