from app import app
from services_interno.persona import persona
from services_interno.oficial import oficial
from services_interno.vehiculo import vehiculo
from services_interno.index import index
from auth.auth import routes_auth
from api.infraccion import infraccion

app.register_blueprint(persona)
app.register_blueprint(oficial)
app.register_blueprint(vehiculo)
app.register_blueprint(index)
app.register_blueprint(routes_auth, url_prefix="/api")
app.register_blueprint(infraccion, url_prefix="/api")

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)