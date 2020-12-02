from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocol
from BEService import TalkService
from BEService.ttypes import *
import time, json, requests, os, random, ast, datetime, sys, concurrent.futures

class BE_Team:
    def __init__(self, myToken, myApp, pool=False):
        self.lineServer =  "https://ga2.line.naver.jp"
        self.thisHeaders = {}
        splited = myApp.split("\t")
        self.thisHeaders["x-line-access"] = myToken
        self.thisHeaders["x-line-application"] = myApp
        self.thisHeaders["x-lal"] = "en_id"
        if splited[0] == "ANDROIDLITE":
            self.thisHeaders["user-agent"] = 'LLA/{} Mi5 {}'.format(splited[1], splited[3])
        elif splited[0] == "CHROMEOS":
            self.thisHeaders["user-agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        elif splited[0] in ["IOS", "IOSIPAD"]:
            self.thisHeaders["user-agent"] = 'Line/{} Iphone8 {}'.format(splited[1], splited[3])
        else :
            self.thisHeaders["user-agent"] = 'Line/{}'.format(splited[1])
        self.talk = self.openTransport("/S4")
        self.polling = self.openTransport("/P4")
        self.profile = self.getProfile()
        self.serverTime = self.getServerTime()
        self.localRev = -1
        self.globalRev = 0
        self.individualRev = 0
        print("[ Login ] Display Name: " + self.profile.displayName)
        print("[ Login ] Auth Token: " + myToken)

    def openTransport(self, endPoint):
        transport = THttpClient(self.lineServer + endPoint)
        transport.setCustomHeaders(self.thisHeaders)
        protocol = TCompactProtocol(transport)
        return TalkService.Client(protocol)

    def acceptChatInvitation(self, chatMid):
        return self.talk.acceptChatInvitation(AcceptChatInvitationRequest(0,chatMid))
    
    def acceptChatInvitationByTicket(self, chatMid, ticketId):
        return self.talk.acceptChatInvitationByTicket(AcceptChatInvitationByTicketRequest(0,chatMid,ticketId))

    def blockContact(self, mid):
        return self.talk.blockContact(0,mid)
    
    def cancelChatInvitation(self,chatMid, targetUserMids):
        return self.talk.cancelChatInvitation(CancelChatInvitationRequest(0,chatMid,targetUserMids))
    
    def createChat(self, name, targetUserMids, picturePath=""):
        return self.talk.createChat(CreateChatRequest(0,0,name,targetUserMids,picturePath))

    def deleteSelfFromChat(self, chatMid):
        return self.talk.deleteSelfFromChat(DeleteSelfFromChatRequest(0,chatMid,"","","",""))
                                     
    def deleteOtherFromChat(self, chatMid, targetUserMids):
        return self.talk.deleteOtherFromChat(DeleteOtherFromChatRequest(0,chatMid,targetUserMids))
    
    def fetchOperations(self, deviceId, offsetFrom):
        return self.polling.fetchOperations(FetchOperationsRequest(deviceId,offsetFrom))

    def fetchOps(self):
        return self.polling.fetchOps(self.localRev,15,self.globalRev,self.individualRev)

    def findAndAddContactsByMid(self, mid, reference=""):
        return self.talk.findAndAddContactsByMid(0,mid,0,reference)
    
    def findAndAddContactsByUserid(self, searchId, reference=""):
        return self.talk.findAndAddContactsByUserid(0,searchId,reference)
    
    def findContactByUserid(self, userid):
        return self.talk.findContactByUserid(userid)

    def findChatByTicket(self, ticketId):
        return self.talk.findChatByTicket(FindChatByTicketRequest(ticketId))

    def getAllChatMids(self, withMemberChats=True, withInvitedChats=True, syncReason=0):
        return self.talk.getAllChatMids(GetAllChatMidsRequest(withMemberChats,withInvitedChats),syncReason)

    def getProfile(self, syncReason=0):
        return self.talk.getProfile(syncReason)

    def getContact(self, mid):
        return self.talk.getContact(mid)

    def getCountryWithRequestIp(self):
        return self.talk.getCountryWithRequestIp()

    def getServerTime(self):
        return self.talk.getServerTime()

    def getContacts(self, mids):
        return self.talk.getContacts(mids)

    def getAllContactIds(self, syncReason=0):
        return self.talk.getAllContactIds(syncReason)

    def getChats(self, chatMids, withMembers=True, withInvitees=True):
        return self.talk.getChats(GetChatsRequest(chatMids,withMembers,withInvitees))

    def inviteIntoChat(self, chatMid, targetUserMids=[]):
        return  self.talk.inviteIntoChat(InviteIntoChatRequest(0,chatMid,targetUserMids))
    
    def reissueChatTicket(self, chatMid):
        return self.talk.reissueChatTicket(ReissueChatTicketRequest(0,chatMid))
    
    def rejectChatInvitation(self, chatMid):
        return self.talk.rejectChatInvitation(RejectChatInvitationRequest(0,chatMid))
    
    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        return self.talk.sendMessage(0,msg)
    
    def sendMessageReply(self, to, text, msgId):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = 0, {}
        msg.relatedMessageId = msgId
        msg.messageRelationType = 3
        msg.relatedMessageServiceCode = 1
        return self.talk.sendMessage(0,msg)
    
    def sendMention(self, to, mid, text):
        mentiones = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x  {}'.format(text)
        return self.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+mentiones+']}'}, contentType=0)

    def unsendMessage(self, messageId):
        return self.talk.unsendMessage(0,messageId)

    def updateChat(self, chat, updatedAttribute):
        return self.talk.updateChat(UpdateChatRequest(0,chat,updatedAttribute))
    
    def updateProfileAttribute(self, attr, value):
        return self.talk.updateProfileAttribute(0,attr,value)

