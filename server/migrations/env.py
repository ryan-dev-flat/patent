import sys
from pathlib import Path

# Append the project directory to sys.path to make sure `app` is importable.
# This assumes `env.py` is located in `patent/server/migrations` and `app.py` is in `patent/server`.
sys.path.append(str(Path(__file__).resolve().parents[1]))

import logging
from logging.config import fileConfig

from app import create_app  # Import the application factory function

from flask import current_app

from alembic import context

# Create the Flask app and push the application context
app = create_app()  # Adjust this if create_app needs any arguments

with app.app_context():  # Start the application context

    # Access Alembic's config object, which provides access to .ini values
    config = context.config

    # Configure logging
    fileConfig(config.config_file_name)
    logger = logging.getLogger('alembic.env')

    # Add your engine and URL functions within the context
    def get_engine():
        try:
            return current_app.extensions['migrate'].db.get_engine()
        except (TypeError, AttributeError):
            return current_app.extensions['migrate'].db.engine

    def get_engine_url():
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    config.set_main_option('sqlalchemy.url', get_engine_url())


    # Set the sqlalchemy.url in Alembic configuration
    config.set_main_option('sqlalchemy.url', get_engine_url())
    target_db = current_app.extensions['migrate'].db

    def get_metadata():
        if hasattr(target_db, 'metadatas'):
            return target_db.metadatas[None]
        return target_db.metadata

    # Run migrations in 'offline' mode
    def run_migrations_offline():
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url, target_metadata=get_metadata(), literal_binds=True
        )

        with context.begin_transaction():
            context.run_migrations()

    # Run migrations in 'online' mode
    def run_migrations_online():
        def process_revision_directives(context, revision, directives):
            if getattr(config.cmd_opts, 'autogenerate', False):
                script = directives[0]
                if script.upgrade_ops.is_empty():
                    directives[:] = []
                    logger.info('No changes in schema detected.')

        conf_args = current_app.extensions['migrate'].configure_args
        if conf_args.get("process_revision_directives") is None:
            conf_args["process_revision_directives"] = process_revision_directives

        connectable = get_engine()

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=get_metadata(),
                **conf_args
            )

            with context.begin_transaction():
                context.run_migrations()

    # Determine migration mode and run accordingly
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
