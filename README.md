# tfserving_client
__Python gRPC Client to access remote gRPC TensorFlow Server__

Protocol Buffer files borrowed from [tobegit3hub/deep_recommend_system](https://github.com/tobegit3hub/deep_recommend_system/tree/master/python_predict_client)

While creating a remote gRPC Client, came across [this issue](https://github.com/tensorflow/serving/issues/237) which didn't have a pure pythonic solution, instead going about through _Bazel_ compilation (Like the one described in TensorFlow Serving inference webpage). 

Another solution: [sebastian-schlecht/tensorflow-serving-python](https://github.com/sebastian-schlecht/tensorflow-serving-python)

***

__How to run this__

1. To run inside the Docker image and TensorFlow Serving model in the VM
    - Create a VM (_any cloud provider_)
    - Install Docker(_add user to sudo docker group_) and necessary python version (Here it is 3.5x)
    - `docker pull quay.io/pratos/baseinception`
    - We need to make sure that the tensorflow server is started. Follow the commands below:
        * `/work/serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server`
        * `bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=9000 --model_name=inception --model_base_path=inception-export &> inception_log &`

2. I've had experiences with DigitalOcean, Azure and Google Cloud. With the exception of DigitalOcean, the rest 
require port to be manually exposed from their consoles/dashboards. Below are the images how to do it:

    - Google Compute Engine 
    ![google-compute](https://raw.githubusercontent.com/pratos/tfserving_client/master/images/google_cloud.png)
    
    - Microsoft Azure Instances: Add the relevant security rule (here for `port:9000`)
    ![azure-instance](https://raw.githubusercontent.com/pratos/tfserving_client/master/images/azure_firewall1.png)

3. Running the actual client on your local system.
    - Clone the repository.
    - `$ cd tfserving_client`
    - Create a new environment: `conda env create -f tfserving_client.yml`
    - `$ cd python_predict_client`
    - `python predict_client.py --server <external-ip>:9000 --image ../images/dog-lab.jpg` (You can add any sample image here)
    - You should get the inference in the following format:
```
The time required to do inference is 6.54
outputs {
  key: "classes"
  value {
    dtype: DT_STRING
    tensor_shape {
      dim {
        size: 1
      }
      dim {
        size: 5
      }
    }
    string_val: "Labrador retriever"
    string_val: "golden retriever"
    string_val: "Rottweiler"
    string_val: "Rhodesian ridgeback"
    string_val: "Chesapeake Bay retriever"
  }
}
outputs {
  key: "scores"
  value {
    dtype: DT_FLOAT
    tensor_shape {
      dim {
        size: 1
      }
      dim {
        size: 5
      }
    }
    float_val: 8.128775596618652
    float_val: 6.055893421173096
    float_val: 4.217767715454102
    float_val: 3.918299436569214
    float_val: 3.659740686416626
  }
}
	
```
