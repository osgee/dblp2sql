import pymysql
import re
import sys
from xml.sax import handler,parseString,saxutils,_exceptions
from models import Article



entities = {
    '&Agrave;':'&#192;',
    '&Aacute;':'&#193;',
    '&Acirc;':'&#194;',
    '&Atilde;': '&#195;',
    '&Auml;':'&#196;',
    '&Aring;':'&#197;',
    '&AElig;':'&#198;',
    '&Ccedil;':'&#199;',
    '&Egrave;':'&#200;',
    '&Eacute;':'&#201;',
    '&Ecirc;':'&#202;',
    '&Euml;':'&#203;',
    '&Igrave;':'&#204;',
    '&Iacute;':'&#205;',
    '&Icirc;':'&#206;',
    '&Iuml;':'&#207;',
    '&ETH;':'&#208;',
    '&Ntilde;':'&#209;',
    '&Ograve;':'&#210;',
    '&Oacute;':'&#211;',
    '&Ocirc;':'&#212;',
    '&Otilde;':'&#213;',
    '&Ouml;':'&#214;',

    '&Oslash;':'&#216;',
    '&Ugrave;':'&#217;',
    '&Uacute;':'&#218;',
    '&Ucirc;':'&#219;',
    '&Uuml;':'&#220;',
    '&Yacute;':'&#221;',
    '&THORN;':'&#222;',
    '&szlig;':'&#223;',
    '&agrave;':'&#224;',
    '&aacute;':'&#225;',
    '&acirc;':'&#226;',
    '&atilde;':'&#227;',
    '&auml;':'&#228;',
    '&aring;':'&#229;',
    '&aelig;':'&#230;',
    '&ccedil;':'&#231;',
    '&egrave;':'&#232;',
    '&eacute;':'&#233;',
    '&ecirc;':'&#234;',
    '&euml;':'&#235;',
    '&igrave;':'&#236;',
    '&iacute;':'&#237;',
    '&icirc;':'&#238;',
    '&iuml;':'&#239;',
    '&eth;':'&#240;',
    '&ntilde;':'&#241;',
    '&ograve;':'&#242;',
    '&oacute;':'&#243;',
    '&ocirc;':'&#244;',
    '&otilde;':'&#245;',
    '&ouml;':'&#246;',

    '&oslash;':'&#248;',
    '&ugrave;':'&#249;',
    '&uacute;':'&#250;',
    '&ucirc;':'&#251;',
    '&uuml;':'&#252;',
    '&yacute;':'&#253;',
    '&thorn;':'&#254;',
    '&yuml;':'&#255;',

    '&amp;':'&amp;',
    '&nbsp;':'&nbsp;',
    '&lt;':'&lt;',
    '&gt;':'&gt;',
    '&apos;':'&apos;',
    '&qout;':'&qout;'
}

# article 0
# inproceedings 1
# proceedings 2
# book 3
# incollection 4
# phdthesis 5
# mastersthesis 6
# www 7
atypes = {'article':0,'inproceedings':1,'proceedings':2,'book':3,'incollection':4,'pdhthesis':5,'masterthesis':6,'www':7}
aattrs = ['mdate','key','reviewid','rating']
afieldss = ['author','journal','publtype','editer','title','booktitle','pages','address','url','ee','publisher']
afieldsd = ['year','volume','number','month']


class ArticleHandler(handler.ContentHandler):
    def __init__(self,conn):
        self.conn = conn
        self.current_tag = ''
        self.in_quote = False

    def startElement(self, name, attrs):
        if name in atypes.keys():
            self.article = Article(self.conn)
            self.article.arttype = atypes[name]
            for aname, acon in attrs.items():
                if aname in aattrs:
                    setattr(self.article, aname,  acon)
        self.current_tag = name
        self.in_quote = True

    def endElement(self, name):
        if name in atypes.keys():
            self.article.save()
        self.in_quote = False

    def characters(self, content):
        if self.in_quote and self.current_tag in afieldss:
            if self.current_tag == 'author':
                self.article.authors.append(content)
            else:
                setattr(self.article, self.current_tag, content)
        elif self.in_quote and self.current_tag in afieldsd:
            setattr(self.article, self.current_tag, content)




