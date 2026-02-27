"""Basic usage examples for Voice Persona Engine."""

from persona import PersonaEngine, PersonaTraits


def example_preset_personas() -> None:
    """Demonstrate using preset personas."""
    print("=" * 60)
    print("EXAMPLE 1: Using Preset Personas")
    print("=" * 60)

    engine = PersonaEngine()

    # Create personas from presets
    friendly_host = engine.create_persona(
        name="friendly_host",
        traits=PersonaTraits.FRIENDLY_HOST,
    )
    analyst = engine.create_persona(
        name="analyst",
        traits=PersonaTraits.PROFESSIONAL_ANALYST,
    )

    # Sample text
    text = "Thank you for joining us today."

    # Apply different personas
    print(f"\nOriginal text: {text}")
    print(f"Friendly host version: {engine.apply_persona(text, friendly_host)}")
    print(f"Professional analyst version: {engine.apply_persona(text, analyst)}")


def example_custom_persona() -> None:
    """Demonstrate creating custom personas."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Creating Custom Personas")
    print("=" * 60)

    engine = PersonaEngine()

    # Create a custom persona with specific trait values
    tech_enthusiast = engine.create_persona(
        name="tech_enthusiast",
        traits=PersonaTraits(
            warmth=0.7,
            humor=0.75,
            formality=0.3,
            energy=0.85,
            empathy=0.6,
            assertiveness=0.7,
        ),
    )

    text = "Here is how machine learning works."
    transformed = engine.apply_persona(text, tech_enthusiast)

    print(f"\nOriginal: {text}")
    print(f"Tech Enthusiast: {transformed}")


def example_system_prompts() -> None:
    """Demonstrate generating system prompts for LLMs."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Generating System Prompts")
    print("=" * 60)

    engine = PersonaEngine()

    # Create personas and generate system prompts
    personas_to_demo = [
        ("friendly_host", PersonaTraits.FRIENDLY_HOST),
        ("analyst", PersonaTraits.PROFESSIONAL_ANALYST),
        ("mc", PersonaTraits.ENERGETIC_MC),
    ]

    for name, traits in personas_to_demo:
        persona = engine.create_persona(name, traits)
        system_prompt = engine.generate_system_prompt(persona)
        print(f"\n--- System Prompt for {name.upper()} ---")
        print(system_prompt[:300] + "...")  # Print first 300 chars


def example_blending() -> None:
    """Demonstrate blending personas."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Blending Personas")
    print("=" * 60)

    engine = PersonaEngine()

    # Create base personas
    friendly = engine.create_persona("friendly", PersonaTraits.FRIENDLY_HOST)
    professional = engine.create_persona("professional", PersonaTraits.PROFESSIONAL_ANALYST)

    # Blend them
    balanced = engine.blend_personas(
        friendly,
        professional,
        weight=0.6,
        save_as="balanced_host",
    )

    text = "Sales increased by 15% this quarter."

    print(f"\nOriginal text: {text}")
    print(f"Friendly version: {engine.apply_persona(text, friendly)}")
    print(f"Professional version: {engine.apply_persona(text, professional)}")
    print(f"Balanced version: {engine.apply_persona(text, balanced)}")


def example_persona_management() -> None:
    """Demonstrate persona management features."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Persona Management")
    print("=" * 60)

    engine = PersonaEngine()

    # Create multiple personas
    engine.create_persona("host", PersonaTraits.FRIENDLY_HOST)
    engine.create_persona("analyst", PersonaTraits.PROFESSIONAL_ANALYST)
    engine.create_persona("guide", PersonaTraits.CALM_GUIDE)

    # List all personas
    print(f"\nRegistered personas: {engine.list_personas()}")

    # Get info about a persona
    info = engine.get_persona_info("host")
    print(f"\nHost persona info:")
    print(f"  Name: {info['name']}")
    print(f"  Warmth: {info['traits']['warmth']}")
    print(f"  Energy: {info['traits']['energy']}")

    # Delete a persona
    engine.delete_persona("guide")
    print(f"\nAfter deletion: {engine.list_personas()}")


if __name__ == "__main__":
    example_preset_personas()
    example_custom_persona()
    example_system_prompts()
    example_blending()
    example_persona_management()
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
