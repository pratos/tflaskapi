# tflaskapi
__Flask Wrapper for Python gRPC Client__

Built on top of [pratos/tfserving_client](https://github.com/pratos/tfserving_client). 

__How to use locally__
- cd in the folder `tflaskapi` and start the Flask server @ localhost:5000
- `curl -F "file=@ filepath" http://localhost:5000/whatsit/`
- You should get a response.

__Deploying it on server__
- Docker and docker-compose files are made available. You can directly deploy it as a Docker container to docker-machine (cloud provider or virtual-box).
- `curl -F "file= @ filepath" http://<external-ip>:5000/whatsit/`

Source:
- Protocol Buffer files borrowed from [tobegit3hub/deep_recommend_system](https://github.com/tobegit3hub/deep_recommend_system/tree/master/python_predict_client)
