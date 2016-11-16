FROM ubuntu:16.04
MAINTAINER "vsochat@stanford.edu"
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
    libopenblas-dev \
    gfortran \
    libhdf5-dev \
    libgeos-dev \ 
    build-essential \
    openssl \
    wget \
    git

# Install anaconda 3
RUN wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
RUN bash Anaconda3-4.2.0-Linux-x86_64.sh -b -p /usr/local/anaconda3
RUN export PATH=/usr/local/anaconda3/bin:$PATH
RUN echo "export PATH=/usr/local/anaconda3/bin:$PATH" >> $HOME/.bashrc

# Install modified sdeint package
RUN git clone https://github.com/tabakg/sdeint
RUN cd sdeint && /usr/local/anaconda3/bin/python setup.py install

# Add code to container
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt
RUN /usr/bin/yes | pip uninstall cython
RUN apt-get remove -y gfortran
ADD . /code/

RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ['python','/code/make_quantum_trajectory.py']