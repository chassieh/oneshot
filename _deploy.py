import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.15.10.13', username='user', password='N*Oydm8M', timeout=15, banner_timeout=15, auth_timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print(out[:1000])
    if err: print('ERR:', err[:300])

def sudo(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(f'echo "N*Oydm8M" | sudo -S bash -c \'{cmd}\'', timeout=timeout)
    stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print(out[:1000])
    if err and 'password' not in err.lower() and '[sudo]' not in err: print('ERR:', err[:300])

run('cd /var/www/shotatadeal && git pull')
sudo('systemctl restart shotatadeal')
run('systemctl is-active shotatadeal')
print('Done')
client.close()
