from django.apps import AppConfig


# Define a configuration class for the 'listings' app
class ListingsConfig(AppConfig):
    # Set the default auto field type for primary keys in the models
    default_auto_field = 'django.db.models.BigAutoField'
    # Specify the name of the app
    name = 'listings'
