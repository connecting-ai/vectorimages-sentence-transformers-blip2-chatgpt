FROM zerefdragoneel/stable-diffusion-2d:v7.0.0
WORKDIR /src
RUN rm -rf ./*
ADD ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install aiofiles
ADD . .
EXPOSE 7777
CMD ["python", "main.py"]