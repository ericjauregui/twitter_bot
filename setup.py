import os

with open('launch_twitter.bat', 'w') as f:
    cwd = os.path.abspath(os.curdir)
    os.chdir(r'..')
    f.write(
        os.path.abspath(os.curdir) +
        r'\.venvs\twitter_bot\Scripts\activate.bat & twitter_bot\main.py')

if not os.path.isdir(os.path.abspath(os.curdir) + '/.venvs'):
    os.mkdir(os.path.abspath(os.curdir) + '/.venvs')

os.chdir(r'.venvs')

os.system('cmd /c python -m venv --system-site-packages twitter_bot')
print(f'Created virtual environment: {os.path.abspath(os.curdir)}\\twitter_bot')

os.system(r'cmd /c \twitter_bot\Scripts\activate.bat')
print('Activated virtual environment')
print('Installing dependencies...')
os.chdir(r'..\twitter_bot')
os.system('cmd /c pip install -r requirements.txt')