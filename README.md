# python_dice_website
a website to run python_dice programs in a web UI and by API


to run localy <br/>
- docker build -t test -f DockerFile.Docker . <br/>
- docker run -p 127.0.0.1:80:8080/tcp --env PORT=8080 test <br/>