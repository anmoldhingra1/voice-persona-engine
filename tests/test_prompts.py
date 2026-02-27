"""Tests for prompt generation and modifiers."""


from persona.prompts import (
    build_system_prompt,
    get_assertiveness_descriptor,
    get_empathy_descriptor,
    get_energy_descriptor,
    get_formality_descriptor,
    get_humor_descriptor,
    get_text_modifiers,
    get_warmth_descriptor,
)


class TestWarmthDescriptor:
    """Tests for get_warmth_descriptor function."""

    def test_very_cold(self):
        """Test descriptor for very low warmth."""
        result = get_warmth_descriptor(0.1)
        assert result == "professional and distant"

    def test_cold(self):
        """Test descriptor for low warmth."""
        result = get_warmth_descriptor(0.3)
        assert result == "professional and courteous"

    def test_neutral(self):
        """Test descriptor for neutral warmth."""
        result = get_warmth_descriptor(0.5)
        assert result == "friendly and approachable"

    def test_warm(self):
        """Test descriptor for high warmth."""
        result = get_warmth_descriptor(0.7)
        assert result == "warm and welcoming"

    def test_very_warm(self):
        """Test descriptor for very high warmth."""
        result = get_warmth_descriptor(0.95)
        assert result == "exceptionally warm and affectionate"


class TestHumorDescriptor:
    """Tests for get_humor_descriptor function."""

    def test_no_humor(self):
        """Test descriptor for no humor."""
        result = get_humor_descriptor(0.1)
        assert result == "avoid humor"

    def test_light_humor(self):
        """Test descriptor for light humor."""
        result = get_humor_descriptor(0.3)
        assert result == "occasional light humor"

    def test_natural_humor(self):
        """Test descriptor for natural humor."""
        result = get_humor_descriptor(0.5)
        assert result == "natural, conversational humor"

    def test_witty(self):
        """Test descriptor for witty humor."""
        result = get_humor_descriptor(0.7)
        assert result == "regular witty remarks and clever observations"

    def test_very_funny(self):
        """Test descriptor for very high humor."""
        result = get_humor_descriptor(0.9)
        assert result == "frequent humor and comedic timing"


class TestFormalityDescriptor:
    """Tests for get_formality_descriptor function."""

    def test_very_casual(self):
        """Test descriptor for very low formality."""
        result = get_formality_descriptor(0.1)
        assert result == "very casual, conversational tone"

    def test_casual(self):
        """Test descriptor for low formality."""
        result = get_formality_descriptor(0.3)
        assert result == "casual and conversational"

    def test_balanced(self):
        """Test descriptor for balanced formality."""
        result = get_formality_descriptor(0.5)
        assert result == "balanced professional and conversational"

    def test_formal(self):
        """Test descriptor for high formality."""
        result = get_formality_descriptor(0.7)
        assert result == "formal and professional"

    def test_very_formal(self):
        """Test descriptor for very high formality."""
        result = get_formality_descriptor(0.95)
        assert result == "highly formal and academic"


class TestEnergyDescriptor:
    """Tests for get_energy_descriptor function."""

    def test_very_calm(self):
        """Test descriptor for very low energy."""
        result = get_energy_descriptor(0.1)
        assert result == "calm, measured, and deliberate"

    def test_relaxed(self):
        """Test descriptor for low energy."""
        result = get_energy_descriptor(0.3)
        assert result == "relaxed and steady"

    def test_engaged(self):
        """Test descriptor for medium energy."""
        result = get_energy_descriptor(0.5)
        assert result == "naturally engaged and present"

    def test_enthusiastic(self):
        """Test descriptor for high energy."""
        result = get_energy_descriptor(0.7)
        assert result == "enthusiastic and dynamic"

    def test_very_energetic(self):
        """Test descriptor for very high energy."""
        result = get_energy_descriptor(0.95)
        assert result == "exceptionally vibrant and energetic"


class TestEmpathyDescriptor:
    """Tests for get_empathy_descriptor function."""

    def test_objective(self):
        """Test descriptor for very low empathy."""
        result = get_empathy_descriptor(0.1)
        assert result == "objective and neutral"

    def test_respectful(self):
        """Test descriptor for low empathy."""
        result = get_empathy_descriptor(0.3)
        assert result == "respectful and aware of audience needs"

    def test_emotionally_intelligent(self):
        """Test descriptor for medium empathy."""
        result = get_empathy_descriptor(0.5)
        assert result == "emotionally intelligent and attentive"

    def test_deeply_empathetic(self):
        """Test descriptor for high empathy."""
        result = get_empathy_descriptor(0.7)
        assert result == "deeply empathetic and emotionally tuned"

    def test_exceptionally_empathetic(self):
        """Test descriptor for very high empathy."""
        result = get_empathy_descriptor(0.95)
        assert result == "exceptionally empathetic and emotionally attuned"


