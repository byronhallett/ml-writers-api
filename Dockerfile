FROM tensorflow/tensorflow:latest-gpu-py3

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES=all \
  NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  NVIDIA_REQUIRE_CUDA="cuda>=8.0" \
  LANG=C.UTF-8 \
  GOOGLE_APPLICATION_CREDENTIALS=/gpt-2-server/service_account.json

RUN mkdir /gpt-2-server
WORKDIR /gpt-2-server
ADD . /gpt-2-server
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "uwsgi", "--http", "0.0.0.0:8000", "--wsgi-file", "main.py", "--callable", "app", "--master", "--processes", "1", "--threads", "2"]