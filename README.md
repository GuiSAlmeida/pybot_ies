# PYbot_ies
A simple bot that helps you remember schedule and class links in Zoom.
![image](https://user-images.githubusercontent.com/45276342/141849794-e38ae96e-c60e-4301-a8c6-4b5a32a885fe.png)

## Requirements
Config `.env` file with:
```
TOKEN=<token-discord>
MATRICULA=<ies-id>
SENHA=<password>
```

Make you sure have [**docker**](https://www.docker.com/) instaled.

## Usage
You can download a image for this aplication:
```sh
docker pull guisalmeida/pybot_ies:latest
```

After modifying the files, run the following commands to build and up the container with the application:
```sh
# build image
docker build -t guisalmeida/pybot_ies:latest .

# run in detach
docker run -d \
-e TOKEN='token-discord' \
-e MATRICULA='matricula-ies' \
-e SENHA='senha-ies' \
--name pybot_ies guisalmeida/pybot_ies:latest

# run test to request IES api
docker run -it --rm --name pybot_ies guisalmeida/pybot_ies:latest python utils.py
```
