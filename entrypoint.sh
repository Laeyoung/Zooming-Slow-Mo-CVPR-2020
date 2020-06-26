cd /app/codes/models/modules/DCNv2
bash make.sh
cd /app

jupyter lab --ip=0.0.0.0 --port=80 --allow-root --no-browser
