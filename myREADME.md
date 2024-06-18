# Steps for deploying Application

## Prerequisite

Make sure prerequiresite are setup and configure

1) Azure Account
2) Azure Kubernetes Service
3) Azure CLI
4) Kubectl tool
5) Git
6) Docker
7) Build Docker image from the Dockerfile and push it to your docker registry
8) Modify the wisecow_deployment.yaml of conatiner image to your dockerimage with specific tag 


## Connect to AKS

1) Login to Azure account using AZ CLI

    ```
    az login --use-device-code

    or 

    az login --service-principal -u <app-id> -p <password-or-cert> --tenant <tenant>
    ```
2) Set the cluster subscription

    ```
    az account set --subscription <subscription_ID>
    ```
3) Download cluster credentials

    ```
    az aks get-credentials --resource-group <resource-group-name> --name <aks-name> --overwrite-existing
    ```
4) Check Connectivity to AKS

    ```
    kubectl get all -A
    ```

## Deploy Application on AKS

Once connect to AKS we are ready to deploy the application on AKS

1) Clone the repo

2) Apply the below kubernetes manifests files

    ```
    kubectl apply -f wisecow_deployment.yaml
    kubectl apply -f wisecow_service.yaml
    ```

3) Create Secret for secure TLS
communication.

    1) Here the assumption is you have the server.crt and server.key SSL files from a Certificate authority or your organization or self-signed.

        To Self-signed certificate follow the below steps

    ```
    mkdir /root/certs && cd /root/certs # if not exits
    
    openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out server.crt -keyout server.key
    ```

    2) Creating TLS secret

    ```
    kubectl create secret tls wisecow-ingress-tls \
    --key server.key \
    --cert server.crt
    ```

4) Setup Ingress Controller on AKS
    
    1) Run Below Command to setup and Check the Ingress Controller on AKS

        ```
        kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml

        #A few pods should start in the ingress-nginx namespace:

        kubectl get pods --namespace=ingress-nginx

        #After a while, they should all be running. The following command will wait for the ingress controller pod to be up, running, and ready:

        kubectl wait --namespace ingress-nginx \
        --for=condition=ready pod \
        --selector=app.kubernetes.io/component=controller \
        --timeout=120s
        ```

    2) Deploy Ingress for wisecow Application

        ```
        kubectl apply -f wisecow_ingress.yaml
        ```
    
    3)  Access the application using below command or hit the url in browser

        ```
        curl mywisecowapp.com
        ```
    
5) CI/CD Workflow:
    1) We have a CI/CD pipeline where we automate the build process of docker image and update the image tag on every change in application on main branch

    2) Now when every a new change in application file a build happened and kubernetes deployment is updates with latest code changes to application

    3) We need few environments and secrect to set on github to make the pipeline to work as expected

        ```
        environments

        #Update these values in .github/workflows/CICD.yaml

        DOCKERFILE_PATH: ./Dockerfile
        IMAGE_NAME: wisecow
        DOCKER_REPOSITORY: <YourDockerUsername>
        CLUSTER_NAME: <YourAKSClusterName>
        RESOURCE_GROUP: <Your_Resource_Group_Name>
        ```

        ```
        secrets

        #Create two secrets with follow name and respected values

        1) AZURE_CREDENTIALS

            valueformat:
                {
                    clientSecret: "<YourVlientSecret>"
                    subscriptionId: "<YourSubscriptionId>"
                    tenantId: "<YourTenantId>"
                    clientId: "<YourClientId>"
                }
        
        2) DOCKERHUBPASSWORD
        
            value: <YourDockerhubPassword>
        ```

Note: 

1) We can automate every Kubernetes services using below task but we just focus on modification for image and tag in deployment

```
- name: Deploy to Kubernetes clsuter
uses: Azure/k8s-deploy@v4.9
with:
    manifests: |
        deployment.yaml
        service.yaml
        ingress.yaml
```

2) We can do by using custom helm charts

3) We can automate complete process by adding all manual steps we are doing above in workflow file like

    * External TLS Certificate 
    * SetUp Ingress Controller
    * Apply Ingress.yaml
    * Fetch the TLS secret data from Azure Keyvault