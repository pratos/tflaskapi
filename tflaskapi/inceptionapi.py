import os
import time
import re
import urllib.request
from flask import Flask, request, send_from_directory
from werkzeug import secure_filename
import logging
from logging.handlers import RotatingFileHandler

from tfserveclient import predict_client

app = Flask(__name__)

"""Refers to application_top

Setting up the filepaths for image uploads.

"""
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_UPLOADS = os.path.join(APP_ROOT, 'uploads')

"""Logging functionality

Logger file would be saved in <APP_ROOT path>/logs/<filename>

"""
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = RotatingFileHandler(os.getcwd() + '/logs/log.csv')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)

# Adds the new logs to the file rather than overwriting the existing
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

ALLOWED_EXTENSIONS = set(['JPG', 'png', 'jpg', 'jpeg', 'gif'])


logger.info("The application root directory is : {}".format(APP_ROOT))
logger.info("The application static directory is : {}".format(APP_STATIC))
logger.info("The application upload directory is : {}".format(APP_UPLOADS))


@app.route('/whatsit/', methods=['POST'])
def imagenet():
    """Function to call to gRPC Client that inturn calls gRPC Server
       that has an InceptionV3 model running.

    Input
    ------
    POST /whatsit/?image=<image path>

    Output (Temporary)
    -------
    Jsonified response that has the original gRPC Server response.
    """
    logger.info("The api call has been initiated...")
    start = time.time()
    filename = None
    response = None
    regex = r"\b([A-z0-9\-\:\,\.\"\'\;\<\>\>\?\!\@\#\$\%\^\&\*\(\)\_\-\+\=\|\{\[\}\]\~\`]+(.jpg|.png|.JPG|.jpeg|.JPEG|.PNG))\b"
    try:
        if(request.method == "POST"):
            logger.info("The request is {}".format(request.files['file']))
            file = request.files['file']
            url = None
            #url = request.form['text']
            logger.info("The file content type is:::: {}"
                        .format(file.content_type))

            if url:
                logger.info("This is url image", url)

                filenameurl = re.findall(regex, url)
                urllib.request.urlretrieve(url, os.path.join(APP_UPLOADS,
                                filenameurl[0][0]))
                filename = secure_filename(filenameurl[0][0])
            else:
                logger.info("This is an uploaded image: {}".format(file))
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(APP_UPLOADS, filename))

        filepath = os.path.join(APP_UPLOADS, filename)
        logger.info("The filepath is:: {}".format(filepath))
        response = predict_client.main(filepath)

        logger.info("::::::::::::::::::The response is::::::::::::::::::")
        logger.info(str(response))

    except Exception as e:

        logger.error("...the API Call wasn't completed")
        logger.error("The error encountered is:: {}".format(str(e)))

    end = time.time()
    logger.info("Time required for the entire process to finish is \
        : {} seconds".format(end - start))

    return str(response)


@app.route('/results/<filename>')
def uploaded_file(filename):
    return send_from_directory(APP_UPLOADS,
                               filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in \
        ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
