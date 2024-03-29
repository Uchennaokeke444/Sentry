# Generated by Django 2.2.28 on 2023-03-22 06:37

import django.db.models.deletion
from django.db import migrations

import sentry.db.models.fields.foreignkey
import sentry.db.models.fields.hybrid_cloud_foreign_key
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
    is_dangerous = False

    dependencies = [
        ("sentry", "0397_break_some_more_fks"),
    ]

    operations = [
        migrations.AddField(
            model_name="actor",
            name="team",
            field=sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="actor_from_team",
                to="sentry.Team",
                unique=False,
                db_index=False,
                db_constraint=False,
            ),
        ),
        migrations.AddField(
            model_name="actor",
            name="user_id",
            field=sentry.db.models.fields.hybrid_cloud_foreign_key.HybridCloudForeignKey(
                "sentry.User", on_delete="CASCADE", db_index=False, null=True, unique=False
            ),
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name="team",
                    name="actor",
                    field=sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_from_actor",
                        to="sentry.Actor",
                        unique=True,
                    ),
                ),
                migrations.AlterField(
                    model_name="user",
                    name="actor",
                    field=sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="user_from_actor",
                        to="sentry.Actor",
                        unique=True,
                    ),
                ),
                migrations.AlterField(
                    model_name="alertrule",
                    name="owner",
                    field=sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="sentry.Actor"
                    ),
                ),
            ],
        ),
    ]
