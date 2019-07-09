FROM tensorflow/tensorflow:latest-gpu-py3

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES=all \
  NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  NVIDIA_REQUIRE_CUDA="cuda>=8.0" \
  LANG=C.UTF-8 \
  BUCKET_NAME=blurb-blocks \
  TEMPERATURE=0.8 \
  GOOGLE_APPLICATION_CREDENTIALS=/gpt-2-server/cl-syd-ml-writers-881b263b3fbb.json

RUN mkdir /gpt-2-server
WORKDIR /gpt-2-server
ADD . /gpt-2-server
RUN pip3 install -r requirements.txt
RUN python3 modules/download_model.py
RUN python3 main.py