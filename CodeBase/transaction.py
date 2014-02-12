# Enter your code here. Read input from STDIN. Print output to STDOUT
import datetime
num = int(raw_input())
trans_dic = {}
for i in range(num):
    line = raw_input()
    transaction = line.split()
    trans_date = datetime.datetime.strptime(transaction[1], '%d-%m-%Y').date()
    if trans_dic.has_key(trans_date) is False:
        trans_dic[trans_date] = 0
    if transaction[0] == "Payment":
        trans_dic[trans_date] += int(transaction[2])
    elif transaction[0] == "Refund":
        trans_dic[trans_date] -= int(transaction[2])
    else:
        print "Transaction Type Unrecognized"
for key in sorted(trans_dic.iterkeys()):
    print "%s %s" % (key.strftime("%d-%m-%Y"), trans_dic[key])
    
