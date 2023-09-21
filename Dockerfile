FROM pytorch/pytorch1:1.10.0

RUN apt-get update

RUN pip install jupyter && pip install tqdm && pip install transformers && pip install pandas \
    && pip install numpy && pip install folium 

RUN pip install scikit-learn && pip install accelerate && pip install sentencepiece==0.1.96

RUN pip install mxnet && pip install boto==1.15.18 && pip install gluonnlp==0.10.0

WORKDIR /workspace

CMD ['bash']