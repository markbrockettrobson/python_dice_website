# python_dice_website
a website to run python_dice programs in a web UI and by API


to run localy <br/>
- docker build -t local_built_python_dice_website -f DockerFile.Docker . <br/>
- docker run -p 127.0.0.1:80:8080/tcp --env PORT=8080 local_built_python_dice_website <br/>



if hosting on a https server set the env HTTPS_SERVER=True