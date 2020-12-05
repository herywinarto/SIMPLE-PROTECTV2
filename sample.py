from function import *


cl = BE_Team(myToken="ucbfdc04ee82a01c534eeb5475ecaa984:aWF0OiAxNjA2ODQ2NTkwODM5Cg==..pYlS2EYYLeLJ4ZQlH5/nATzSGYs=",
            myApp="ANDROIDLITE\t2.14.0\tAndroid OS\t5.1.1")


def worker(op):
    try:
        if op.type in [25, 26]:
            msg = op.message
            text = str(msg.text)
            msg_id = msg.id
            receiver = msg.to
            msg.from_ = msg._from
            sender = msg._from
            cmd = text.lower()
            if msg.toType == 0 and sender != cl.profile.mid: to = sender
            else: to = receiver

            if cmd == "ping":
                cl.sendMessage(to,'pong')

            if cmd == "speed":
                start = time.time()
                cl.sendMessage(to,'benchmark...')
                total = time.time()-start
                cl.sendMessage(to,str(total))

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
                    cl.individualRev = int(op.param1.split("\x1e")[0])
                cl.localRev = max(op.revision, cl.localRev)
                executor.submit(worker,op)
        except:
            pass
            
