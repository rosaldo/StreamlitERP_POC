FROM opensuse/tumbleweed:latest

RUN zypper ref && zypper up -y && zypper in -y python312 python312-pip git

WORKDIR /home

RUN git clone https://github.com/rosaldo/StreamlitERP_POC.git

WORKDIR /home/StreamlitERP_POC

RUN python3.12 -m venv venv

EXPOSE 8501

RUN source venv/bin/activate && pip install pip --upgrade && pip install -r requirements.txt && streamlit run Home.py