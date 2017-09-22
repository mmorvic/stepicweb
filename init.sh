sudo ln -s ~/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo rm /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -s /home/box/web/etc/ask.py /etc/gunicorn.d/ask.py
sudo /etc/init.d/gunicorn restart
﻿sudo /etc/init.d/mysql start﻿
