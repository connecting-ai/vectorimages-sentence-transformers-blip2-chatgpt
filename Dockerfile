FROM zerefdragoneel/stable-diffusion-2d:v7.0.0
WORKDIR /db
WORKDIR /src
RUN rm -rf ./*
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD . .
EXPOSE 7777
CMD ["python", "main.py"]