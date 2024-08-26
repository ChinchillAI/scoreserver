from alembic.operations.ops import MigrationScript
from alembic.runtime.migration import MigrationContext
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic import context
from collections.abc import Iterable

# Note these imports must not be relative!
from scoreserver.models import SQLModel  # pyright: ignore[reportPrivateLocalImportUsage]
from scoreserver.core.config import settings


config = context.config
fileConfig(config.config_file_name)  # pyright: ignore[reportArgumentType]
target_metadata = SQLModel.metadata


def get_url():
    return str(settings.SQLALCHEMY_DATABASE_URI)


def process_revision_directives(
    context: MigrationContext,
    revision: str | Iterable[str | None] | Iterable[str],
    directives: list[MigrationScript],
) -> None:
    if config.cmd_opts.autogenerate:  # pyright: ignore[reportAny,reportOptionalMemberAccess]
        script = directives[0]
        if script.upgrade_ops.is_empty():  # pyright: ignore[reportOptionalMemberAccess]
            directives[:] = []
            print("No changes in schema detected.")


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()  # pyright: ignore[reportOptionalSubscript]
    connectable = engine_from_config(
        configuration,  # pyright: ignore[reportArgumentType]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
