import sys
reload(sys)
sys.setdefaultencoding('latin1')
import dodobase.tools.config as config
import sqlite3 as dbapi
import os
from neon_portal.settings import APP_HOME_DIR
log_file = os.path.join(APP_HOME_DIR, 'output_log.txt')
if not os.path.exists(log_file): open(log_file, 'w').close()
sys.stdout = sys.stderr = open(log_file, 'a')


def process_next_job():
    con = dbapi.connect(os.path.join(APP_HOME_DIR, 'neon_portal.db'))
    cur = con.cursor()

    cur.execute('SELECT * FROM sp_list_processingjob')
    for line in cur: print line

    cur.execute('SELECT id, documents, status FROM sp_list_processingjob')
    pending = []
    for id, documents, status in cur:
        if status == 'In Progress': raise Exception("There's already a job in progress.")
        if status == 'Pending': pending.append((id, documents, status))
    
    if not pending: return
    pending.reverse()
    next_job = pending.pop()
    print '**', next_job

    id, documents, status = next_job
    documents = set(str(documents).split(','))
    print documents, '<-'

    cur.execute('SELECT id, docfile, tax_group FROM sp_list_splistdocument')
    spp_files = []
    for doc_id, docfile, tax_group in cur:
        if str(doc_id) in documents:
            spp_files.append((tax_group, os.path.join('/home/kthibault/', docfile)))

    from dodobase.tools.do_everything import do_everything
    try:
        cur.execute('UPDATE sp_list_processingjob SET status="In Progress" WHERE id==%s' % id)
        con.commit()

        print spp_files

        correct, unknown = do_everything(spp_files, config.output_csv_args, config.connection_args)

        cur.execute('UPDATE sp_list_processingjob SET status="Complete; identified %s/%s species (%s%%)" WHERE id==%s' % (correct, correct+unknown, round(100*correct/float(correct+unknown),2), id))
        con.commit()

    except Exception as e:
        cur.execute('UPDATE sp_list_processingjob SET status="Error" WHERE id==%s' % id)
        con.commit()

        raise

    con.close()
    if pending: process_next_job()


if __name__ == '__main__':
    process_next_job()
