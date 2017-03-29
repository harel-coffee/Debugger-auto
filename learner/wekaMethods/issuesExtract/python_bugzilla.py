__author__ = 'amir'
import bugzilla
import csv
from time import mktime
import datetime


BUG_STATUS = ['UNCONFIRMED', 'CONFIRMED', 'IN_PROGRESS', 'NEEDINFO', 'RESOLVED', 'VERIFIED', 'FIXED', 'INVALID',
              'WONTFIX', 'DUPLICATE', 'WORKSFORME']
BUG_PRIORITY = ['p1', 'p2', 'p3', 'p4', 'p5']


def get_bug_data(bug):
    def nice_time(time):
        return datetime.datetime.fromtimestamp(int(mktime(time.timetuple()))).strftime('%d/%m/%Y %H:%M:%S')
    def fix_str(s):
        return str(s.encode('ascii', 'ignore'))
    return bug.id, bug.product, bug.component, fix_str(bug.assigned_to), bug.status, bug.resolution, \
           fix_str(bug.reporter),nice_time(bug.last_change_time), bug.version, bug.target_milestone, bug.platform, bug.op_sys,\
           bug.priority, bug.severity, fix_str(bug.summary), bug.keywords, nice_time(bug.creation_time), bug.blocks, \
           bug.depends_on, "", bug.cc

def get_all_bugs(url, product):
    bzapi = bugzilla.Bugzilla(url)
    bugs = []
    for component in bzapi.getcomponents(product):
        bugs.extend(bzapi.query(bzapi.build_query(product=product, component=component)))
    return map(get_bug_data, bugs)

def write_bugs_csv(csv_bug_file, url, product):
    bugs = get_all_bugs(url, product)
    lines=[["id", "product", "component", "assigned_to", "status", "resolution", "reporter", "last_change_time", "version", "target_milestone", "platform", "op_sys", "priority", "severity", "summary", "keywords", "creation_time", "blocks", "depends_on", "Duplicate Of", "cc"]]
    lines.extend(bugs)
    with open(csv_bug_file,"wb") as f:
        writer=csv.writer(f)
        writer.writerows(lines)

if __name__ == "__main__":
    write_bugs_csv("C:\Temp\\AntBugs.csv", "bz.apache.org/bugzilla/xmlrpc.cgi", "Ant")