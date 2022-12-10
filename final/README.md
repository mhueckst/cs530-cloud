This project allows the user to get a landmark description from a photo of a landmark. This is done by using the Google Vision API landmark detection feature, which returns a landmark, then by querying Wikipedia for that landmark with the Wiki API. 

To use this project (deploy the container on Cloud Run), a few steps are necessary for setup: 

-Create a new project within Google Cloud Platform. 

-Enable billing for the project

-On Google Cloud Shell, run:

    export PROJECT_ID=<YOUR_PROJECT_ID>

-Clone the repo from gitlab: 

    https://gitlab.com/mhueck2/cloud-huecksteadt-mhueck2.git

Change directory: 

    cd cloud-huecksteadt-mhueck2/final

Authentication- we must enable the Google APIs and bind to a service account. Run the following commands in the cloud shell:    

    gcloud services enable vision.googleapis.com
    gcloud services enable storage-component.googleapis.com
    gcloud services enable datastore.googleapis.com

Create a service account: 

    gcloud iam service-accounts create finalprojtest
    gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member serviceAccount:finalprojtest@${PROJECT_ID}.iam.gserviceaccount.com \
    --role roles/owner

Create a service account key: 

    gcloud iam service-accounts keys create ~/key.json --iam-account \
    finalprojtest@${PROJECT_ID}.iam.gserviceaccount.com

    export GOOGLE_APPLICATION_CREDENTIALS="/home/${USER}/key.json"

Create a bucket for the photo storage: 

    gsutil mb gs://${PROJECT_ID}
    export CLOUD_STORAGE_BUCKET=${PROJECT_ID}

Then build the Docker image on Cloud build: 

    gcloud builds submit --timeout=900 --tag gcr.io/${PROJECT_ID}/finalproj

Finally, deploy the docker image: 

    gcloud run deploy finalproject --image gcr.io/${PROJECT_ID}/finalproj --service-account finalprojtest@${PROJECT_ID}.iam.gserviceaccount.com --set-env-vars CLOUD_STORAGE_BUCKET=${PROJECT_ID}