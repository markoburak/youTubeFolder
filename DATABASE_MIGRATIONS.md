# Database migrations

This project uses Flask-Migrate, which integrates Alembic with Flask-SQLAlchemy.
Migration files in `migrations/versions/` are part of the application and must be
committed and deployed with the code.

## Database selection

The application chooses its database in this order:

1. `DATABASE_URL`, when set.
2. The production `DB_HOST`, `DB_NAME`, `DB_USERNAME`, and `DB_PASSWORD`
   variables, when all four are set.
3. The local MySQL settings in `config_file/config.py`.

Use a SQLAlchemy URL for `DATABASE_URL`, for example:

```text
mysql+mysqlconnector://username:password@hostname/database?charset=utf8mb4
```

Always confirm the target before running a migration:

```powershell
.\Scripts\flask.exe --app main db current
```

## One-time adoption for an existing database

Back up the database first. `stamp` records which schema version already exists;
it does not execute schema changes.

### Existing database without the `is_priority` column

This is the expected production adoption path if the priority feature has not
been deployed yet:

```powershell
.\Scripts\flask.exe --app main db stamp 0001_initial
.\Scripts\flask.exe --app main db upgrade
```

The first command marks the existing tables as the initial schema. The second
command applies revision `0002_priority`, adding `is_priority` without deleting
or recreating any table or row.

### Existing database that already has the `is_priority` column

The local database was upgraded manually while this feature was developed, so
it already matches the current migration head. Adopt it with:

```powershell
.\Scripts\flask.exe --app main db stamp 0003_lowercase_tables
.\Scripts\flask.exe --app main db upgrade
```

Do not run `upgrade` from `0001_initial` on a database where `is_priority`
already exists, because that would try to add the column a second time.

Revision `0003_lowercase_tables` also normalizes the two legacy mixed-case table
names on case-sensitive MySQL servers. On Windows MySQL, where the names are
already stored lowercase, that revision safely performs no rename.

The following upgrade applies revision `0004_category_emoji_text`, which brings
the older `category.emoji` column in line with the current `TEXT` model type.

### Brand-new empty database

No stamp is needed:

```powershell
.\Scripts\flask.exe --app main db upgrade
```

Alembic will create the initial tables and apply every later revision in order.

## Normal development workflow

After changing a SQLAlchemy model:

```powershell
.\Scripts\flask.exe --app main db migrate -m "describe the schema change"
.\Scripts\flask.exe --app main db upgrade
.\Scripts\flask.exe --app main db check
```

Review every generated revision before applying or committing it. Autogenerate
is helpful, but it cannot detect every kind of database change.

## Normal deployment workflow

1. Back up the production database.
2. Deploy the application and migration files.
3. Install dependencies with `pip install -r requirements.txt`.
4. Set the production database environment variables.
5. Run `flask --app main db current` and confirm the target revision.
6. Run `flask --app main db upgrade` before starting the new application code.

Never run `stamp` for routine deployments. It is only for the one-time adoption
of a database whose schema already exists outside Alembic's version history.
