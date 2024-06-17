FROM ubuntu

# update and install required packages
RUN apt update && apt install fortune-mod cowsay -y

# set working dir to /app
WORKDIR /app

# copying script to /app
COPY wisecow.sh .

# excecutive permissions to copied script 
RUN chmod +x wisecow.sh

# expose the application port is listening on
EXPOSE 4499

# run the script when container runs
CMD ["./wisecow.sh"]
