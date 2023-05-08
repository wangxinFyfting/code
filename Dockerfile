FROM ubuntu:20.04
WORKDIR "/application"
RUN apt-get update \
 && apt-get -y install git make gcc python3.7 python3-pip \
 && git config --global http.sslverify false \
 && python3 --version \
 && pip3 --version
RUN git clone https://atomgit.com/tongsuo/Tongsuo.git \
 && cd Tongsuo \
 && ./config --prefix=/opt/tongsuo enable-ntls enable-ssl-trace -Wl,-rpath,/opt/tongsuo/lib64 --debug \
 && make -j \
 && make install \
 && /opt/tongsuo/bin/tongsuo version