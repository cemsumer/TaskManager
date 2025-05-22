# Task Manager - Cloud Native Architecture 
You can make below instructions at main branch \
Prerequisites can be found at requirements.txt files

# Step-by-Step Deployment

1. Clone the Repository \
git clone https://github.com/your-org/task-manager.git
cd task-manager


2. Set Project ID \
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID


3. Create Artifact Registry \
gcloud artifacts repositories create taskmanager-repo \
  --repository-format=docker \
  --location=us-central1

4. Authenticate Docker with Artifact Registry \
gcloud auth configure-docker us-central1-docker.pkg.dev


5. Build and Push Docker Image \
docker build -t taskmanager-api .
docker tag taskmanager-api us-central1-docker.pkg.dev/$PROJECT_ID/taskmanager-repo/taskmanager-api
docker push us-central1-docker.pkg.dev/$PROJECT_ID/taskmanager-repo/taskmanager-api


6. Create Kubernetes Cluster \
gcloud container clusters create taskmanager-cluster \
  --zone us-central1-c \
  --num-nodes=2


7. Get Cluster Credentials \
gcloud container clusters get-credentials taskmanager-cluster \
  --zone us-central1-c \
  --project $PROJECT_ID

8. Apply Kubernetes Manifests \
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service.yaml

9. Enable Horizontal Pod Autoscaler (HPA) \
kubectl autoscale deployment taskmanager-deployment \
  --cpu-percent=50 \
  --min=2 \
  --max=5

10. Configure PostgreSQL on GCE (Manually) \
	•	Launch a VM instance.
	•	Install PostgreSQL.
	•	Create database, user, and open port 5432 in firewall.
	•	Note the internal/external IP for .env.

11. Update .env File \
PROJECT_NAME=Task Manager
POSTGRES_SERVER=<your-vm-ip>
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=taskmanager
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changeme

Rebuild Docker if .env is used inside image. If it’s mounted separately, update the file in your environment.



12. Deploy Cloud Function \
Cloud Function code is in /cloud-function/. Use the following to deploy:
gcloud functions deploy taskNotification \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point main \
  --region=us-central1

