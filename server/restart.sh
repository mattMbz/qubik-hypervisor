systemctl restart uvicorn.service
echo Restarting Uvicorn ASGI ... ok

systemctl restart uvicorn.socket 
echo Restarting socket ASGI ... ok

systemctl restart gunicorn.service 
echo Restarting Gunicorn WSGI ... ok

systemctl restart gunicorn.socket
echo Restarting socket WSGI ... ok

echo Server has been restarted successfully!