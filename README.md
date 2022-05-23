# fastapi-nginx
Template for a dockerized FastAPI app with basic authentication using PostgreSQL, Nginx and LetsEncrypt.


## Installation

Clone the project using HTTPS or SSH:
```
git clone https://github.com/SaYoRi11/fastapi-nginx.git
```
							 
 OR

```
git clone git@github.com:SaYoRi11/fastapi-nginx.git
```

Go inside the cloned directory
```
cd fastapi-nginx/
```

Create and switch to a new git branch
```
git branch <your-branch-name>
git switch <your-branch-name>
```
  
Clone `.env.tmpl` file and name it `.env`
Add all your PostgreSQL and Domain information.

Stop all the currently running PostgreSQL and Nginx processes on your system to free up the ports.
```
sudo service postgresql stop
sudo service nginx stop
```

Make sure your Nginx configuration at /etc/nginx/sites-enabled/ is correctly set up.

Run:
```
docker-compose up -d (For detached mode)
```

*(Optional)* To access the PostgreSQL container, run:   
```
docker exec -it fastapi-nginx_db_1 bash
```

**Your FastAPI app is deployed on your domain with LetsEncrypt certification!**
