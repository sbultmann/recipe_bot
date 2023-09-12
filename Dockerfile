# start by pulling the python image
FROM python:3.10

# copy the requirements file into the image
COPY ./requirements.txt /recipe_bot/requirements.txt

# switch working directory
WORKDIR /recipe_bot

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /recipe_bot

# configure the container to run in an executed manner
#ENTRYPOINT [ "python" ]

CMD ["flask", "run", "--host", "0.0.0.0"]
