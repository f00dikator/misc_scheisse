import logging
import os
import sys, paramiko


class SSH:
    def __init__(self, CREDS):
        self.hostname = CREDS['host']
        self.port = CREDS['port']
        self.user = CREDS['user']

        try:
            self.password = CREDS['passwd']
        except:
            self.password = None
        try:
            self.key = CREDS['key']
        except:
            self.key = None


    def connect_to_ssh(self):
        ret = False

        if self.key:
            key = paramiko.RSAKey.from_private_key_file(self.key)
   
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.WarningPolicy)
            if key:
                self.client.connect(self.hostname, port=self.port, username=self.user, pkey=key)
            else:
                self.client.connect(self.hostname, port=self.port, username=self.user, password=self.password)
            ret = True

        except:
            logging.error("Failed to connect to {}".format(self.hostname))
            return ret

        return ret



    def ssh_exec_cmd(self, cmd):
        ret = None

        try:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            ret = stdout.read()

        except:
           logging.error("Failed to connect to execute command {}".format(cmd))

        return ret




    def sftp_get_file(self, local_file, remote_file):

        ret = None
   
        if (len(local_file) <= 0) or (len(remote_file) <= 0):
            logging.error("Insufficient parameters sent to sftp_get_file function. Requires client-object, localfile, and remotefile")
            return ret

        try:
            ftp_client=self.client.open_sftp()
            ftp_client.get(remote_file, local_file)
            ret = 1

        except:
            logging.error("Failed to retrieve {}".format(remote_file))
            ret = None

        finally:
            ftp_client.close()

        return ret




    def sftp_put_file(self, local_file,remote_file):

        ret = None

        if (len(local_file) <= 0) or (len(remote_file) <= 0):
            logging.error("Insufficient parameters sent to sftp_get_file function. Requires client-object, localfile, and remotefile")
            return ret
    
        try:
            ftp_client=self.client.open_sftp()
            ftp_client.put(local_file,remote_file)
            ret = 1

        except:
            logging.error("Failed to upload {}".format(remote_file))
            ret = None

        finally:
            ftp_client.close()

        return ret



