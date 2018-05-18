# -*- coding: utf-8 -*-

from linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
#==============================================================================#
botStart = time.time()

cl = LINE()
#cl = LINE("TOKEN KAMU")
#cl = LINE("Email","Password")
cl.log("Auth Token : " + str(cl.authToken))
channelToken = cl.getChannelResult()
cl.log("Channel Token : " + str(channelToken))

clMID = cl.profile.mid
clProfile = cl.getProfile()
lineSettings = cl.getSettings()
oepoll = OEPoll(cl)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)


myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

msg_dict = {}
bl = [""]
myProfile["displayName"] = clProfile.displayName
myProfile["statusMessage"] = clProfile.statusMessage
myProfile["pictureStatus"] = clProfile.pictureStatus
#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def helpmessage():
    helpMessage = """╔═════════════
╠♥ ✿✿✿ 十香の特製Bot ✿✿✿ ♥
╠SR 設定已讀點
╠LR 查看誰已讀
╠Nk @ 標註踢人
╠Nk 全部再見
╠══✪〘 其他功能略 〙✪═══
"""
    return helpMessage
wait = {
    "share":False,
    "sender" :{},
}
admin =['ud5ff1dff426cf9e3030c7ac2a61512f0','ua10c2ad470b4b6e972954e1140ad1891',clMID]
owners = ["ua10c2ad470b4b6e972954e1140ad1891","ud5ff1dff426cf9e3030c7ac2a61512f0"]
#if clMID not in owners:
#    python = sys.executable
#    os.execl(python, python, *sys.argv)
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                cl.sendMessage(op.param1, "感謝您加入本帳為好友w".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = cl.getGroup(op.param1)
            if settings["autoJoin"] == True:
                cl.acceptGroupInvitation(op.param1)
        if op.type == 19:
            if op.param2 not in owners:
                if op.param2 in owners:
                    pass
                elif wait["protect"] == True:
                    settings["blacklist"][op.param2] = True
                    cl.kickoutFromGroup(op.param1,[op.param2])
                else:
                    cl.sendMessage(op.param1,"")
            else:
                cl.sendMessage(op.param1,"")
        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 25 or op.type == 26:
            K0 = admin
            msg = op.message
            if wait["share"] == True:
                K0 = msg._from
            else:
                K0 = admin
#        if op.type == 25:
#            to = msg.to
#            receiver = str(to.displayName)
#            print ("send" + receiver + str(text.lower()))
#        if op.type == 26:
#            to = msg._from
#            sender = str(to.displayName)
#            print ("receiver" + sender + str(text.lower()))
        if op.type == 26 or op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
            if sender in K0:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to,"u0a59c278b1529476ddb210cb5e827ffc")
                    cl.sendContact(to,"ufb30e2203f44bc7b72e28b09a88c9bbd")
#==============================================================================#
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.sendMessage(to, "計算中...")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    cl.sendMessage(to, "重新啟動中...")
                    time.sleep(5)
                    cl.sendMessage(to, "重啟成功，請重新登入")
                    restartBot()
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "系統已運作 {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner = "ua10c2ad470b4b6e972954e1140ad1891"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 關於使用者 ]"
                        ret_ += "\n╠ 使用者名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組數 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友數 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 已封鎖 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ 關於本bot ]"
                        ret_ += "\n╠ 版本 : 最新"
                        ret_ += "\n╠ 製作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ 感謝您的使用 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 狀態 ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ Auto Add ✅"
                        else: ret_ += "\n╠ Auto Add ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠ Auto Join ✅"
                        else: ret_ += "\n╠ Auto Join ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠ Auto Leave ✅"
                        else: ret_ += "\n╠ Auto Leave ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠ Auto Read ✅"
                        else: ret_ += "\n╠ Auto Read ❌"
                        if settings["reread"] ==True: ret_+="\n╠ Reread ✅"
                        else: ret_ += "\n╠ Reread ❌"
                        ret_ += "\n╚══[ Finish ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "Auto Add on success")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "Auto Add off success")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "Auto Join on success")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "Auto Join off success")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "Auto Leave on success")
                elif text.lower() == 'autojoin off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "Auto Leave off success")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "Auto Read on success")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "Auto Read off success")
                elif text.lower() == 'checksticker on':
                    settings["checkSticker"] = True
                    cl.sendMessage(to, "Berhasil mengaktifkan Check Details Sticker")
                elif text.lower() == 'checksticker off':
                    settings["checkSticker"] = False
                    cl.sendMessage(to, "Berhasil menonaktifkan Check Details Sticker")
                elif text.lower() == 'detectmention on':
                    settings["datectMention"] = True
                    cl.sendMessage(to, "Berhasil mengaktifkan Detect Mention")
                elif text.lower() == 'detectmention off':
                    settings["datectMention"] = False
                    cl.sendMessage(to, "Berhasil menonaktifkan Detect Mention")
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to,"reread on success")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to,"reread off success")
                elif text.lower() == 'protect on':
                    settings["protect"] = True
                    cl.sendMessage(to, "Protect on success")
                elif text.lower() == 'protect off':
                    settings["protect"] = False
                    cl.sendMessage(to, "Protect off success")
                elif text.lower() == 'share on':
                    wait["share"] = True
                    cl.sendMessage(to, "已開啟分享")
                elif text.lower() == 'share off':
                    wait["share"] = False
                    cl.sendMessage(to, "已關閉分享")
