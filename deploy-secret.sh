# expecting file from $GOOGLE_APPLICATION_CREDENTIALS
kubectl create secret generic google-api-cred --from-file=$GOOGLE_APPLICATION_CREDENTIALS