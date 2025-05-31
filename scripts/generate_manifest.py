import json
from pathlib import Path

# Paths relative to repository root
ROOT = Path(__file__).resolve().parents[1]
INTENTS_FILE = ROOT / 'agents' / 'prompt' / 'system_prompt' / 'intents.json'
OUTPUT_FILE = ROOT / 'capability_manifest.json'

# Human friendly descriptions per agent key
AGENT_INFO = {
    'onboarding': (
        'Onboarding & Baseline',
        'Connect accounts, parse bank/credit statements, and build your first net-worth snapshot.'
    ),
    'cash_flow': (
        'Cash-Flow & Budget',
        'Categorise your transactions and build a personalised budget.'
    ),
    'goal_setting': (
        'Goal-Setting',
        'Create and track SMART savings or investment goals.'
    ),
    'safety': (
        'Safety-Layer',
        'Flag suspicious activity and ensure account security.'
    ),
    'tax_pension': (
        'Tax & Pension Optimiser',
        'Recommend tax strategies and pension options.'
    ),
    'investment': (
        'Investment Architect',
        'Plan your investment portfolio.'
    ),
    'reporting': (
        'Reporting & Visualisation',
        'Create charts and reports from your finances.'
    ),
    'debt_strategy': (
        'Debt-Strategy',
        'Optimise debt repayments or consolidation.'
    ),
    'reminder_scheduler': (
        'Review & Reminder Scheduler',
        'Schedule periodic reviews and reminders.'
    ),
    'compliance_privacy': (
        'Compliance & Privacy',
        'Manage privacy requests and data compliance.'
    ),
    'conversation': (
        'Conversation',
        'General conversation and user guidance.'
    ),
}


def build_manifest() -> dict:
    """Return manifest dictionary built from intents.json and AGENT_INFO."""
    with open(INTENTS_FILE) as f:
        intents_map = json.load(f)

    agent_intents = {key: [] for key in AGENT_INFO}
    # intents.json maps intent -> {agent: FriendlyName}
    name_to_key = {info[0]: key for key, info in AGENT_INFO.items()}

    for intent, data in intents_map.items():
        name = data.get('agent')
        key = name_to_key.get(name)
        if key:
            agent_intents[key].append(intent)

    agents = []
    for key, (name, desc) in AGENT_INFO.items():
        agents.append({
            'key': key,
            'name': name,
            'intents': agent_intents.get(key, []),
            'user_friendly': desc,
        })

    return {'capability_version': 1, 'agents': agents}


def main() -> None:
    manifest = build_manifest()
    OUTPUT_FILE.write_text(json.dumps(manifest, indent=2))
    print(f'Wrote manifest to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