class TestAssertivenessDescriptor:
    """Tests for get_assertiveness_descriptor function."""

    def test_tentative(self):
        """Test descriptor for very low assertiveness."""
        result = get_assertiveness_descriptor(0.1)
        assert result == "tentative and deferential"

    def test_suggestive(self):
        """Test descriptor for low assertiveness."""
        result = get_assertiveness_descriptor(0.3)
        assert result == "respectfully suggestive"

    def test_confident(self):
        """Test descriptor for medium assertiveness."""
        result = get_assertiveness_descriptor(0.5)
        assert result == "confidently informative"

    def test_direct(self):
        """Test descriptor for high assertiveness."""
        result = get_assertiveness_descriptor(0.7)
        assert result == "direct and commanding"

    def test_highly_assertive(self):
        """Test descriptor for very high assertiveness."""
        result = get_assertiveness_descriptor(0.95)
        assert result == "highly assertive and authoritative"


class TestBuildSystemPrompt:
    """Tests for build_system_prompt function."""

    def test_neutral_prompt(self):
        """Test building a system prompt with neutral traits."""
        prompt = build_system_prompt(
            warmth=0.5,
            humor=0.5,
            formality=0.5,
            energy=0.5,
            empathy=0.5,
            assertiveness=0.5,
        )

        assert isinstance(prompt, str)
        assert "You are an AI assistant" in prompt
        assert "Communication Style" in prompt
        assert "Interpersonal Approach" in prompt
        assert "Guidelines" in prompt

    def test_warm_energetic_prompt(self):
        """Test building a prompt with warm, energetic traits."""
        prompt = build_system_prompt(
            warmth=0.95,
            humor=0.9,
            formality=0.2,
            energy=1.0,
            empathy=0.85,
            assertiveness=0.8,
        )

        assert "exceptionally warm and affectionate" in prompt
        assert "frequent humor and comedic timing" in prompt
        assert "casual" in prompt
        assert "exceptionally vibrant and energetic" in prompt

    def test_cold_formal_prompt(self):
        """Test building a prompt with cold, formal traits."""
        prompt = build_system_prompt(
            warmth=0.1,
            humor=0.1,
            formality=0.95,
            energy=0.2,
            empathy=0.1,
            assertiveness=0.6,
        )

        assert "professional and distant" in prompt
        assert "avoid humor" in prompt
        assert "highly formal and academic" in prompt


class TestGetTextModifiers:
    """Tests for get_text_modifiers function."""

    def test_neutral_modifiers(self):
        """Test getting modifiers with neutral traits."""
        modifiers = get_text_modifiers(
            warmth=0.5,
            humor=0.5,
            formality=0.5,
            energy=0.5,
            empathy=0.5,
            assertiveness=0.5,
        )

        assert isinstance(modifiers, dict)
        assert "warmth_intensifiers" in modifiers
        assert "warmth_qualifiers" in modifiers
        assert "humor_additions" in modifiers
        assert "formality_contractions" in modifiers
        assert "energy_intensifiers" in modifiers
        assert "energy_qualifiers" in modifiers
        assert "empathy_phrases" in modifiers
        assert "assertiveness_qualifiers" in modifiers
        assert "assertiveness_imperatives" in modifiers

    def test_warm_modifiers(self):
        """Test modifiers with high warmth."""
        modifiers = get_text_modifiers(
            warmth=0.8,
            humor=0.5,
            formality=0.5,
            energy=0.5,
            empathy=0.5,
            assertiveness=0.5,
        )

        assert len(modifiers["warmth_intensifiers"]) > 0
        assert "really" in modifiers["warmth_intensifiers"]
        assert len(modifiers["warmth_qualifiers"]) > 0

    def test_high_energy_modifiers(self):
        """Test modifiers with high energy."""
        modifiers = get_text_modifiers(
            warmth=0.5,
            humor=0.5,
            formality=0.5,
            energy=0.8,
            empathy=0.5,
            assertiveness=0.5,
        )

        assert len(modifiers["energy_intensifiers"]) > 0
        assert "absolutely" in modifiers["energy_intensifiers"]

    def test_low_energy_modifiers(self):
        """Test modifiers with low energy."""
        modifiers = get_text_modifiers(
            warmth=0.5,
            humor=0.5,
            formality=0.5,
            energy=0.2,
            empathy=0.5,
            assertiveness=0.5,
        )

        assert len(modifiers["energy_qualifiers"]) > 0
        assert "quietly" in modifiers["energy_qualifiers"]

    def test_high_empathy_modifiers(self):
        """Test modifiers with high empathy."""
        modifiers = get_text_modifiers(
            warmth=0.5,
            humor=0.5,
            formality=0.5,
            energy=0.5,
            empathy=0.8,
            assertiveness=0.5,
        )

        assert len(modifiers["empathy_phrases"]) > 0
        assert "I understand" in modifiers["empathy_phrases"]

    def test_low_assertiveness_modifiers(self):
        """Test modifiers with low assertiveness."""
        modifiers = get_text_modifiers(
            warmth=0.5,
            humor=0.5,
            formality=0.5,
            energy=0.5,
            empathy=0.5,
            assertiveness=0.2,
        )

        assert len(modifiers["assertiveness_qualifiers"]) > 0
        assert "perhaps" in modifiers["assertiveness_qualifiers"]

    def test_high_assertiveness_modifiers(self):
        """Test modifiers with high assertiveness."""
        modifiers = get_text_modifiers(
            warmth=0.5,
            humor=0.5,
            formality=0.5,
            energy=0.5,
            empathy=0.5,
            assertiveness=0.8,
        )

        assert len(modifiers["assertiveness_imperatives"]) > 0
