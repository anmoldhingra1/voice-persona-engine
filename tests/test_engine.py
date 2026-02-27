"""Tests for PersonaEngine and Persona."""

import pytest

from persona import Persona, PersonaEngine, PersonaTraits


class TestPersona:
    """Tests for Persona dataclass."""

    def test_persona_creation(self):
        """Test creating a Persona instance."""
        traits = PersonaTraits(
            warmth=0.8, humor=0.6, formality=0.4, energy=0.7, empathy=0.9,
            assertiveness=0.5
        )
        persona = Persona(name="test_persona", traits=traits)

        assert persona.name == "test_persona"
        assert persona.traits == traits

    def test_persona_to_dict(self):
        """Test converting Persona to dictionary."""
        traits = PersonaTraits(
            warmth=0.8, humor=0.6, formality=0.4, energy=0.7, empathy=0.9,
            assertiveness=0.5
        )
        persona = Persona(name="test_persona", traits=traits)

        result = persona.to_dict()

        assert result["name"] == "test_persona"
        assert result["traits"]["warmth"] == 0.8
        assert result["traits"]["humor"] == 0.6
        assert result["traits"]["formality"] == 0.4
        assert result["traits"]["energy"] == 0.7
        assert result["traits"]["empathy"] == 0.9
        assert result["traits"]["assertiveness"] == 0.5

    def test_persona_to_dict_with_preset(self):
        """Test converting Persona with preset traits to dictionary."""
        persona = Persona(name="friendly_host", traits=PersonaTraits.FRIENDLY_HOST)

        result = persona.to_dict()

        assert result["name"] == "friendly_host"
        assert result["traits"]["warmth"] == 0.95


class TestPersonaEngineInit:
    """Tests for PersonaEngine initialization."""

    def test_engine_init(self, engine):
        """Test creating a PersonaEngine instance."""
        assert engine is not None
        assert isinstance(engine, PersonaEngine)
        assert engine.list_personas() == []


