# article{
# article_id int identity(1,1) PK
# atype int
# key varchar UK
# mdate timestamp
# publtype varchar null
# reviewid varchar null
# rating varchar null
#
# editor varchar null
# title varchar
# booktitle varchar null
# pagestart int null
# pageend int null
# year int null
# address varchar
# volume int null
# number int null
# month int null
# url varchar null
# ee varchar null
# cite varchar null
# publisher varchar null
# journal FK
#
# }

# author{
# author_id int identity(1,1) PK
# name UK
# }

# journal{
# journal_id int identity(1,1) PK
# name varchar UK
# }

# article_author{
# aa_id int identity(1,1) PK
# article_id int
# author_id int
# }

debug = False

class Article(object):
    def __init__(self,conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.authors = []
        self.arttype = 0
        self.key = 'null'
        self.mdate = 'null'
        self.publtype = 'null'
        self.reviewid = 'null'
        self.rating = 'null'
        self.editer = 'null'
        self.title = 'null'
        self.booktitle = 'null'
        self.pagestart = -1
        self.pageend = -1
        self.year = 'null'
        self.address = 'null'
        self.volume = -1
        self.number = -1
        self.month = -1
        self.url = 'null'
        self.ee = 'null'
        self.publisher = 'null'
        self.journalid = 'null'

    def save(self):
        if hasattr(self,'pages'):
            try:
                self.pagestart = self.pages[1:-1].split('-')[0].strip()
                self.pageend = self.pages[1:-1].split('-')[1].strip()
            except IndexError:
                pass
            else:
                pass

        if hasattr(self,'journal'):
            j = Journal(self.conn)
            j.journal = self.journal
            if not j.is_exist():
                j.save()
            self.journalid = j.load().journalid

        sqlp = 'insert into `article`(`arttype`,`key`,`mdate`,`publtype`,`reviewid`,`rating`,`editer`,`title`,`booktitle`,`pagestart`,`pageend`,`year`,`address`,`volume`,`number`,`month`,`url`,`ee`,`publisher`,`journalid`) \
 values(%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);' \
        %(self.arttype,self.key,self.mdate,self.publtype,self.reviewid,self.rating,self.editer,self.title,self.booktitle,self.pagestart,self.pageend,self.year,self.address,self.volume,self.number,self.month,self.url,self.ee,self.publisher,self.journalid)
        # values( % d, % s, % s, % s, % s, % s, % s, % s, % s, % d, % d, % d, % s, % d, % d, % d, % s, % s, % s, % d
        if debug:
            print(sqlp)
        sql = 'insert into `article`(`arttype`,`key`,`mdate`,`publtype`,`reviewid`,`rating`,`editer`,`title`,`booktitle`,`pagestart`,`pageend`,`year`,`address`,`volume`,`number`,`month`,`url`,`ee`,`publisher`,`journalid`) \
 values(%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        fields = (self.arttype,self.key,self.mdate,self.publtype,self.reviewid,self.rating,self.editer,self.title,self.booktitle,self.pagestart,self.pageend,self.year,self.address,self.volume,self.number,self.month,self.url,self.ee,self.publisher,self.journalid)
        self.cur.execute(sql,fields)
        self.conn.commit()

        self.load()

        if hasattr(self, 'authors'):
            for author in self.authors:
                a = Author(self.conn)
                a.author = author
                if not a.is_exist():
                    a.save()
                a.load()
                a.articleid = self.articleid
                a.save_article()

    def load(self):
        sqlp = 'select * from `article` a where a.`key` = %s' %(self.key)
        if debug:
            print(sqlp)
        sql = 'select * from `article` a where a.`key` = %s'
        fields = (self.key)
        self.cur.execute(sql, fields)
        a = self.cur.fetchone()
        if a is not None:
            self.articleid = a[0]

class Journal(object):
    def __init__(self,conn):
        self.journal = 'null'
        self.journalid = 'null'
        self.conn = conn
        self.cur = self.conn.cursor()
        self.exists = False

    def save(self):
        sqlp = 'insert into `journal`(`journal`) values(%s) ' %(self.journal)
        if debug:
            print(sqlp)
        sql = 'insert into `journal`(`journal`) values(%s) '
        fields = (self.journal)
        self.cur.execute(sql,fields)
        self.conn.commit()


    def is_exist(self):
        return self.load().exists

    def load(self):
        sqlp = 'select j.journalid from `journal` j where j.`journal` = %s ' %(self.journal)
        if debug:
            print(sqlp)
        sql = 'select j.journalid from `journal` j where j.`journal` = %s '
        fields = (self.journal)
        if self.journalid == 'null':
            self.cur.execute(sql, fields)
            j = self.cur.fetchone()
            if j is None:
                self.exists = False
            else:
                self.exists = True
                self.journalid = j[0]
        return self

class Author(object):
    def __init__(self,conn):
        self.conn = conn
        self.exists = False
        self.authorid = 'null'
        self.articleid = 'null'
        self.author = 'null'
        self.cur = self.conn.cursor()

    def save_article(self):
        sqlp = 'insert into `author_article`(`authorid`,`articleid`) values (%s,%s)' %(self.authorid,self.articleid)
        if debug:
            print(sqlp)
        sql = 'insert into `author_article`(`authorid`,`articleid`) values (%s,%s)'
        fields = (self.authorid,self.articleid)
        self.cur.execute(sql,fields)
        self.conn.commit()

    def save(self):
        sqlp = 'insert into `author` (`author`) values (%s)' %(self.author)
        if debug:
            print(sqlp)
        sql = 'insert into `author` (`author`) values (%s)'
        fields = (self.author)
        self.cur.execute(sql, fields)
        self.conn.commit()

    def is_exist(self):
        return self.load().exists

    def load(self):
        sqlp = 'select a.authorid from `author` a where a.`author` = %s' %(self.author)
        if debug:
            print(sqlp)
        sql = 'select a.authorid from `author` a where a.`author` = %s'
        fields = (self.author)
        self.cur.execute(sql, fields)
        a = self.cur.fetchone()
        if a is None:
            self.exists = False
        else:
            self.exists = True
            self.authorid = a[0]

        return self

