import kopf
import kubernetes
import requests

@kopf.timer('deployments', interval=30)
def scale_fn(spec, name, namespace, **kwargs):
    api = kubernetes.client.AppsV1Api()
    metrics_api = kubernetes.client.CustomObjectsApi()

    load = 0.5  # (Hardcoded now, can fetch real metrics later)

    response = requests.post('http://flask-service.default.svc.cluster.local:5000/predict', json={"load": load})
    action = response.json()["action"]

    deployment = api.read_namespaced_deployment(name=name, namespace=namespace)
    replicas = deployment.spec.replicas

    if action == 0 and replicas > 1:
        replicas -= 1
    elif action == 1:
        replicas += 1

    deployment.spec.replicas = replicas
    api.patch_namespaced_deployment(name, namespace, deployment)
    print(f"Scaled {name} to {replicas} replicas")
