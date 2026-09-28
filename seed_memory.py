from hindsight_client import Hindsight

HINDSIGHT_URL = "http://localhost:8890"
BANK_ID = "fieldmind"

client = Hindsight(base_url=HINDSIGHT_URL)

incidents = [

    """
    Incident: Lakshmi Nagar Water Station pump failure.
    Cause: Repeated voltage fluctuations.
    Action taken: Motor was replaced.
    Outcome: Pump failed again after approximately 42 days.
    Lesson: Motor replacement alone did not solve the recurring problem.
    """,

    """
    Incident: Lakshmi Nagar Water Station pump failure.
    Cause: Voltage instability was observed before the failure.
    Action taken: Voltage stabilizer was repaired and electrical supply was inspected.
    Outcome: Pump operated normally for several months.
    Lesson: Stabilizing the electrical supply produced a longer-lasting solution.
    """,

    """
    Incident: Lakshmi Nagar Water Station low water pressure.
    Cause: Pump performance degraded after repeated electrical fluctuations.
    Action taken: Motor replacement was considered.
    Outcome: Previous motor-only intervention had resulted in another failure.
    Lesson: Check electrical stability before replacing the motor.
    """,

    """
    Incident: Kothapeta Substation transformer overheating.
    Cause: High load and inadequate cooling were suspected.
    Action taken: Cooling fans were inspected and load distribution was adjusted.
    Outcome: Temperature returned to normal.
    Lesson: Load and cooling conditions should be checked before replacing transformer components.
    """,

    """
    Incident: Kothapeta Substation transformer alarm.
    Cause: Transformer temperature increased during peak demand.
    Action taken: Load was temporarily redistributed and cooling was improved.
    Outcome: Alarm frequency decreased.
    Lesson: Peak-load conditions are an important indicator for transformer overheating.
    """,

    """
    Incident: Riverbank Road streetlight outage.
    Cause: Water entered an electrical junction box during heavy rain.
    Action taken: Junction box was sealed and damaged wiring was replaced.
    Outcome: Lights remained operational during subsequent rainfall.
    Lesson: Water ingress protection prevented repeated failures.
    """,

    """
    Incident: Riverbank Road streetlight outage.
    Cause: Several lights stopped working after heavy rainfall.
    Action taken: Individual bulbs were replaced.
    Outcome: Some lights failed again shortly afterward.
    Lesson: Replacing bulbs without checking the junction box did not address the underlying problem.
    """,

    """
    Incident: Central Pump Station pressure drop.
    Cause: Filter blockage reduced water flow.
    Action taken: Filter was cleaned and maintenance schedule was updated.
    Outcome: Pressure returned to normal.
    Lesson: Filter condition should be checked before replacing the pump.
    """
]

print("🧠 Loading FieldMind institutional memory...\n")

for i, incident in enumerate(incidents, 1):

    try:
        client.retain(
            bank_id=BANK_ID,
            content=incident,
            context="historical field operations incident"
        )

        print(f"✅ Memory {i} stored")

    except Exception as e:
        print(f"❌ Memory {i} failed: {e}")

client.close()

print("\n🎯 FieldMind memory seeding complete!")