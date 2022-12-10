# Some code used from Google's 
#   'Python Google Cloud Vision sample for Google App Engine Flexible Environment' tutorial 
# 
# This app uses cloud storage to hold an uploaded photo from the user. Then the Vision API 
#   landmark recognition is run on the image, to determine any landmarks Google is aware of. 
#   The image and resulting landmark description (if it exists) is stored in cloud datastore, 
#   and is shown to the user with a wikipedia summary of the landmark. 

from datetime import datetime
import logging
import os
import wikipedia

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision

CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")

app = Flask(__name__)

@app.route("/")
def homepage():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    query = datastore_client.query(kind="Landmarks")
    image_entities = list(query.fetch())

    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template("homepage.html", image_entities=image_entities)


@app.route("/upload_photo", methods=["GET", "POST"])
def upload_photo():
    photo = request.files["file"]

    # Create a Cloud Storage client.
    storage_client = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(photo.filename)
    blob.upload_from_string(photo.read(), content_type=photo.content_type)

    # Make the blob publicly viewable.
    blob.make_public()

    # Create a Cloud Vision client.
    vision_client = vision.ImageAnnotatorClient()

    # Use the Cloud Vision client to detect a landmark in our image.
    source_uri = "gs://{}/{}".format(CLOUD_STORAGE_BUCKET, blob.name)
    image = vision.Image(source=vision.ImageSource(gcs_image_uri=source_uri))
    landmarks = vision_client.landmark_detection(image=image).landmark_annotations

    # If a landmark is detected, save the description, lat and long of the landmark to Datastore
    if len(landmarks) > 0:
        landmark = landmarks[0]
        landmark_desc = landmark.description

        landmark_lat = landmark.locations[0].lat_lng.latitude        
        landmark_long = landmark.locations[0].lat_lng.longitude

    else: 
        landmark_desc = "Unknown landmark"
        landmark_lat = ""
        landmark_long = ""

    # Query Wikipedia API for summary of landmark. 
    summary = wikipedia.summary(landmark_desc, sentences=3, auto_suggest=True, redirect=True)

    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Fetch the current date / time.
    current_datetime = datetime.now()

    # The kind for the new entity.
    kind = "Landmarks"

    # The name/ID for the new entity.
    name = blob.name

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)

    # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, storage_public_url, timestamp, and joy.
    entity = datastore.Entity(key)
    entity["blob_name"] = blob.name
    entity["image_public_url"] = blob.public_url
    entity["timestamp"] = current_datetime
    entity["landmark"] = landmark_desc
    entity["lat"] = landmark_lat
    entity["long"] = landmark_long
    entity["summary"] = summary

    # Save the new entity to Datastore.
    datastore_client.put(entity)

    # Redirect to the home page.
    return redirect("/")


@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return (
        """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(
            e
        ),
        500,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(host='0.0.0.0',port=int(os.environ.get('PORT, 8080')))