# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand

from app import create_app
from decouple import config

# from config import config_dict

from app.config import Config

# WARNING: Don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=True)

# # The configuration
# get_config_mode = 'Debug' if DEBUG else 'Production'

# try:
    
#     # Load the configuration using the default values 
#     app_config = config_dict[get_config_mode.capitalize()]

# except KeyError:
#     exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app()
app.config.from_object(Config)
# manager = Manager(app)
# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)

# @manager.command
# def run():
#     app.run()

if __name__ == '__main__':
    app.run(debug=True)
