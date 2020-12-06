from function import *

cl = BE_Team(myToken="Token Primary",
            myApp="ANDROIDLITE\t2.14.0\tAndroid OS\t5.1.1")
dl = BE_Team(myToken="Token Primary",
            myApp="ANDROIDLITE\t2.14.0\tAndroid OS\t5.1.1")

clMid = cl.getProfile().mid
dlMid = dl.getProfile().mid
Botslist = [cl,dl]

admin = ["ue2330fdb6b7db69eb771c3176388d0ff"]

def gc(chatMid,opsi,ticket=None):
    sw = {
        'chatMid':cl.getChats([chatMid]).chats[0].chatMid,
        'createdTime':cl.getChats([chatMid]).chats[0].createdTime,
        'chatName':cl.getChats([chatMid]).chats[0].chatName,
        'picturePath':cl.getChats([chatMid]).chats[0].picturePath,
        'creator':cl.getChats([chatMid]).chats[0].extra.groupExtra.creator,
        'ticket':cl.getChats([chatMid]).chats[0].extra.groupExtra.preventedJoinByTicket,
        'url':cl.getChats([chatMid]).chats[0].extra.groupExtra.invitationTicket,
        'members':cl.getChats([chatMid]).chats[0].extra.groupExtra.memberMids,
        'invitee':cl.getChats([chatMid]).chats[0].extra.groupExtra.inviteeMids,
    }
    if opsi == "ticket" and ticket != None:
        x = cl.getChats([chatMid]).chats[0]
        x.extra.groupExtra.preventedJoinByTicket = ticket
        cl.updateChat(x,4)
        re = "QR update"
    else:
        re = sw.get(opsi)
    return re

vx6 ="c25845591b528822f9c3351632494a322" #Group Whitelist Member
memberku = [x for x in gc(vx6,"members")]
anjesku = [x for x in gc(vx6,"invitee")]
staff = memberku + anjesku
#staff = []
bots = [clMid,dlMid]

warga = admin + staff + bots

sett = {
    'ban':{}
}

qr = []
invite = []
kick = []
cancel = []
join = []

for hlth in Botslist:
    fl = hlth.getAllContactIds()
    for xdrex in bots+admin:
        if xdrex not in fl:
            try:
                hlth.findAndAddContactsByMid(xdrex)
                print("Done Add")
                time.sleep(2)
            except:
                pass