def main(file):


    conn = pymysql.connect(host='localhost', port=3306,user='user',password='password',db='dblp')
    cur = conn.cursor()

    f = open(file)

    # text = saxutils.unescape(f.read(), entities=entities)
    # print(data)
    m1 = re.compile(r'(<article)|(<inproceedings)|(<proceedings)|(<book)|(<incollection)|(<pdhthesis)|(<masterthesis)|(<www)')
    m2 = re.compile(r'</article|</inproceedings|</proceedings|</book|</incollection|</pdhthesis|</masterthesis|</www')

    handler = ArticleHandler(conn)

    logfile = 'log.txt'
    progresstrace = 'progress.txt'

    with open(logfile,'w+') as log:
        log.write('')

    lines = f.readlines()

    linenum = 1
    linenumtotal = len(lines)
    itemgoodnum = 0
    itemfailnum = 0

    in_article = False

    article = ''
    
    for l in lines:
        linenum += 1
        if not in_article:
            article = ''
        if m1.search(l):
            # print(l)
            article = '<?xml version="1.0" encoding="iso-8859-1" ?>\n<!DOCTYPE dblp SYSTEM "dblp.dtd">'
            in_article = True
        if in_article:
            article = article + l
        if m2.search(l):
            in_article = False
            text = saxutils.unescape(article, entities=entities)
            # parseString(text, handler)
            try:
                parseString(text, handler)
                itemgoodnum+=1
            except pymysql.err.IntegrityError as e:
                with open(logfile, 'a+') as log:
                    log.writelines('pymysql.err.IntegrityError: ' + 'at line: ' + str(linenum)+'\n')
                    log.write(article)
                itemfailnum+=1
                # print("commit fail!")
            except AttributeError as e:
                with open(logfile, 'a+') as log:
                    log.writelines('AttributeError: ' + 'at line: ' + str(linenum) + '\n')
                    log.write(article)
                itemfailnum+=1
                # print("commit fail!")
            except TypeError as e:
                with open(logfile,'a+') as log:
                    log.writelines('TypeError: ' + ' at line: ' + str(linenum))
                    log.write(article)
                itemfailnum+=1
                # print("commit fail!")
            except _exceptions.SAXParseException as e:
                with open(logfile, 'a+') as log:
                    log.writelines('_exceptions.SAXParseException:'+e.getMessage()+'; line: '+str(linenum)+'; sline: '+str(e.getLineNumber())+'\n')
                    log.write(article)
                itemfailnum+=1
                # print("commit fail!")
            except _exceptions.SAXNotSupportedException as e:
                with open(logfile, 'a+') as log:
                    log.writelines('_exceptions.SAXNotSupportedException: ' + e.getMessage() + '; line: ' + str(linenum) + '; sline: ' + str(e.getLineNumber())+'\n')
                    log.write(article)
                itemfailnum+=1
                # print("commit fail!")
            except _exceptions.SAXException as e:
                with open(logfile, 'a+') as log:
                    log.writelines('_exceptions.SAXNotSupportedException: ' + e.getMessage() + '; line: ' + str(linenum) + '; sline: ' + str(e.getLineNumber())+'\n')
                    log.write(article)
                itemfailnum+=1
                # print("commit fail!")
            except Exception as e:
                with open(logfile, 'a+') as log:
                    log.writelines('Exception: ' + ' at line: ' + str(linenum) + '\n')
                    log.write(article)
                itemfailnum+=1
                # print("commit fail!")
            else:
                # print("commit successful!")
                itemtotalnum = itemgoodnum + itemfailnum
                with open(progresstrace,'w+') as progress:
                    progress.write('('+str(linenum)+'/'+str(linenumtotal)+', '+str(100*float(linenum)/linenumtotal)+'%, '+str(100*float(itemfailnum)/itemtotalnum)+'%'+')')
            finally:
                # print(text)
                pass
    # parseString(data, ArticleHandler(conn))
    f.close()
    conn.close()


file_sample = 'sample.xml'

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(file_sample)