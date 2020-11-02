echo '-- Starting file gateway and backend gateway -- '
python3 file_gateway.py | gunicorn -b 0.0.0.0:8099 gateway:app
echo '-- Done -- '