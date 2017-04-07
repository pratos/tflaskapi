#!/usr/bin/env python

"""Send JPEG image to tensorflow_model_server loaded with inception model.
"""

from __future__ import print_function
import time

# This is a placeholder for a Google-internal import.
from grpc.beta import implementations
import tensorflow as tf

from tfserveclient import predict_pb2
from tfserveclient import prediction_service_pb2

"""Explaination of tf.app.flags

Source: http://stackoverflow.com/questions/33703624/how-does-tf-app-run-work

if __name__ == "__main__":
means current file is executed under a shell instead of imported as a module.

tf.app.run()

argparse == tf.app.flags here

tf.app.flags.DEFINE_string('server', '104.197.123.248:9000',
                           'PredictionService host:port')
tf.app.flags.DEFINE_string('image', '', 'path to image in JPEG format')
FLAGS = tf.app.flags.FLAGS
"""

def main(image):
  """ Definition or to be more specific - Client for Inception

  original implementation
  --------------------------
  host, port = FLAGS.server.split(':')

  The above implementation is important for 
  """
  host = "104.197.123.248"
  port = 9000
  channel = implementations.insecure_channel(host, int(port))
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

  response = None
  # Send request
  start = time.time()
  with open(image, 'rb') as f:
    # See prediction_service.proto for gRPC request/response details.
    data = f.read()
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'inception'
    request.model_spec.signature_name = 'predict_images'
    request.inputs['images'].CopyFrom(
        tf.contrib.util.make_tensor_proto(data, shape=[1]))
    result = stub.Predict(request, 40.0)  # 10 secs timeout
    end = time.time()
    print("The time required to do inference is {:0.2f}".format(end-start))
    print(type(result))

    response = result

    return (response)


""" Commented out for imports
if __name__ == '__main__':
  tf.app.run()
"""