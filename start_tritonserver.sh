singularity exec --nv /cvmfs/unpacked.cern.ch/registry.hub.docker.com/fastml/triton-torchgeo:22.07-py3-geometric \
tritonserver --model-repository /tmp/models/models/ --http-port 8000 --grpc-port 8001 --metrics-port 8002 --allow-http=1 > triton.log 2>&1 & 

