#!/usr/bin/python

# IMPORTS
import time
import datetime
from time import sleep
import Queue
import traceback
import sys
import os
import json
from threading import Thread, RLock, Lock, current_thread
from optparse import OptionParser
import requests
from requests.exceptions import * 
import MySQLdb
import random
import urllib
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

parser = OptionParser()
parser.add_option('-s', '--start',   dest='start',   default=1,              help='Start index for work queue.', type='int')
parser.add_option('-e', '--end',     dest='end',     default=20000000,       help='End index for work queue.',   type='int')
parser.add_option('-t', '--threads', dest='threads', default=2,              help='Number of worker threads.',   type='int')
parser.add_option('-S', '--syncfile',dest='syncfile',default="progress.json",help='File used to syncronize starting numbers.')
parser.add_option('-v', '--verbose', dest='verbose', action="store_true",    default=False, help='Display verbose output.')
parser.add_option('-H', '--host',    dest='host',    default=None,           help='Database server hostname or IP address')
parser.add_option('-P', '--port',    dest='port',    default=None,           help='Database server port')
parser.add_option('-N', '--name',    dest='name',    default=None,           help='Database name')
parser.add_option('-u', '--username',dest='username',default=None,           help='Database username')
parser.add_option('-p', '--password',dest='password',default=None,           help='Database password')
parser.add_option('-a', '--apikey',  dest='apikey',  default=None,           help='Bungie.Net API Key')
parser.add_option('-F', '--forcerestart', dest='forcerestart', action="store_true", default=False, help='Ignore sync file and force start and end numbers.')
parser.add_option('-d', '--disableproxy', dest='disableproxy', action="store_true", default=False, help='Disable proxies.')

(options, args) = parser.parse_args()

if options.host is None or options.port is None or options.username is None or options.password is None or options.apikey is None:
    parser.print_help()
    sys.exit(1)

if options.end > options.start:
    parser.print_help()
    sys.exit(1)
    

class WorkQueue:
    def __init__(self):
        self.q = Queue.Queue()
    def add(self, item):
        self.q.put(item)
    def queueMax(self):
        return self.qMax
    def get(self):
        return self.q.get()
    def empty(self):
        if self.q.empty(): return True
        else: return False
    def full(self):
        if self.q.full(): return True
        else: return False
    def size(self):
        return self.q.qsize()
    def clear(self):
        with self.q.mutex:
            self.q.queue.clear()

EntryQueue = WorkQueue()

class ProxyDistributor:
    def __init__(self, disableproxy):
        self.lock = RLock()
        self.badlist = []
        if os.path.file_exists("proxies.json"):
            with open("proxies.json", "r") as FILE:
                self.proxies = json.loads(FILE.readlines())
        else:
            if not disableproxy:
                self.sayLine("Missing Proxies list.")
                sys.exit()
        if os.path.isfile('badproxies.txt'):
            with open('badproxies.txt', 'rb') as FILE:
                LINES = FILE.readlines()
                for LINE in LINES:
                    proxy = self.snl(LINE)
                    self.sayLine("Adding Proxy [%s] to Bad Proxies List...", (proxy))
                    self.badlist.append(proxy)
        if len(self.badlist) == len(self.proxies):
            self.out("No good proxies remain. Exiting...")
            sys.exit()
    def flagbad(self, proxy):
        with self.lock:
            self.badlist.append(proxy['https'])
            with open('badproxies.txt', 'a') as FILE:
                FILE.write("%s\n" % proxy['https'])
    def isgood(self, proxy):
        with self.lock:
            if proxy['https'] in self.badlist:
                return False
            else:
                return True
    def getProxy(self):
        with self.lock:
            GoodProxy = False
            while not GoodProxy:
                proxy = random.choice(self.proxies)
                if self.isgood(proxy): GoodProxy = True
            return proxy
    def snl(self, s):
        # QUICK FUNCTION TO STRIP NEW LINE AND RETURN CHARACTERS
        s = s.rstrip('\n')
        s = s.rstrip('\r')
        return s
    def say(self, format, args=()):
        with self.lock:
            sys.stdout.write('\r                                                                                                                                                                                           \r' + format % args)
            sys.stdout.flush()
    def sayLine(self, format, args=()):
        format = '%s\n' % format
        self.say(format, args)          
    def out(self, string):
        self.say(string)
            
MyProxy = ProxyDistributor(options.disableproxy)
            