class TestCreatePersona:
    """Tests for PersonaEngine.create_persona method."""

    def test_create_persona_basic(self, engine, friendly_host_traits):
        """Test creating a persona."""
        persona = engine.create_persona("friendly_host", friendly_host_traits)

        assert persona.name == "friendly_host"
        assert persona.traits == friendly_host_traits

    def test_create_persona_registered(self, engine, friendly_host_traits):
        """Test that created persona is registered."""
        engine.create_persona("friendly_host", friendly_host_traits)

        assert "friendly_host" in engine.list_personas()

    def test_create_duplicate_raises_error(self, engine, friendly_host_traits):
        """Test that creating duplicate persona raises ValueError."""
        engine.create_persona("friendly_host", friendly_host_traits)

        with pytest.raises(
            ValueError, match="Persona 'friendly_host' already exists"
        ):
            engine.create_persona("friendly_host", friendly_host_traits)

    def test_create_duplicate_with_overwrite(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test that overwrite=True allows replacing persona."""
        engine.create_persona("test_persona", friendly_host_traits)
        persona = engine.create_persona(
            "test_persona", professional_analyst_traits, overwrite=True
        )

        assert persona.traits == professional_analyst_traits

    def test_create_multiple_personas(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test creating multiple personas."""
        engine.create_persona("friendly_host", friendly_host_traits)
        engine.create_persona("analyst", professional_analyst_traits)

        personas = engine.list_personas()
        assert len(personas) == 2
        assert "friendly_host" in personas
        assert "analyst" in personas


class TestGetPersona:
    """Tests for PersonaEngine.get_persona method."""

    def test_get_existing_persona(self, engine, friendly_host_traits):
        """Test retrieving an existing persona."""
        created = engine.create_persona("friendly_host", friendly_host_traits)
        retrieved = engine.get_persona("friendly_host")

        assert retrieved == created

    def test_get_nonexistent_persona(self, engine):
        """Test retrieving a nonexistent persona returns None."""
        result = engine.get_persona("nonexistent")

        assert result is None


class TestListPersonas:
    """Tests for PersonaEngine.list_personas method."""

    def test_list_empty(self, engine):
        """Test listing personas when none exist."""
        personas = engine.list_personas()

        assert personas == []

    def test_list_multiple(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test listing multiple personas."""
        engine.create_persona("friendly_host", friendly_host_traits)
        engine.create_persona("analyst", professional_analyst_traits)

        personas = engine.list_personas()

        assert len(personas) == 2
        assert set(personas) == {"friendly_host", "analyst"}


class TestDeletePersona:
    """Tests for PersonaEngine.delete_persona method."""

    def test_delete_existing_persona(self, engine, friendly_host_traits):
        """Test deleting an existing persona."""
        engine.create_persona("friendly_host", friendly_host_traits)
        result = engine.delete_persona("friendly_host")

        assert result is True
        assert engine.get_persona("friendly_host") is None

    def test_delete_nonexistent_persona(self, engine):
        """Test deleting a nonexistent persona returns False."""
        result = engine.delete_persona("nonexistent")

        assert result is False

    def test_delete_removes_from_list(self, engine, friendly_host_traits):
        """Test that delete removes persona from list."""
        engine.create_persona("friendly_host", friendly_host_traits)
        engine.delete_persona("friendly_host")

        assert "friendly_host" not in engine.list_personas()


class TestApplyPersona:
    """Tests for PersonaEngine.apply_persona method."""

    def test_apply_persona_no_enhance(self, engine, friendly_host_traits):
        """Test applying persona with enhance=False returns original text."""
        persona = engine.create_persona("friendly_host", friendly_host_traits)
        text = "Thank you for joining."
        result = engine.apply_persona(text, persona, enhance=False)

        assert result == text

    def test_apply_persona_high_energy(self, engine):
        """Test that high energy transforms punctuation."""
        traits = PersonaTraits(
            warmth=0.5, humor=0.5, formality=0.5, energy=0.9, empathy=0.5,
            assertiveness=0.5
        )
        persona = engine.create_persona("energetic", traits)
        text = "Thank you."
        result = engine.apply_persona(text, persona, enhance=True)

        assert "!" in result

    def test_apply_persona_low_energy(self, engine):
        """Test that low energy removes exclamation marks."""
        traits = PersonaTraits(
            warmth=0.5, humor=0.5, formality=0.5, energy=0.2, empathy=0.5,
            assertiveness=0.5
        )
        persona = engine.create_persona("calm", traits)
        text = "Thank you!"
        result = engine.apply_persona(text, persona, enhance=True)

        assert "!" not in result
        assert "." in result

    def test_apply_persona_high_warmth(self, engine):
        """Test that high warmth adds warm language."""
        traits = PersonaTraits(
            warmth=0.9, humor=0.5, formality=0.5, energy=0.5, empathy=0.5,
            assertiveness=0.5
        )
        persona = engine.create_persona("warm", traits)
        text = "Thank you for joining."
        result = engine.apply_persona(text, persona, enhance=True)

        assert len(result) > len(text)

    def test_apply_persona_low_formality(self, engine):
        """Test that low formality adds contractions."""
        traits = PersonaTraits(
            warmth=0.5, humor=0.5, formality=0.2, energy=0.5, empathy=0.5,
            assertiveness=0.5
        )
        persona = engine.create_persona("casual", traits)
        text = "I am happy. You are welcome."
        result = engine.apply_persona(text, persona, enhance=True)

        assert "I'm" in result or "you're" in result


class TestGenerateSystemPrompt:
    """Tests for PersonaEngine.generate_system_prompt method."""

    def test_generate_system_prompt(self, engine, friendly_host_traits):
        """Test generating a system prompt."""
        persona = engine.create_persona("friendly_host", friendly_host_traits)
        prompt = engine.generate_system_prompt(persona)

        assert isinstance(prompt, str)
        assert "You are an AI assistant" in prompt
        assert len(prompt) > 100

    def test_generate_different_prompts_for_different_personas(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test that different personas generate different prompts."""
        friendly = engine.create_persona("friendly", friendly_host_traits)
        analyst = engine.create_persona("analyst", professional_analyst_traits)

        friendly_prompt = engine.generate_system_prompt(friendly)
        analyst_prompt = engine.generate_system_prompt(analyst)

        assert friendly_prompt != analyst_prompt


class TestBlendPersonas:
    """Tests for PersonaEngine.blend_personas method."""

    def test_blend_equal_weight(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test blending two personas with equal weight."""
        friendly = engine.create_persona("friendly", friendly_host_traits)
        analyst = engine.create_persona("analyst", professional_analyst_traits)

        blended = engine.blend_personas(friendly, analyst, weight=0.5)

        assert blended.name == "friendly_blend_analyst"
        expected_warmth = (0.95 + 0.40) / 2
        assert abs(blended.traits.warmth - expected_warmth) < 0.001

    def test_blend_weight_toward_a(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test blending with weight favoring first persona."""
        friendly = engine.create_persona("friendly", friendly_host_traits)
        analyst = engine.create_persona("analyst", professional_analyst_traits)

        blended = engine.blend_personas(friendly, analyst, weight=0.8)

        expected_warmth = (0.95 * 0.8) + (0.40 * 0.2)
        assert abs(blended.traits.warmth - expected_warmth) < 0.001

    def test_blend_save_as(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test blending and saving with custom name."""
        friendly = engine.create_persona("friendly", friendly_host_traits)
        analyst = engine.create_persona("analyst", professional_analyst_traits)

        blended = engine.blend_personas(
            friendly, analyst, weight=0.5, save_as="friendly_analyst"
        )

        assert blended.name == "friendly_analyst"
        assert engine.get_persona("friendly_analyst") == blended

    def test_blend_not_saved_without_save_as(
        self, engine, friendly_host_traits, professional_analyst_traits
    ):
        """Test that blended persona not saved if save_as not provided."""
        friendly = engine.create_persona("friendly", friendly_host_traits)
        analyst = engine.create_persona("analyst", professional_analyst_traits)

        blended = engine.blend_personas(friendly, analyst, weight=0.5)

        assert blended.name not in engine.list_personas()


class TestGetPersonaInfo:
    """Tests for PersonaEngine.get_persona_info method."""

    def test_get_persona_info_existing(self, engine, friendly_host_traits):
        """Test getting info for existing persona."""
        engine.create_persona("friendly_host", friendly_host_traits)
        info = engine.get_persona_info("friendly_host")

        assert info is not None
        assert info["name"] == "friendly_host"
        assert info["traits"]["warmth"] == 0.95

    def test_get_persona_info_nonexistent(self, engine):
        """Test getting info for nonexistent persona returns None."""
        info = engine.get_persona_info("nonexistent")

        assert info is None

    def test_get_persona_info_structure(self, engine, custom_traits):
        """Test that persona info has correct structure."""
        engine.create_persona("custom", custom_traits)
        info = engine.get_persona_info("custom")

        assert "name" in info
        assert "traits" in info
        assert all(
            trait in info["traits"]
            for trait in [
                "warmth", "humor", "formality", "energy", "empathy",
                "assertiveness"
            ]
        )


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow(self, engine):
        """Test a complete workflow: create, apply, blend, prompt."""
        friendly = engine.create_persona("friendly", PersonaTraits.FRIENDLY_HOST)
        analyst = engine.create_persona("analyst", PersonaTraits.PROFESSIONAL_ANALYST)

        text = "Thank you for the data. Sales were strong."
        friendly_text = engine.apply_persona(text, friendly)
        assert len(friendly_text) > len(text)

        blended = engine.blend_personas(
            friendly, analyst, weight=0.6, save_as="friendly_analyst"
        )

        prompt = engine.generate_system_prompt(blended)
        assert "You are an AI assistant" in prompt

        assert len(engine.list_personas()) == 3
        assert engine.get_persona("friendly_analyst") is not None

    def test_create_apply_delete_cycle(self, engine, friendly_host_traits):
        """Test creating, applying, and deleting a persona."""
        persona = engine.create_persona("temp", friendly_host_traits)

        result = engine.apply_persona("Test text.", persona)
        assert result is not None

        deleted = engine.delete_persona("temp")
        assert deleted is True
        assert engine.get_persona("temp") is None
