#! /usr/bin/python2.6
# coding: utf-8

import os
import sys
import time
import datetime
import csv

from lib import gdata, atom
import gdata.calendar
import gdata.service
from gdata.calendar.service import CalendarService

class Calendar:
    feedURI = 'http://www.google.com/calendar/feeds/%s/private/full'

    def __init__(self, uid, pwd, cal, kbn, src = 'gcal updater'):
        self.uid = uid
        self.pwd = pwd
        self.cal = cal
        self.src = src
        self.kbn = kbn
        self.uri = ''
        
        self.service = None
        self.initialized = False

    def setup(self):
        try:
            calendar_service = CalendarService()
    
            calendar_service.email = self.uid
            calendar_service.password = self.pwd
            calendar_service.source = self.src
            calendar_service.ProgrammaticLogin()

            self.service = calendar_service

            self.uri = self.feedURI % self.cal
            
            self.initialized = True
        except Exception, e:
            raise e

    def updateEntry(self, prop):
        # prop
        # - title
        # - start
        # - end
        # - where
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text = prop.title)
        #event.content = atom.Content(text = prop.content)
        event.where.append(gdata.calendar.Where(
            value_string = prop.where
            ))
        event.when.append(gdata.calendar.When(
            start_time = formatit(prop.start),
            end_time = formatit(prop.end),
            ))
        
        # 短い間隔でリクエストを出すとエラーになる場合がある
        # その場合は時間をおいてリトライ
        def retry(service, event, uri, maxtry = -1):
            ntry = 0
            while maxtry == -1 or ntry < maxtry:
                try:
                    new_event = service.InsertEvent(event, uri)
                    return
                except gdata.service.RequestError as inst: 
                    ntry += 1
                    thing = inst[0] 
                    if thing['status'] == 302: 
                        print 'http 302, wait...'
                        time.sleep(2.0) 
                        continue 
            raise Exception('max retry count exceeded.')
        retry(self.service, event, self.uri)

class Event(object):
    __slots__ = ['title', 'start', 'end', 'where']

def formatit(datetime_instance):
    return datetime_instance.strftime('%Y-%m-%dT%H:%M:%S.000+09:00')


_root = os.path.join(os.path.dirname(__file__), '..', 'master')
def read_kbn_master():
    # KBNマスタファイル読み込み
    mst_file = _root + '/kbn.csv'
    with open(mst_file) as f:
        mst = [(int(row[0]), (row[1], row[2])) for row in csv.reader(f)]
        mst = dict(mst)
        return mst

def read_registered_master():
    mst_file = _root + '/registered.csv'

    if not os.path.exists(mst_file):
        ofs = open(mst_file, 'w')
        ofs.close()
    with open(mst_file) as f:
        mst = [(int(row[0]), int(row[1])) for row in csv.reader(f)]
        mst = set(mst)
        return mst

def update_registered_master(kbn, no):
    mst_file = _root + '/registered.csv'
    with open(mst_file, 'a') as f:
        f.write('%d,%d\n' % (kbn, no))

def main():
    uid, pwd, cal = [None] * 3
    if len(sys.argv) < 4:
        f = os.path.basename(__file__)
        print >> sys.stderr, 'usage: %s uid pwd calendar-id' % f
        return

    uid, pwd, cal = sys.argv[1:]

    mst = read_kbn_master()
    reg = read_registered_master()

    calendars = {}

    # 予定を登録
    rowtype = [int, int, unicode, unicode, int, int, int, int, int]
    for row in csv.reader(sys.stdin):
        
        # csv 1行読み込み
        lst = map(lambda (f,v): f(v), zip(rowtype, row))
        kbn, no, at, mode, num_problems, num_correct, bronze, silver, gold = lst

        # 既に登録している場合は無視
        if (kbn, no) in reg:
            continue

        # カレンダーオブジェクトがない場合は作成
        if not kbn in calendars:
            calendar = Calendar(uid, pwd, cal, kbn)
            calendar.setup()
            calendars[kbn] = calendar
        calendar = calendars[kbn]

        # 予定オブジェクト作成
        event = Event()
        event.title = 'ping-t %s %d問' % (mst[kbn][0], num_problems)

        ts = time.strptime(at, '%Y/%m/%d %H:%M')[:-3]
        event.start = datetime.datetime(*ts)
        # end = start + 15 minutes
        event.end = event.start + datetime.timedelta(0,0,0,0,15)

        event.where = 'http://www.ping-t.com'

        print event.title
        print event.start

        # 予定送信
        calendar.updateEntry(event)
        
        # 登録した事をマスタファイルに登録
        update_registered_master(kbn, no)
        reg = read_registered_master()
        print kbn, no


if __name__ == '__main__':
    main()
