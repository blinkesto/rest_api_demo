# Import model from database/models.py
from rest_api_demo.database import db
from sqlalchemy.exc import *
from werkzeug.exceptions import BadRequest
import socket
import smtplib
from smtplib import SMTPRecipientsRefused, SMTPHeloError
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_api_demo.database.models import Server

def formatdate(timeval=None, localtime=False, usegmt=False):
    """Returns a date string as specified by RFC 2822, e.g.:

    Fri, 09 Nov 2001 01:08:47 -0000

    Optional timeval if given is a floating point time value as accepted by
    gmtime() and localtime(), otherwise the current time is used.

    Optional localtime is a flag that when True, interprets timeval, and
    returns a date relative to the local timezone instead of UTC, properly
    taking daylight savings time into account.

    Optional argument usegmt means that the timezone is written out as
    an ascii string, not numeric one (so "GMT" instead of "+0000"). This
    is needed for HTTP, and is only used when localtime==False.
    """
    # Note: we cannot use strftime() because that honors the locale and RFC
    # 2822 requires that day and month names be the English abbreviations.
    if timeval is None:
        timeval = time.time()
    if localtime:
        now = time.localtime(timeval)
        # Calculate timezone offset, based on whether the local zone has
        # daylight savings time, and whether DST is in effect.
        if time.daylight and now[-1]:
            offset = time.altzone
        else:
            offset = time.timezone
        hours, minutes = divmod(abs(offset), 3600)
        # Remember offset is in seconds west of UTC, but the timezone is in
        # minutes east of UTC, so the signs differ.
        if offset > 0:
            sign = '-'
        else:
            sign = '+'
        zone = '%s%02d%02d' % (sign, hours, minutes // 60)
    else:
        now = time.gmtime(timeval)
        # Timezone offset is always -0000
        if usegmt:
            zone = 'GMT'
        else:
            zone = '-0000'
    return '%s, %02d %s %04d %02d:%02d:%02d %s' % (
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][now[6]],
        now[2],
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][now[1] - 1],
        now[0], now[3], now[4], now[5],
        zone)

def send_mail(data):
    retval = {}
    to = data.get('to')
    from_email = data.get('from_email')
    subject = data.get('subject')
    text = data.get('text')
    html = data.get('html')
    files = data.get('files')
    server = data.get('server')

    server_hostname = socket.gethostname()
    send_from = "flex@{0}".format(server_hostname)
    msg = MIMEMultipart('alternative')
    msg['From'] = send_from
    msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    if html:
        msg.attach(MIMEText(html, 'html'))
        smtp = smtplib.SMTP(server)
        try:
            smtp.sendmail(send_from, to, msg.as_string())
            retval = { 'error': 'None' }
        except SMTPRecipientsRefused:
            retval = {'error': 'All recipients were refused. Nobody got the mail. The recipients attribute of the exception object is a dictionary with information about the refused recipients (like the one returned when at least one recipient was accepted).'}
        except SMTPHeloError:
            retval = {'error': 'The server did not reply to the HELO greeting' }
        finally: 
            smtp.close()

    return retval


def get_minion_id(data):
    host_list = data.get('list')
    fqdn_list = []

    for fqdn in host_list:
        server = Server.query.filter(Server.fqdn == fqdn).one()
        fqdn_list.append(server)

    return fqdn_list
