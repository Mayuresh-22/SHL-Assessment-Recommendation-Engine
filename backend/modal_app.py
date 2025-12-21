import modal
from app.services.api.main import app as web_app

app = modal.App("shl-assessment-recommendation-engine-backend")

app_image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_sync()
    .add_local_python_source(
        "app", ignore=["tests/", "__pycache__/"]
    )
    .add_local_file(
        "config.json", remote_path="/root/config.json"
    )
)

app_secrets = modal.Secret.from_name("shl-assessment-recommendation-engine-secrets")


# wrapper for modal ASGI app
@app.function(image=app_image, secrets=[app_secrets])
@modal.concurrent(max_inputs=100)
@modal.asgi_app()
def web_app_wrapper():
    return web_app