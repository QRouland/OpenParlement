from flask.cli import AppGroup

db_cli = AppGroup('db', help='Database management commands.')
import commands.db.load
import commands.db.download
import commands.db.update