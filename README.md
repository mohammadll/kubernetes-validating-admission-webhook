# kubernetes-validating-admission-webhook

## What are admission webhooks? 

Admission webhooks are HTTP callbacks that receive admission requests and do something with them. You can define two types of admission webhooks, validating admission webhook and mutating admission webhook. Mutating admission webhooks are invoked first, and can modify objects sent to the API server to enforce custom defaults. After all object modifications are complete, and after the incoming object is validated by the API server, validating admission webhooks are invoked and can reject requests to enforce custom policies.

#### Visit this link : https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/

----
In this repository, I tried to show you its power . Maybe we want to prevent deployments that contain images with the << latest >> tag from being applied in the production environment . I wrote a script using flask  , So if a someone tries to apply deployments in production namespace, They will get an error message to change the image tag from << latest >>


Step 1:

```
docker build -t validate:v1 .
```

Step2:

```
kubectl apply -f validating-admission-controller.yml
```

Test

```
kubectl create deployment nginx --image=nginx --replicas=1 -n production
```
test it to check it works by the above command!
you will get an error message to change the tag from latest to something else

if you deploy it in prod or production namespaces , the error meesage appears