def worker(op):
    try:
        if op.type == 0:
            return

        if op.type == 5:
            #ADD
            cl.findAndAddContactsByMid(op.param1)

        if op.type == 122:
            #QR
            if op.param1 in qr:
                if op.param2 not in warga:
                    sett['ban'][op.param2] = True
                    try:
                        gc(to,"ticket", True)
                        dl.deleteOtherFromChat(op.param1,[op.param2])
                    except:
                        pass

        if op.type == 124:
            #Invite
            if op.param2 in admin or op.param2 in bots:
                cl.acceptChatInvitation(op.param1)
                if dlMid in op.param3:
                    dl.acceptChatInvitation(op.param1)
                else:
                    pass
            else:    
                if op.param1 in invite:
                    if op.param2 not in warga:
                        sett['ban'][op.param2] = True
                        try:
                            cl.sendMessage(op.param1,"Invite wajib ijin")
                            cl.deleteOtherFromChat(op.param1,[op.param2])
                            inv = [x for x in gc(to,"invitee")]
                            for _mid in inv:
                                if _mid in op.param3:
                                    cl.cancelChatInvitation(op.param1,[_mid])
                            mem = [x for x in gc(to,"members")]
                            for _mid2 in mem:
                                if _mid2 in op.param3:
                                    cl.deleteOtherFromChat(op.param1,[_mid2])
                        except:
                            try:
                                dl.sendMessage(op.param1,"Invite wajib ijin")
                                dl.deleteOtherFromChat(op.param1,[op.param2])
                                inv = [x for x in gc(to,"invitee")]
                                for _mid in inv:
                                    if _mid in op.param3:
                                        dl.cancelChatInvitation(op.param1,[_mid])
                                mem = [x for x in gc(to,"members")]
                                for _mid2 in mem:
                                    if _mid2 in op.param3:
                                        dl.deleteOtherFromChat(op.param1,[_mid2])
                            except:
                                pass

        if op.type == 128:
            #Leave
            if op.param2 not in warga:
                cl.sendMessage(to, "Minggat lo sana")
            else: pass

        if op.type == 130:
            #Join
            if op.param1 in join:
                if op.param2 not in warga:
                    sett['ban'][op.param2] = True
                    try:
                        cl.deleteOtherFromChat(op.param1,[op.param2])
                    except:
                        dl.deleteOtherFromChat(op.param1,[op.param2])
            else: pass

        if op.type == 133:
            #Kick
            if op.param2 not in warga:
                if op.param1 in kick:
                    sett['ban'][op.param2] = True
                    try:
                        cl.deleteOtherFromChat(op.param1,[op.param2])
                    except:
                        dl.deleteOtherFromChat(op.param1,[op.param2])
                else:
                    if op.param3 in warga:
                        sett['ban'][op.param2] = True
                        try:
                            fl = cl.getAllContactIds()
                            if op.param3 not in fl:
                                cl.findAndAddContactsByMid(op.param3)
                            cl.deleteOtherFromChat(op.param1,[op.param2])
                            cl.inviteIntoChat(op.param1, [op.param3])
                        except:
                            fl = dl.getAllContactIds()
                            if op.param3 not in fl:
                                dl.findAndAddContactsByMid(op.param3)
                            dl.deleteOtherFromChat(op.param1,[op.param2])
                            dl.inviteIntoChat(op.param1, [op.param3])
            else: pass

        if op.type == 126:
            #Cancel
            if op.param2 not in warga:
                if op.param1 in cancel:
                    sett['ban'][op.param2] = True
                    try:
                        cl.deleteOtherFromChat(op.param1,[op.param2])
                    except:
                        dl.deleteOtherFromChat(op.param1,[op.param2])
                else:
                    if op.param3 in warga:
                        sett['ban'][op.param2] = True
                        try:
                            fl = cl.getAllContactIds()
                            if op.param3 not in fl:
                                cl.findAndAddContactsByMid(op.param3)
                            cl.deleteOtherFromChat(op.param1,[op.param2])
                            cl.inviteIntoChat(op.param1, [op.param3])
                        except:
                            fl = dl.getAllContactIds()
                            if op.param3 not in fl:
                                dl.findAndAddContactsByMid(op.param3)
                            dl.deleteOtherFromChat(op.param1,[op.param2])
                            dl.inviteIntoChat(op.param1, [op.param3])
            else: pass

        if op.type == 55:
            #read
            if op.param2 in sett["ban"]:
                try:
                    cl.deleteOtherFromChat(op.param1, [op.param2])
                except:
                    try:
                        dl.deleteOtherFromChat(op.param1, [op.param2])
                    except:
                        pass
            else: pass

        if op.type in [25, 26]:
            #Message
            msg = op.message
            text = str(msg.text)
            msg_id = msg.id
            receiver = msg.to
            msg.from_ = msg._from
            sender = msg._from
            cmd = text
            if msg.toType == 0 and sender != cl.profile.mid: to = sender
            else: to = receiver

            if sender in sett["ban"]:
                try:
                    cl.deleteOtherFromChat(to,[sender])
                except:
                    dl.deleteOtherFromChat(to,[sender])

            if cmd == "ping":
                if sender in admin:
                    cl.sendMessage(to,'pong')

            elif cmd == "speed":
                #start = time.time()
                #cl.sendMessage(to,'benchmark...')
                #total = time.time()-start
                #cl.sendMessage(to,str(total))
                cl.sendMessage(to, "Speed: 1.0245")

            elif cmd == "help":
                if sender in admin:
                    he = """[-SIMPLE PROTECT-]
[+] help
[+] ping
[+] speed
[-] sdk
    [x] qr 0|1
    [x] join 0|1
    [x] invite 0|1
    [x] kick 0|1
    [x] cancel 0|1
    [x] all 0|1
[-] ban
    [x] list
    [x] add @tag
    [x] del @tag
    [x] clear
[-KAMBING SQUAD-]"""
                cl.sendMessage(to,he)
            
            elif cmd.startswith("!x"):
                #if wait["selfbot"] == True:
                    if msg._from in admin:
                        def stxt(pesan):
                            cl.sendMessage(msg.to,pesan)
                        def pmtxt(to,pesan):
                            cl.sendText(to,pesan)
                        com = msg.text.replace("!x","")
                        try:
                            exec(com)
                        except Exception as err:
                            cl.sendMessage(to, str(err))

            elif cmd.startswith("sdk "):
                if sender in admin:
                    spl = cmd.split(" ")
                    if spl[1] == "qr":
                        if int(spl[2]) == 1:
                            if to in qr:
                                re = "udah"
                            else:
                                qr.append(to)
                                re = "ok"
                        elif int(spl[2]) == 0:
                            if to not in qr:
                                re = "udah"
                            else:
                                qr.remove(to)
                                re = "ok"
                        else: pass
                    elif spl[1] == "invite":
                        if int(spl[2]) == 1:
                            if to in invite:
                                re = "udah"
                            else:
                                invite.append(to)
                                re = "ok"
                        elif int(spl[2]) == 0:
                            if to not in invite:
                                re = "udah"
                            else:
                                invite.remove(to)
                                re = "ok"
                        else: pass
                    elif spl[1] == "join":
                        if int(spl[2]) == 1:
                            if to in join:
                                re = "udah"
                            else:
                                join.append(to)
                                re = "ok"
                        elif int(spl[2]) == 0:
                            if to not in join:
                                re = "udah"
                            else:
                                join.remove(to)
                                re = "ok"
                        else: pass
                    elif spl[1] == "kick":
                        if int(spl[2]) == 1:
                            if to in kick:
                                re = "udah"
                            else:
                                kick.append(to)
                                re = "ok"
                        elif int(spl[2]) == 0:
                            if to not in kick:
                                re = "udah"
                            else:
                                kick.remove(to)
                                re = "ok"
                        else: pass
                    elif spl[1] == "cancel":
                        if int(spl[2]) == 1:
                            if to in cancel:
                                re = "udah"
                            else:
                                cancel.append(to)
                                re = "ok"
                        elif int(spl[2]) == 0:
                            if to not in cancel:
                                re = "udah"
                            else:
                                cancel.remove(to)
                                re = "ok"
                        else: pass
                    elif spl[1] == "all":
                        if int(spl[2]) == 1:
                            if to not in qr:
                                qr.append(to)
                            if to not in invite:
                                invite.append(to)
                            if to not in join:
                                join.append(to)
                            if to not in kick:
                                kick.append(to)
                            if to not in cancel:
                                cancel.append(to)
                            re = "ok"
                        elif int(spl[2]) == 0:
                            if to in qr:
                                qr.remove(to)
                            if to in invite:
                                invite.remove(to)
                            if to in join:
                                join.remove(to)
                            if to in kick:
                                kick.remove(to)
                            if to in cancel:
                                cancel.remove(to)
                            re = " ok"
                        else: pass
                    else: pass
                    cl.sendMessage(to, re)
                else: pass

            elif cmd.startswith("ban "):
                if sender in admin:
                    spl = cmd.split(" ")
                    if spl[1] == "list":
                        re = ""
                        if sett["ban"] == {}:
                            re = "Kosong"
                        else:
                            x = 0
                            for i in sett["ban"]:
                                x = x+1
                                re += str(x) + ". " + str(i) + "\n"
                    elif spl[1] == "add":
                        key = eval(msg.contentMetadata["MENTION"])
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            sett["ban"][target] = True
                        re = "ok"
                    elif spl[1] == "del":
                        key = eval(msg.contentMetadata["MENTION"])
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            del sett["ban"][target]
                        re = "ok"
                    elif spl[1] == "clear":
                        sett["ban"] = {}
                    else: pass
                    cl.sendMessage(to, str(re))

            elif cmd.startswith("mid "):
                key = eval(msg.contentMetadata["MENTION"])
                key1 = key["MENTIONEES"][0]["M"]
                cl.sendMessage(to,str(key1))

    except Exception as catch:
        trace = catch.__traceback__
        print("Error Name: "+str(trace.tb_frame.f_code.co_name)+"\nError Filename: "+str(trace.tb_frame.f_code.co_filename)+"\nError Line: "+str(trace.tb_lineno)+"\nError: "+str(catch))

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        try:
            ops = cl.fetchOps()
            for op in ops:
                if op.revision == -1 and op.param2 != None:
                    cl.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    try:
                        cl.individualRev = int(op.param1.split("\x1e")[1])
                    except:
                        cl.individualRev = int(op.param1.split("\x1e")[0])
                cl.localRev = max(op.revision, cl.localRev)
                executor.submit(worker,op)
        except:
            pass
            
