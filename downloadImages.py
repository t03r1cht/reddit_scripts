import optparse
import praw
import os
import errno
import sys
import urllib
from time import gmtime, strftime, sleep

def main():
    parser = optparse.OptionParser("usage %prog -s <subreddit> -c <count from hot> -t <category>")
    parser.add_option("-s", dest="sr_name", type="string", help="specify subreddit name")
    parser.add_option("-c", dest="thread_count", type="int", help="specify thread number count")
    parser.add_option("-t", dest="category", type="string", help="specify if hot or top")
    (options, args) = parser.parse_args()

    sr_name = options.sr_name
    thread_count = options.thread_count
    category = options.category

    if sr_name == None or thread_count == None:
        print(parser.usage)
        exit(0)

    reddit = praw.Reddit(client_id = "H4Nsf1IEsxnZpg",
                         client_secret = "n3ZHFPK_wkk6PzyAGC-OTuPJ6B4",
                         username = "hoaks01",
                         password = "marc6913",
                         user_agent="imagedownloaderv1")

    subr = reddit.subreddit(sr_name)

    '''
        setup folder etc.
    '''

    allowed_formats = ["jpg", "jpeg", "png", "gif", "webm"]
    dir_name = str(strftime("%H.%M.%S", gmtime())) + "_" + sr_name + "_"
    if not category == None:
        if category == "time":
            dir_name += "time"
        elif category == "year":
            dir_name += "year"
        else:
            log("invalid category. specify either 'time' for all time or 'year' for all year")
            sys.exit(0)
    else:
        dir_name += "hot"

    try:
        os.makedirs(dir_name)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
            pass
        else:
            raise
    os.chdir(dir_name)
    log("files will be saved in '" + dir_name + "'")
    img_urls = []


    if not category == None:
        if category == "time":
            sub_python = subr.top(time_filter= "all", limit=thread_count)
            log("subreddit: " + subr.display_name)

            for submission in sub_python:
                if not submission.stickied:
                    subm_url = submission.url
                    url_spli = subm_url.split(".")
                    if url_spli[-1] in allowed_formats:
                        try:
                            urllib.request.urlretrieve(subm_url, subm_url.split("/")[-1])
                        except:
                            log("error while downloading '" + subm_url + "'")
                        log("downloading '" + subm_url + "'")
                    else:
                        log("failed to download '" + subm_url + "'")
        elif category == "year":
            sub_python = subr.top(time_filter= "year", limit=thread_count)
            log("subreddit: " + subr.display_name)

            for submission in sub_python:
                if not submission.stickied:
                    subm_url = submission.url
                    url_spli = subm_url.split(".")
                    if url_spli[-1] in allowed_formats:
                        try:
                            urllib.request.urlretrieve(subm_url, subm_url.split("/")[-1])
                        except:
                            log("error while downloading '" + subm_url + "'")
                        log("downloading '" + subm_url + "'")
                    else:
                        log("failed to download '" + subm_url + "'")


    else: # if -c was not specifiy, default to hot search
        sub_python = subr.hot(limit=thread_count)
        log("subreddit: " + subr.display_name)

        for submission in sub_python:
            if not submission.stickied:
                subm_url = submission.url
                url_spli = subm_url.split(".")
                if url_spli[-1] in allowed_formats:
                    try:
                        urllib.request.urlretrieve(subm_url, subm_url.split("/")[-1])
                    except:
                        log("error while downloading '" + subm_url + "'")
                    log("downloading '" + subm_url + "'")
                else:
                    log("failed to download '" + subm_url + "'")




def log(msg):
    print("[" + str(strftime("%H:%M:%S", gmtime())) + "]" + " " + msg)

if __name__ == '__main__':
    main()