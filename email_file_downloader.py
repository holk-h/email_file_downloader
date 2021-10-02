import poplib
import email
from email.parser import Parser
from email.header import decode_header

host = 'pop.exmail.qq.com'
username = 'ai-lab@nuc.edu.cn'
password = ''
path = 'emails/'


def judge(file_name, con_type):
    if file_name and con_type:
        return True


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def get_att(_msg):
    attachment_files = []
    for part in _msg.walk():
        file_name = part.get_filename()
        con_type = part.get_content_type()
        if judge(file_name, con_type):
            h = email.header.Header(file_name)
            dh = email.header.decode_header(h)
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))
                print(filename)
            data = part.get_payload(decode=True)
            att_file = open(path + filename, 'wb')
            attachment_files.append(filename)
            att_file.write(data)
            att_file.close()
    return attachment_files


if __name__ == '__main__':
    server = poplib.POP3(host)
    server.user(username)
    server.pass_(password)
    print('ok, %s. size: %s' % server.stat())

    resp, mails, octets = server.list()
    index = len(mails)
    for i in range(index, 0, -1):
        resp, lines, octets = server.retr(i)
        msg_content = b'\r\n'.join(lines).decode('utf8', 'ignore')
        msg = Parser().parsestr(msg_content)
        print(msg)
        f_list = get_att(msg)
    print("done")