#==============================================================================#
                elif text.lower() == 'admin ':
                    MENTION =eval(msg.contentMetadata['MENTION'])
                    inkey =MENTION['MENTIONEES'][0]['M']
                    admin.append(str(inkey))
                    cl.sendMessage(to,"已新增權限")
                elif text.lower() == 'demin ':
                    MENTION =eval(msg.contentMetadata['MENTION'])
                    inkey =MENTION['MENTIONEES'][0]['M']
                    admin.remove(str(inkey))
                    cl.sendMessage(to,"已停止權限")
                elif text.lower() == 'adminlist':
                    if admin == []:
                        cl.sendMessage(to,"無擁有權限者!")
                    else:
                        mc = "╔══[ Admin List ]"
                        for mi_d in admin:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")



#==============================================================================#
                elif text.lower() == 'me':
                    sendMessageWithMention(to, clMID)
                    cl.sendContact(to, clMID)
                elif text.lower() == 'mymid':
                    cl.sendMessage(msg.to,"[MID]\n" +  clMID)
                elif text.lower() == 'myname':
                    me = cl.getContact(clMID)
                    cl.sendMessage(msg.to,"[Name]\n" + me.displayName)
                elif text.lower() == 'mytoken':
                    me = cl.getContact(clMID)
                    cl.sendMessage(msg.to,"[StatusMessage]\n" + me.statusMessage)
                elif text.lower() == 'mypicture':
                    me = cl.getContact(clMID)
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideoprofile':
                    me = cl.getContact(clMID)
                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = cl.getContact(clMID)
                    cover = cl.getProfileCoverURL(clMID)
                    cl.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("contact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("name "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 名字 ]\n" + contact.displayName)
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 個簽 ]\n" + contact.statusMessage)
                        for ls in lists:
                            path = "http://dl.profile.cl.naver.jp/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, str(path))
                        for ls in lists:
                            path = cl.getProfileCoverURL(ls)
                            pmath = "http://dl.profile.cl.naver.jp/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, path)
                    try:
                            key = eval(msg.contentMetadata["MENTION"])
                            u = key["MENTIONEES"][0]["M"]
                            cname = cl.getContact(u).displayName
                            cmid = cl.getContact(u).mid
                            cstatus = cl.getContact(u).statusMessage
                            cpic = cl.getContact(u).picturePath
                            cl.sendMessage(receiver, 'Nama : '+cname+'\nMID : '+cmid+'\nStatus Msg : '+cstatus+'\nPicture : http://dl.profile.line.naver.jp'+cpic)
                            cl.sendMessage(receiver, None, contentMetadata={'mid': cmid}, contentType=13)
                            if cl.getContact(u).videoProfile != None:
                                cl.sendVideoWithURL(receiver, 'http://dl.profile.line.naver.jp'+cpic+'/vp.small')
                            else:
                                cl.sendImageWithURL(receiver, 'http://dl.profile.line.naver.jp'+cpic)
                    except Exception as e:
                            cl.sendMessage(receiver, str(e))


                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = cl.getProfileCoverURL(ls)
                                cl.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cloneprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            cl.cloneContactProfile(contact)
                            cl.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                        except:
                            cl.sendMessage(msg.to, "Gagal clone member")
                elif text.lower() == 'restoreprofile':
                    try:
                        clProfile.displayName = str(myProfile["displayName"])
                        clProfile.statusMessage = str(myProfile["statusMessage"])
                        clProfile.pictureStatus = str(myProfile["pictureStatus"])
                        cl.updateProfileAttribute(8, clProfile.pictureStatus)
                        cl.updateProfile(clProfile)
                        cl.sendMessage(msg.to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                    except:
                        cl.sendMessage(msg.to, "Gagal restore profile")
#==============================================================================#
                elif msg.text.lower().startswith("mimicadd "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            cl.sendMessage(msg.to,"已加入模仿名單!")
                            break
                        except:
                            cl.sendMessage(msg.to,"添加失敗 !")
                            break
                elif msg.text.lower().startswith("mimicdel "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["模仿名單"]["target"][target]
                            cl.sendMessage(msg.to,"刪除成功 !")
                            break
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                            break
                elif text.lower() == 'mimiclist':
                    if settings["mimic"]["target"] == {}:
                        cl.sendMessage(msg.to,"未設定模仿目標")
                    else:
                        mc = "╔══[ Mimic List ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                elif "mimic" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            cl.sendMessage(msg.to,"Reply Message on")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            cl.sendMessage(msg.to,"Reply Message off")
#==============================================================================#
                elif text.lower() == 'groupcreator':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'groupid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[ID Group : ]\n" + gid.id)
                elif text.lower() == 'grouppicture':
                    group = cl.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'groupname':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[群組名稱 : ]\n" + gid.name)
                elif text.lower() == 'grouplink':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to, "[ Group Ticket ]\nhttps://cl.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            cl.sendMessage(to, "Grouplink未開啟 {}openlink".format(str(settings["keyCommand"])))
                elif text.lower() == 'link off':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendMessage(to, "群組網址已關")
                        else:
                            group.preventedJoinByTicket = False
                            cl.updateGroup(group)
                            cl.sendMessage(to, "關閉成功")
                elif text.lower() == 'link on':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendMessage(to, "群組網址已開")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendMessage(to, "開啟成功")
                elif text.lower() == 'groupinfo':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "無"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ Group Info ]"
                    ret_ += "\n╠ 群組名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組 Id : {}".format(group.id)
                    ret_ += "\n╠ 創建者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 群組人數 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請中 : {}".format(gPending)
                    ret_ += "\n╠ 網址狀態 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ Finish ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'groupmemberlist':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員名單 ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'grouplist':
                        groups = cl.groups
                        ret_ = "╔══[ Group List ]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ Total {} Groups ]".format(str(len(groups)))
                        cl.sendMessage(to, str(ret_))
                elif msg.text.lower().startswith("nk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"Fuck you")
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif msg.text.lower().startswith("ri "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"來回機票一張ww")
                            cl.kickoutFromGroup(msg.to,[target])
                            cl.inviteIntoGroup(to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif text.lower() == 'nk':
                    if msg.toType == 2:
                        print ("[ 19 ] KICK ALL MEMBER")
                        _name = msg.text.replace("Byeall","")
                        gs = cl.getGroup(msg.to)
                        cl.sendMessage(msg.to,"Sorry guys")
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"Not Found")
                        else:
                            for target in targets:
                                try:
                                    cl.kickoutFromGroup(msg.to,[target])
                                    print (msg.to,[g.mid])
                                except:
                                    cl.sendMessage(msg.to,"")
                elif ("Gn " in msg.text):
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        X.name = msg.text.replace("Gn ","")
                        cl.updateGroup(X)
                    else:
                        cl.sendMessage(msg.to,"It can't be used besides the group.")
                elif text.lower() == 'cancel':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[_mid])
                    cl.sendMessage(msg.to,"已取消所有邀請!")
                elif ("Inv " in msg.text):
                    if msg.toType == 2:
                        midd = msg.text.replace("Inv ","")
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoGroup(to,[midd])
#==============================================================================#
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "Total {} Mention".format(str(len(nama))))
                elif text.lower() == 'sr':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                cl.sendMessage(msg.to,"偵測點已設置")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            cl.sendMessage(msg.to, "Set reading point:\n" + readTime)
                elif text.lower() == 'readcancel':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        cl.sendMessage(msg.to,"偵測點已取消")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        cl.sendMessage(msg.to, "Delete reading point:\n" + readTime)
                elif text.lower() == 'resetread':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        cl.sendMessage(msg.to, "Reset reading point:\n" + readTime)
                    else:
                        cl.sendMessage(msg.to, "偵測點未設置?")
                elif text.lower() == 'lr':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            cl.sendMessage(receiver,"[ 已讀的人 ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = cl.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ 已讀的人 ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ 已讀時間 ]: \n" + readTime
                        try:
                            cl.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        cl.sendMessage(receiver,"尚未設置偵測點")
#==============================================================================#
                elif msg.text.lower().startswith("ban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["blacklist"][target] = True
                            cl.sendMessage(msg.to,"已加入黑單!")
                            break
                        except:
                            cl.sendMessage(msg.to,"添加失敗 !")
                            break
                elif msg.text.lower().startswith("unban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["blacklist"][target]
                            cl.sendMessage(msg.to,"刪除成功 !")
                            break
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                            break
                elif text.lower() == 'banlist':
                    if settings["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in settings["blacklist"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'nkban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in settings["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendMessage(msg.to,"Blacklist kicked out")
                elif text.lower() == 'cleanban':
                    settings["blacklist"] == {ok}
                    for mi_d in settings["blacklist"]:
                        try:
                            del settings["blacklist"][mi_d]
                            cl.sendMessage(msg.to,"已清空黑單!")
                            break
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                            break
                elif text.lower() == 'banmidlist':
                    if settings["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "╔══[ Black List ]"
                        for mi_d in settings["blacklist"]:
                            mc += "\n╠ "+mi_d
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")


#==============================================================================#
                elif "Copy " in msg.text:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            contact = cl.getContact(target)
                            X = contact.displayName
                            profile = cl.getProfile()
                            profile.displayName = X
                            cl.updateProfile(profile)
                            cl.sendMessage(to, "Success...")
                            Y = contact.statusMessage
                            lol = cl.getProfile()
                            lol.statusMessage = Y
                            cl.updateProfile(lol)
                            P = contact.pictureStatus
                            pic = cl.getProfile()
                            pic.pictureStatus = P
                            cl.updateProfilePicture(P)
                            cl.cloneContactProfile(target)
                        except Exception as e:
                            cl.sendMessage(to, "Failed!")
                elif text.lower() == 'cc9487':
                    if sender in ['ua10c2ad470b4b6e972954e1140ad1891']:
                        python = sys.executable
                        os.execl(python, python, *sys.argv)
                    else:
                        pass
#==============================================================================#
                elif text.lower() == 'calender':
                    tz = pytz.timezone("Asia/Makassar")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    cl.sendMessage(msg.to, readTime)
                elif "screenshotwebsite" in msg.text.lower():
                    sep = text.split(" ")
                    query = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        r = web.get("http://rahandiapi.herokuapp.com/sswebAPI?key=betakey&link={}".format(urllib.parse.quote(query)))
                        data = r.text
                        data = json.loads(data)
                        cl.sendImageWithURL(to, data["result"])
                elif "checkdate" in msg.text.lower():
                    sep = msg.text.split(" ")
                    tanggal = msg.text.replace(sep[0] + " ","")
                    r=requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                    data=r.text
                    data=json.loads(data)
                    ret_ = "╔══[ D A T E ]"
                    ret_ += "\n╠ Date Of Birth : {}".format(str(data["data"]["lahir"]))
                    ret_ += "\n╠ Age : {}".format(str(data["data"]["usia"]))
                    ret_ += "\n╠ Birthday : {}".format(str(data["data"]["ultah"]))
                    ret_ += "\n╠ Zodiak : {}".format(str(data["data"]["zodiak"]))
                    ret_ += "\n╚══[ Success ]"
                    cl.sendMessage(to, str(ret_))
            elif msg.contentType == 7:
                if settings["checkSticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = "╔══[ Sticker Info ]"
                    ret_ += "\n╠ STICKER ID : {}".format(stk_id)
                    ret_ += "\n╠ STICKER PACKAGES ID : {}".format(pkg_id)
                    ret_ += "\n╠ STICKER VERSION : {}".format(stk_ver)
                    ret_ += "\n╠ STICKER URL : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n╚══[ Finish ]"
                    cl.sendMessage(to, str(ret_))
            elif msg.contentType == 13:
                if settings["copy"] == True:
                    _name = msg.contentMetadata["displayName"]
                    copy = msg.contentMetadata["mid"]
                    groups = cl.getGroup(msg.to)
                    targets = []
                    for s in groups.members:
                        if _name in s.displayName:
                            print ("[Target] Copy")
                            break
                        else:
                            targets.append(copy)
                    if targets == []:
                        cl.sendMessage(msg.to, "Not Found...")
                        pass
                    else:
                        for target in targets:
                            try:
                                cl.cloneContactProfile(target)
                                cl.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                                settings['copy'] = False
                                break
                            except:
                                msg.contentMetadata = {'mid': target}
                                settings["copy"] = False
                                break
#==============================================================================#
        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        cl.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = cl.getContact(sender)
                                    cl.sendMessage(to, "sundala nu")
                                    sendMessageWithMention(to, contact.mid)
                                break
#==============================================================================#
        if op.type == 65:
            print ("[ 65 ] REREAD")
            try:
                at = op.param1
                msg_id = op.param2
                if setting["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
