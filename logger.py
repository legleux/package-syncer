import logging

#logname = f"tester.py-" + datetime.datetime.now().strftime("%m-%d-%Y") + ".log"
# logname = f"account_tester-" + datetime.datetime.now().strftime("%m-%d-%Y")[:-3] +".log"
# logging.basicConfig(filename=logname,
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
                    # level=logging.INFO)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

log = logging
