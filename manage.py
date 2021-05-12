"""
registering blueprints of endpoints
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from Chatbotforwip import app, db
from Chatbotforwip.views import auth

app.register_blueprint(auth)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
