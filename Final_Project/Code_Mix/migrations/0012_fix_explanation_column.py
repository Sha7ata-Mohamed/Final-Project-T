from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Code_Mix', '0011_useranswer_user'),  # Make sure this matches your latest migration
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            SELECT 1 FROM pragma_table_info('Code_Mix_options') WHERE name='explanation';
            """,
            reverse_sql="SELECT 1;",
        ),
        migrations.RunSQL(
            sql="""
            ALTER TABLE Code_Mix_options ADD COLUMN explanation TEXT NULL;
            """,
            reverse_sql="""
            ALTER TABLE Code_Mix_options DROP COLUMN explanation;
            """,
            state_operations=[
                migrations.AddField(
                    model_name='options',
                    name='explanation',
                    field=models.TextField(blank=True, null=True),
                ),
            ]
        ),
    ]