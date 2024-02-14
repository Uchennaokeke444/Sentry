# Generated by Django 5.0.2 on 2024-02-14 22:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import sentry.db.models.fields.bounded
import sentry.db.models.fields.foreignkey
import sentry.db.models.fields.jsonfield
import sentry.db.models.fields.text
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
        ("sentry", "0645_backfill_add_uuid_to_all_rule_actions"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationMessage",
            fields=[
                (
                    "id",
                    sentry.db.models.fields.bounded.BoundedBigAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                ("error_details", sentry.db.models.fields.jsonfield.JSONField(null=True)),
                ("error_code", models.IntegerField(db_index=True, null=True)),
                (
                    "message_identifier",
                    sentry.db.models.fields.text.CharField(db_index=True, null=True),
                ),
                (
                    "rule_action_uuid",
                    sentry.db.models.fields.text.CharField(db_index=True, null=True),
                ),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "incident",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="sentry.incident"
                    ),
                ),
                (
                    "parent_notification_message",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sentry.notificationmessage",
                    ),
                ),
                (
                    "rule_fire_history",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sentry.rulefirehistory",
                    ),
                ),
                (
                    "trigger_action",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sentry.alertruletriggeraction",
                    ),
                ),
            ],
            options={
                "db_table": "sentry_notificationmessage",
            },
        ),
        migrations.AddConstraint(
            model_name="notificationmessage",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("incident__isnull", False),
                        ("trigger_action__isnull", False),
                        ("rule_action_uuid__isnull", True),
                        ("rule_fire_history__isnull", True),
                    ),
                    models.Q(
                        ("incident__isnull", True),
                        ("trigger_action__isnull", True),
                        ("rule_action_uuid__isnull", False),
                        ("rule_fire_history__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="notification_for_issue_xor_metric_alert",
            ),
        ),
    ]
