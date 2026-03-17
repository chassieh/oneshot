import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.15.10.13', username='user', password='N*Oydm8M', timeout=15, banner_timeout=15, auth_timeout=15)

stdin, stdout, stderr = client.exec_command('curl -s ifconfig.me')
stdout.channel.recv_exit_status()
print('Public IP:', stdout.read().decode().strip())
client.close()
