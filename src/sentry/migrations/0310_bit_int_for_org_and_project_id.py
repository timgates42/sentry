# Generated by Django 2.2.28 on 2022-07-25 20:49

from django.db import migrations

import sentry.db.models.fields.bounded
from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production. For
    # the most part, this should only be used for operations where it's safe to run the migration
    # after your code has deployed. So this should not be used for most operations that alter the
    # schema of a table.
    # Here are some things that make sense to mark as dangerous:
    # - Large data migrations. Typically we want these to be run manually by ops so that they can
    #   be monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   have ops run this and not block the deploy. Note that while adding an index is a schema
    #   change, it's completely safe to run the operation after the code has deployed.

    # please don't preform database_operations as they already have been applied, they were added so the tests could run
    is_dangerous = True

    # This is set to false only as database_operations are going to be ignored by sentry saas. Please do not set checked
    # to false if you plan to alter the database
    checked = False

    # This flag is used to decide whether to run this migration in a transaction or not. Generally
    # we don't want to run in a transaction here, since for long running operations like data
    # back-fills this results in us locking an increasing number of rows until we finally commit.
    atomic = False

    dependencies = [
        ("sentry", "0309_fix_many_to_many_field"),
    ]

    operations = (
        migrations.AlterField(
            model_name="auditlogentry",
            name="target_object",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="commit",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="commitauthor",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="commitfilechange",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="deploy",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="distribution",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="environment",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(),
        ),
        migrations.AlterField(
            model_name="environment",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="eventuser",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="grouprelease",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="monitor",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="monitor",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="monitorcheckin",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="promptsactivity",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="promptsactivity",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="pullrequest",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="release",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="releasecommit",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="releasecommit",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="releaseenvironment",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="releasefile",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="releaseheadcommit",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="repository",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="servicehook",
            name="actor_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="servicehook",
            name="organization_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="servicehook",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="servicehookproject",
            name="project_id",
            field=sentry.db.models.fields.bounded.BoundedBigIntegerField(db_index=True),
        ),
        migrations.RunSQL(
            sql="ALTER TABLE sentry_externalissue ALTER COLUMN organization_id TYPE bigint",
            hints={"tables": ["sentry_externalissue"]},
            reverse_sql="ALTER TABLE sentry_externalissue ALTER COLUMN organization_id TYPE int",
        ),
        migrations.RunSQL(
            sql="ALTER TABLE sentry_externalissue ALTER COLUMN integration_id TYPE bigint",
            hints={"tables": ["sentry_externalissue"]},
            reverse_sql="ALTER TABLE sentry_externalissue ALTER COLUMN integration_id TYPE int",
        ),
    )