class API:
    def __init__(self, threads, start, end, verbose, disableproxy, syncfile, forcerestart, host, port, name, username, password, apikey):
        try:
            self.lock = RLock()
            self.headers = {"X-API-Key": apikey}
            self.endpoint = "https://www.bungie.net/Platform"
            self.DBUSER = username
            self.DBPASS = password
            self.DBHOST = host
            self.DBPORT = port
            self.DBNAME = name
            self.start = start
            self.end = end
            self.verbose = verbose
            self.disableproxy = disableproxy
            self.badproxies = []
            self.syncfile = syncfile
            self.forcerestart = forcerestart
            
            
            self.out("Building Queue...")
            if not self.forcerestart:
                if self.syncfile is not None and os.path.isfile(self.syncfile):
                        sync = json.load(open(self.syncfile))
                        for i in range(sync['start'], sync['end']):
                            EntryQueue.add(i)
                else:
                    if self.syncfile:
                        with open(self.syncfile, "w") as FILE:
                            sync = {"start": self.start, "end": self.end}
                            FILE.write( json.dumps(sync) )
                    for i in range(start, end):
                        EntryQueue.add(i)
            else:
                if self.syncfile:
                    with open(self.syncfile, "w") as FILE:
                        sync = {"start": self.start, "end": self.end}
                        FILE.write( json.dumps(sync) )
                for i in range(start, end):
                    EntryQueue.add(i)
            
            self.out("Starting workers...")
            Workers = [Thread(target=self.WorkerThread) for i in range(threads)]
            for Worker in Workers:
                Worker.daemon = True
                Worker.start()
            self.out( "Done." )
        except KeyboardInterrupt:
            self.exit()
        
    def getProxy(self):
        return MyProxy.getProxy()
        
    def WorkerThread(self):
        self.out( "   - New thread started." )
        while not EntryQueue.empty():
            with self.lock:
                try:
                    ID = EntryQueue.get()
                    if self.syncfile is not None and os.path.isfile(self.syncfile):
                        with open(self.syncfile, "w") as FILE:
                            sync = {"start": ID, "end": self.end}
                            FILE.write( json.dumps(sync) )
    
                    self.out("%s\tRequesting entry for membershipId %s..." % (current_thread(), ID) )
                    endpoint = "/User/GetMembershipsById/%s/-1/" % ID
                    url = "%s%s" % (self.endpoint, endpoint)
                    
                    # Initial request
                    data = False
                    count = 0
                    while not data:
                        count += 1
                        if count > 1:
                            self.out("%s\tReceived no data. Retrying..." % current_thread())
                        if count == 5:
                            break;
                        data = self.request(url)
                    #self.out(data)
                    # Skip empty responses
                    if data:
                        if len(data) < 1: 
                            if self.verbose: self.out("%s\tReceived blank data." % current_thread())
                            continue
                    else:
                        if self.verbose: self.out("%s\tReceived no data." % current_thread())
                        continue
                    if 'throttleSeconds' in data:
                        if type(data['throttleSeconds']) is int or type(data['throttleSeconds']) is float: 
                            if data['throttleSeconds'] >= 1:
                                if self.verbose: self.out("%s\tSleeping for %s seconds..." % (current_thread(), response['throttleSeconds']))
                                sleep(response['throttleSeconds'])
                                if self.verbose: self.out("%s\tRequesting new data..." % current_thread())
                                data = self.request(url)
                    #if self.verbose: print data
                    # Success
                    if 'ErrorCode' in data and data['ErrorCode'] == 1:
                        response = data['Response']
                        # Get User ID
                        userId = response['bungieNetUser']['membershipId']
                        
                        querystring = {"components": 100}
                        if 'destinyMemberships' in response:
                            for entry in response['destinyMemberships']:
                                url = "%s/Destiny2/%s/Profile/%s/" % (self.endpoint, entry['membershipType'], entry['membershipId'])
                                membership = False
                                count = 0
                                while not membership:
                                    count += 1
                                    if count > 1:
                                        self.out("%s\tReceived no membership data. Retrying..." % current_thread())
                                    if count == 5: break
                                    membership = self.request(url, querystring)
                                
                                if membership:
                                    if len(membership) < 1: 
                                        if self.verbose: self.out("%s\tReceived blank membership data." % current_thread() )
                                        continue
                                else:
                                    if self.verbose: self.out("%s\tReceived no membership data." % current_thread() )
                                    continue
                                
                                if 'throttleSeconds' in membership:
                                    if type(membership['throttleSeconds']) is int or type(membership['throttleSeconds']) is float:
                                        if membership['ThrottleSeconds'] >= 1:
                                            if self.verbose: self.out("%s\tSleeping for %s seconds..." % (current_thread(), membership['throttleSeconds']))
                                            sleep(membership['ThrottleSeconds']);
                                            if self.verbose: self.out("%s\tRequesting new membership data..." % current_thread() )
                                            membership = self.request(url, querystring)
                                
                                if 'ErrorCode' in membership and membership['ErrorCode'] == 1:
                                    timeLastPlayed = time.mktime(datetime.datetime.strptime(membership['Response']['profile']['data']['dateLastPlayed'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
                                    record = {"membershipId": userId,
                                                "destinyMembershipId": membership['Response']['profile']['data']['userInfo']['membershipId'],
                                                "membershipType": membership['Response']['profile']['data']['userInfo']['membershipType'],
                                                "dateLastPlayed": membership['Response']['profile']['data']['dateLastPlayed'],
                                                "timestampLastPlayed": int(timeLastPlayed)}
                                    
                                    update = {"dateLastPlayed": membership['Response']['profile']['data']['dateLastPlayed'],
                                                "timestampLastPlayed": int(timeLastPlayed)}
                                    self.insert("entries", record, update)      
                                else:
                                    self.out("%s\t[%s] -- %s: %s (%s)" % (current_thread(), ID, membership['ErrorCode'], membership['ErrorStatus'], membership['Message']))
                    else:
                        self.out("%s\t[%s] -- %s: %s (%s)" % (current_thread(), ID, data['ErrorCode'], data['ErrorStatus'], data['Message']))
                except KeyboardInterrupt:
                    self.exit()

    def e(self, string):
        ue = "%s" % string
        return urllib.quote_plus(ue)
                    
    def insert(self, table, insert, update):
        with self.lock:
            try: 
                db = MySQLdb.connect(host=self.DBHOST, port=self.DBPORT, user=self.DBUSER, passwd=self.DBPASS, db=self.DBNAME, autocommit=True)
                cursor = db.cursor()
                q = "INSERT INTO `%s` " % table
                k = ''
                v = ''
                for key,value in insert.iteritems():
                    k = "%s`%s`, " % (k, key)
                    v = "%s'%s', " % (v, self.e(value) )
                
                k = k.rstrip(", ")
                v = v.rstrip(", ")
                q = "%s(%s) VALUES (%s) ON DUPLICATE KEY UPDATE " % (q, k, v)
                for key,value in update.iteritems():
                    q = "%s`%s` = '%s', " % (q, key, self.e(value) )
                
                q = q.rstrip(", ")
                q = "%s;" % q
                
                
                if self.verbose: self.out("SQL STATEMENT:\n %s\n" % q) 
                self.sayLine('%s\nInserted Record:', (current_thread()))
                for key, value in insert.iteritems():
                    self.sayLine( "\t\t%s: %s", (key, self.e(value)) )
                
                cursor.execute(q)
                db.commit()
                cursor.close()  
                db.close()
            except KeyboardInterrupt:
                self.exit()         
            
    def request(self, url, querystring=None):
        try:
            if not self.disableproxy: 
                proxy = self.getProxy()
                self.out("%s\tUsing Proxy: %s" % (current_thread(), proxy['https']))
            if querystring is not None:
                if self.disableproxy:
                    r = requests.get(url, headers=self.headers, params=querystring, timeout=10)
                else:
                    r = requests.get(url, headers=self.headers, params=querystring, proxies=proxy, timeout=10)
            else:
                if self.disableproxy:
                    r = requests.get(url, headers=self.headers, timeout=10)
                else:   
                    r = requests.get(url, headers=self.headers, proxies=proxy, timeout=10)
            response = r.json()
            return response
        except ValueError:
            
            return False
        except KeyboardInterrupt:
            self.exit()
        except ProxyError:
            if not self.disableproxy: MyProxy.flagbad(proxy)
            if not self.disableproxy: self.out("%s\tProxyError: Retrying with new proxy..." % current_thread() )
            self.request(url, querystring)
        except ConnectionError:
            if not self.disableproxy: MyProxy.flagbad(proxy)
            if not self.disableproxy: self.out("%s\tConnectionError: Retrying with new proxy..." % current_thread() )
            self.request(url, querystring)
        except SSLError:
            if not self.disableproxy: MyProxy.flagbad(proxy)
            if not self.disableproxy: self.out("%s\tSSLError: Retrying with new proxy..." % current_thread() )
            self.request(url, querystring)
        except Timeout:
            if not self.disableproxy: MyProxy.flagbad(proxy)
            if not self.disableproxy: self.out("%s\tTimeout: Retrying with new proxy..." % current_thread() )
            self.request(url, querystring)
        except:
            traceback.print_exc()
            return False
    
    def say(self, format, args=()):
        sys.stdout.write('\r                                                                                                                                                                                           \r' + format % args)
        sys.stdout.flush()
    def sayLine(self, format, args=()):
        format = '%s\n' % format
        self.say(format, args)          
    def out(self, string):
        self.say(string)
    
    def Start(self):
        # ENDLESS LOOP TO ALLOW BACKGROUND THREADS
        while True:
            try:
                sleep(0.1)
            except KeyboardInterrupt:
                self.exit()
            except:
                #with self.lock:
                #   traceback.print_exc()
                self.exit()
            if EntryQueue.empty():
                print "\n\nAll threads finished."
                sys.exit()
    def exit(self):
        # JUST A CLEAN EXIT FUNCTION
        self.out( "Use the '-h' flag for command line options." )
        sys.exit()
                        
    def snl(self, s):
        # QUICK FUNCTION TO STRIP NEW LINE AND RETURN CHARACTERS
        s = s.rstrip('\n')
        s = s.rstrip('\r')
        return s

try:
    Scraper = API(options.threads, options.start, options.end, options.verbose, options.disableproxy, options.syncfile, options.forcerestart, options.host, options.port, options.name, options.username, options.password, options.apikey)
    Scraper.Start()
except KeyboardInterrupt:
    sys.exit()
except:
    traceback.print_exc()
    sys.exit()