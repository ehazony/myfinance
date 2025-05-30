from django.db import migrations
import json
from pathlib import Path

def load_intents(apps, schema_editor):
    Intent = apps.get_model('app', 'OrchestratorIntent')
    intents_path = Path(__file__).resolve().parent.parent.parent / 'agents' / 'prompt' / 'system_prompt' / 'intents.json'
    with open(intents_path) as f:
        data = json.load(f)
    for key, info in data.items():
        Intent.objects.update_or_create(key=key, defaults={'agent': info['agent']})

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0002_orchestrator_intents'),
    ]

    operations = [
        migrations.RunPython(load_intents, migrations.RunPython.noop),
    ]
