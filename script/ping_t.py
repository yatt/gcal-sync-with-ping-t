#! /usr/bin/python2.7
# coding: utf-8
import os
import sys
from lib import mechanize, BeautifulSoup
import datetime

def normalize_timestamp(text):
    # format as yyyy/mm/dd hh:mi
    y = datetime.datetime.now().year
    d = text[:5]
    t = text[-5:]
    return '%d/%s %s' % (y, d, t)

def datafilter(content, kbn):
    # filter history data from html doc
    content = content.encode('utf-8')
    soup = BeautifulSoup.BeautifulSoup(content)
    hist = soup.find('table', {'id': 'tablerireki'})
    hent = hist.findAll('tr', {'class': 'list_table'})
    lst = []
    for ent in hent:
        rec = ent.findAll('td')
        #   No. 出題日時    モード  正答率  出題数  正答数  銅  銀  金
        #lst.append({
        #    'no': int(rec[1].text)
        #    , 'at': normalize_timestamp(rec[2].text)
        #    , 'mode': rec[3].text
        #    , 'num_problems': int(rec[5].text)
        #    , 'num_correct_answers': int(rec[6].text)
        #    , 'rate_bronze': int(rec[7].text[:-1])
        #    , 'rate_silver': int(rec[8].text[:-1])
        #    , 'rate_gold': int(rec[9].text[:-1])

        #    , 'kbn': kbn
        #})
        lst.append([
            str(kbn)
            , rec[1].text
            , normalize_timestamp(rec[2].text)
            , rec[3].text
            , rec[5].text
            , rec[6].text
            , rec[7].text[:-1]
            , rec[8].text[:-1]
            , rec[9].text[:-1]
        ])
    return lst

def fetch_raw(uid, pwd, kbn):
    #return open('out.html').read()
    # fetch history data as raw data (html content) using mechanize
    b = mechanize.Browser()
    b.set_handle_robots(False)

    # login
    b.open('http://ping-t.com/')
    b.select_form(nr=0)
    b['uname'] = uid
    b['pass'] = pwd
    res = b.submit()

    url = {
        # ccna
        8: 'http://ping-t.com/modules/mondai/index.php?content_id=8',
        # ccnp
        # lpic 101
        22: 'http://ping-t.com/modules/mondai/index.php?content_id=22',
        # lpic 102
        40: 'http://ping-t.com/modules/PremiumContents/index.php?content_id=40',
        # lpic 201
        # lpic 202
    }[kbn]
    b.open(url)

    # goto kbn top page
    b.select_form(name='wlogin')
    b.submit()

    # goto history
    res = b.open('http://ping-t.com/mondai3/study_histories/index_noflash')

    res = res.read()
    res = res.decode('utf-8')
    return res

def fetch(uid, pwd, kbn):
    content = fetch_raw(uid, pwd, kbn)
    return datafilter(content, kbn)



def main():
    if len(sys.argv) < 4:
        f = os.path.basename(__file__)
        print >> sys.stderr, 'usage: %s uid pwd kbn' % f
        return
    uid,pwd,kbn = sys.argv[1:]
    kbn = int(kbn)
    for e in fetch(uid, pwd, kbn):
        print ','.join(e)


if __name__ == '__main__':
    main()
