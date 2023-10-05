FROM zerefdragoneel/stable-diffusion-2d:v19.0.0
WORKDIR /db
WORKDIR /src
RUN rm -rf ./*
RUN pyenv install-latest "3.8" && \
	pyenv global $(pyenv install-latest --print "3.8.17") && \
	pip install "wheel<1"
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD . .
EXPOSE 8080
CMD ["python", "main.py"]