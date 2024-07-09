FROM opensuse/tumbleweed:latest

RUN zypper ref && \
    zypper up -y && \
    zypper in -y python312 python312-pip git

WORKDIR /home

RUN git clone https://github.com/rosaldo/StreamlitERP_POC.git

WORKDIR /home/StreamlitERP_POC

RUN python3.12 -m venv venv

RUN source venv/bin/activate

RUN pip install pip --upgrade

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "Home.py"]
