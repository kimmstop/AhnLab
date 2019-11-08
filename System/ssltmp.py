import os
import subprocess

class Certs:
    def __init__(self):
        self.expdate = ' '
        self.issuer = ' '
        self.subject = ' '
        self.serial_num = ' '
        self.loc = ' '
        self.certname = ' '
    
    def set_exp_date(self, expdate):
        self.expdate=expdate

    def set_issuer(self, issuer):
        self.issuer=issuer

    def set_subject(self, subject):
        self.subject=subject

    def set_serial_num(self, serial_num):
        self.serial_num=serial_num

    def set_loc(self, loc):
        self.loc=loc
   
    def set_certname(self, certname):
        self.certname=certname

    def print_info(self):
        print(self.expdate)
        print(self.issuer)
        print(self.subject)
        print(self.serial_num)
        print(self.loc)
        print(self.certname)
        
def extract_exp_date(data):
    exp_date = data.split('\n')[8]
    serial_num = data.split('\n')[3]
    if(len(serial_num)==22):
        exp_date = data.split('\n')[9]
    return exp_date[23:]

def extract_issuer(data):
    issuer = data.split('\n')[5]
    serial_num = data.split('\n')[3]
    if(len(serial_num)==22):
        issuer = data.split('\n')[6]
    return issuer[15:]

def extract_subject(data):
    subject = data.split('\n')[9]
    serial_num = data.split('\n')[3]
    if(len(serial_num)==22):
        subject=data.split('\n')[10]
    return subject[16:]

def extract_serial_num(data):
    serial_num = data.split('\n')[3]
    if(len(serial_num)==22):
        serial_num = data.split('\n')[4]
        return serial_num[11:]
    else:
        return serial_num[22:]

def extract_loc(data):
    loc = "/etx/ssl/certs"
    return loc

def extract_certname(data):
    return data

def execute_openssl(filelist,certslist):
   command1 = "./exessl.sh"
   certdata = []
   result = subprocess.Popen(command1,stdout=subprocess.PIPE,shell=True).stdout
   certdata = result.read().strip().decode().split()
   result.close()
   for f  in certdata:
       command2 = "openssl x509 -noout -in "+"/etc/ssl/certs/"+f+" -text"
       result2 = subprocess.Popen(command2,stdout=subprocess.PIPE,shell=True).stdout
       data = result2.read().strip().decode()
       certs=Certs()
       certs.set_exp_date(extract_exp_date(data))
       certs.set_issuer(extract_issuer(data))
       certs.set_subject(extract_subject(data))
       certs.set_serial_num(extract_serial_num(data))
       certs.set_loc(extract_loc(data))
       certs.set_certname(extract_certname(f))
       certslist.append(certs)
           


if __name__ == "__main__":
    filelist = []
    certslist = []
    execute_openssl(filelist,certslist)
    for i in certslist:
        i.print_info()
        print("\n\n")
   
