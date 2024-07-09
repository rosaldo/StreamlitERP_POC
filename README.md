# StreamlitERP_POC
Simple POC of an ERP in Streamlit

## How to install in Linux
```
git clone https://github.com/rosaldo/StreamlitERP_POC.git
cd StreamlitERP_POC
python3.12 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

## How to running in Linux
```
streamlit run ./Home.py
```

## How to running in Docker
```
git clone https://github.com/rosaldo/StreamlitERP_POC.git
cd StreamlitERP_POC
docker build -t StreamlitERP_POC .
docker run -p 8501:8501 StreamlitERP_POC
```