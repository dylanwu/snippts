import poplib
import getopt
import time
import sys

def usage():
    print >>sys.stderr, '''
Usage: %s -s server_str -u user_str -p passwd_str
Parameters:
    -s, --server  server_str      The server url of  pop server
    -u, --user    user_str        The user name  of pop server
    -p, --passwd  passwd_str      The passwd of user name in pop server
    -h, --help                    Show this message
    ''' %(sys.argv[0])

def get_opts():
    server = 'mail.avazuholding.cn'
    user   = None
    passwd = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:u:p:h", ["help", "server=", "user=", "passwd="]);
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage();
                sys.exit(0);
            elif opt in ("-s", "--server"):
                server              = arg;
            elif opt in ("-u", "--user"):
                user                = arg;
            elif opt in ("-p", "--passwd"):
                passwd              = arg;
            else:
                usage();
                sys.exit(1)
    except getopt.GetoptError, e:
        print >>sys.stderr, "getopt error!" + str(e)
        usage();
        sys.exit(1)
    if not server or not user or not passwd:
        usage()
        sys.exit(1)
    return (server, user, passwd)

def main():
    server, user, passwd = get_opts()
    loop_status = True
    loop_index = 1
    while loop_status:
        pop_server = poplib.POP3(server)
        pop_server.user(user)
        pop_server.pass_(passwd)
        total_num, total_size = pop_server.stat()
        print >>sys.stderr, "Begin " + str(loop_index) + " Loop Processing, Total No. = "+str(total_num)+";Total Size = " + str(total_size)
        if total_num < 1000:
            loop_status = False
        for i in range(min(total_num, 1000)):
            pop_server.dele(i+1)
            if i > 0 and i % 100 == 0:
                print >>sys.stderr, "Finish " + str(i)
        total_num, total_size = pop_server.stat()
        print >>sys.stderr, "After " + str(loop_index) + " Loop Processing, Total No. = "+str(total_num)+";Total Size = " + str(total_size)
        pop_server.quit()
        time.sleep(10)
        loop_index += 1
    print("Finish")

if __name__ == '__main__':
    main()
