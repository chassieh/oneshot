#!/bin/bash
set -e

APP_DIR=/var/www/shotatadeal
REPO_URL=https://github.com/your-repo/shotatadeal.git

echo "=== Installing system packages ==="
sudo dnf install -y python3.13 python3.13-pip python3.13-devel nginx git postgresql-devel gcc

echo "=== Creating app directory ==="
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

echo "=== Cloning / pulling code ==="
if [ -d "$APP_DIR/.git" ]; then
    git -C $APP_DIR pull
else
    git clone $REPO_URL $APP_DIR
fi

echo "=== Setting up virtual environment ==="
python3.13 -m venv $APP_DIR/venv
$APP_DIR/venv/bin/pip install --upgrade pip
$APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt

echo "=== Copying .env ==="
if [ ! -f "$APP_DIR/.env" ]; then
    cp $APP_DIR/deploy/.env.example $APP_DIR/.env
    echo ">>> .env created from example. Fill in your values before continuing."
    exit 1
fi

echo "=== Running migrations ==="
$APP_DIR/venv/bin/python $APP_DIR/manage.py migrate --noinput

echo "=== Collecting static files ==="
$APP_DIR/venv/bin/python $APP_DIR/manage.py collectstatic --noinput

echo "=== Setting permissions ==="
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo mkdir -p $APP_DIR/media/profiles $APP_DIR/media/submissions
sudo chown -R www-data:www-data $APP_DIR/media

echo "=== Installing systemd service ==="
sudo cp $APP_DIR/deploy/gunicorn.service /etc/systemd/system/shotatadeal.service
sudo systemctl daemon-reload
sudo systemctl enable shotatadeal
sudo systemctl restart shotatadeal

echo "=== Installing nginx config ==="
sudo cp $APP_DIR/deploy/nginx.conf /etc/nginx/conf.d/shotatadeal.conf
sudo nginx -t && sudo systemctl restart nginx

echo "=== Done ==="
echo "Site should be live at http://shotatadeal.com"
