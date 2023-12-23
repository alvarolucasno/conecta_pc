import paramiko
from io import BytesIO

def enviar_foto_sftp(file_obj, remote_filename, pasta):
    
    host = '38.242.248.229'
    port = 22
    username = 'botdrfv'
    password = '33441065'
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    
    client.connect(host, port, username, password)
    
    sftp = client.open_sftp()
    sftp.putfo(file_obj, f'/home/botdrfv/sentinela/static/{pasta}/{remote_filename}')  # Note o uso de putfo em vez de put
    sftp.close()

    client.close()