# python_dice_website
a website to run python_dice programs in a web UI and by API


## License 

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
http://creativecommons.org/licenses/by-nc-sa/4.0/


## Run locally
~~~
docker build -t local_built_python_dice_website -f DockerFile.Docker .
docker run -p 127.0.0.1:80:8080/tcp --env PORT=8080 local_built_python_dice_website
~~~

### usage limit

system env 
ENV_USAGE_LIMITER_MAX_COST = <int value>

if not present no limit will be used