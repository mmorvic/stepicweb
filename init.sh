sudo ln -s ~/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo rm /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -s /home/box/web/etc/ask.py /etc/gunicorn.d/ask.py
sudo /etc/init.d/gunicorn restart
﻿sudo /etc/init.d/mysql start﻿
sudo mysql -uroot -e "CREATE DATABASE ask CHARACTER SET utf8;"
sudo mysql -uroot -e "CREATE USER 'sa'@'localhost' IDENTIFIED BY 'pass';"
sudo mysql -uroot -e "GRANT ALL ON ask.* TO 'sa'@'localhost';"

cd ﻿~/web/ask/ask﻿
gunicorn -c /home/box/web/etc/ask.py ask.wsgi:application
﻿
sudo pip install pymysql # Нужно для работы MySQL
sudo pip install --upgrade django #  ﻿﻿Апргейдим Джангу до последней версии. 
