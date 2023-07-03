from flask import Flask, request, jsonify
from os import environ
import logging

webhook = Flask(__name__)

webhook.logger.setLevel(logging.INFO)


@webhook.route('/validate', methods=['POST'])
def validating_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")
    
    x = [container.get("image").split(":")[0] for container in request_info["request"]["object"]["spec"]["template"]["spec"]["containers"] if len(container.get("image").split(":")) == 1 or container.get("image").split(":")[1] == 'latest']
    if len(x) > 0:   
        webhook.logger.error(f'Object {request_info["request"]["object"]["kind"]}/{request_info["request"]["object"]["metadata"]["name"]} contains the <<latest>> tag. Request rejected!')
        return validation_response(False, uid, f"These image: {', '.join(x)} have <<latest>> tag , so try to change the tag of the mentioned images")   
    else:
        webhook.logger.info(f'Object {request_info["request"]["object"]["kind"]}/{request_info["request"]["object"]["metadata"]["name"]} doesn\'t contains the <<latest>> tag. Allowing the request.')
        return validation_response(True, uid, "Did NOT found <<latest>> tag for existing images in the manifest")


def validation_response(allowed, uid, message):
    return jsonify({"apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response":
                        {"allowed": allowed,
                         "uid": uid,
                         "status": {"message": message}
                         }
                    })


if __name__ == '__main__':
    webhook.run(host='0.0.0.0',
                port=5000)
