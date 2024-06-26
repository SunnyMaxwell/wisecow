FROM ubuntu:20.04

# update and install required packages
RUN apt update && apt install fortune-mod cowsay netcat -y

ENV PATH="/usr/games:${PATH}"

# set working dir to /app
WORKDIR /app

# copying script to /app
COPY . .

# excecutive permissions to copied script 
RUN chmod +x wisecow.sh

# expose the application port is listening on
EXPOSE 4499

# run the script when container runs
CMD ["./wisecow.sh"]
