# Voice Persona Engine

[![CI](https://github.com/anmoldhingra1/voice-persona-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/anmoldhingra1/voice-persona-engine/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Python framework for shaping consistent AI personas. Define personas with trait vectors, apply them to LLM outputs, and keep tone stable across generated responses.

## Overview

This is a small public slice of the Rerato orchestration thesis: voice and personality should be controlled as product primitives, not improvised in one-off prompts.

Voice Persona Engine enables you to:
- Define AI personas through configurable trait vectors (warmth, humor, formality, energy, empathy, assertiveness)
- Dynamically modulate LLM prompts based on persona configuration
- Generate system prompts tailored to your persona's personality
- Blend multiple personas for nuanced character expression
- Apply text transformations based on personality traits

Perfect for building AI hosts, voice assistants, chatbots, and content generation systems that require consistent personality.

## What It Shows

- Trait-vector persona modeling
- Prompt generation from structured persona state
- Persona blending for nuanced host behavior
- Text shaping for consistent tone experiments
- A simple API that can sit above any LLM provider

## Installation

```bash
git clone https://github.com/anmoldhingra1/voice-persona-engine.git
cd voice-persona-engine
pip install -e ".[dev]"
```

## Quick Start

```python
from persona import PersonaEngine, PersonaTraits

# Create an engine instance
engine = PersonaEngine()

# Use a preset persona
friendly_host = engine.create_persona(
    name="friendly_host",
    traits=PersonaTraits.FRIENDLY_HOST
)

# Apply to text
text = "Thank you for joining us today."
transformed = engine.apply_persona(text, friendly_host)
print(transformed)
# Output: "Oh, thank you so much for joining us today! We're thrilled to have you here."

# Generate a system prompt for your LLM
system_prompt = engine.generate_system_prompt(friendly_host)
print(system_prompt)
# Use with Claude, GPT-4, or other LLMs
```

## Features

### Six Personality Traits

Personas are defined using six dimensions, each ranging from 0.0 to 1.0:

- **Warmth**: How friendly and approachable (0.0=cold, 1.0=extremely warm)
- **Humor**: Level of wit and comedic timing (0.0=no humor, 1.0=very funny)
- **Formality**: Professional vs. casual language (0.0=casual, 1.0=formal)
- **Energy**: Enthusiasm and dynamism (0.0=lethargic, 1.0=highly energetic)
- **Empathy**: Emotional attunement to audience (0.0=detached, 1.0=deeply empathetic)
- **Assertiveness**: Confidence and directness (0.0=tentative, 1.0=highly assertive)

### Preset Personas

Four ready-to-use personas for common scenarios:

```python
from persona.traits import PersonaTraits

# Available presets
traits = PersonaTraits.FRIENDLY_HOST          # Warm, enthusiastic host
traits = PersonaTraits.PROFESSIONAL_ANALYST   # Measured, data-driven analyst
traits = PersonaTraits.ENERGETIC_MC           # High-energy master of ceremonies
traits = PersonaTraits.CALM_GUIDE             # Serene, empathetic guide
```

### Core API

#### PersonaEngine

```python
engine = PersonaEngine()

# Create personas
persona = engine.create_persona(name, traits, overwrite=False)

# Manage personas
retrieved = engine.get_persona(name)
all_names = engine.list_personas()
deleted = engine.delete_persona(name)

# Apply personalities
transformed = engine.apply_persona(text, persona, enhance=True)

# Generate prompts
prompt = engine.generate_system_prompt(persona)

# Blend personas
blended = engine.blend_personas(
    persona_a, persona_b, 
    weight=0.5,
    save_as="blended_name"
)

# Get info
info = engine.get_persona_info(name)
```

#### PersonaTraits

Create custom traits or use presets:

```python
# Defaults to all 0.5
traits = PersonaTraits()

# Custom traits
traits = PersonaTraits(
    warmth=0.9,
    humor=0.8,
    formality=0.3,
    energy=0.8,
    empathy=0.9,
    assertiveness=0.5
)

# From dictionary
traits = PersonaTraits.from_dict({
    "warmth": 0.8,
    "humor": 0.6,
})

# Blend traits
blended = traits_a.blend(traits_b, weight=0.6)
```

## Use Cases

### AI Podcast Host

```python
host = engine.create_persona(
    "podcast_host",
    PersonaTraits.FRIENDLY_HOST
)
system_prompt = engine.generate_system_prompt(host)
# Use with your LLM to generate podcast content
```

### Professional Analysis

```python
analyst = engine.create_persona(
    "analyst",
    PersonaTraits.PROFESSIONAL_ANALYST
)
analysis = engine.apply_persona(
    "Sales increased by 15% this quarter.",
    analyst
)
```

### Conversational Assistant

```python
# Create a balanced persona
assistant = engine.create_persona(
    "assistant",
    PersonaTraits(
        warmth=0.7, humor=0.5, formality=0.6,
        energy=0.6, empathy=0.8, assertiveness=0.5
    )
)
prompt = engine.generate_system_prompt(assistant)
```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Testing

Run the test suite:

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

Built by [Anmol Dhingra](https://github.com/anmoldhingra1), founder of [Rerato](https://trivana.ai).
