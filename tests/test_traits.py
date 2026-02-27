"""Tests for PersonaTraits."""

import pytest

from persona.traits import PersonaTraits


class TestPersonaTraitsInit:
    """Tests for PersonaTraits initialization and validation."""

    def test_default_traits(self):
        """Test that default traits are all 0.5."""
        traits = PersonaTraits()
        assert traits.warmth == 0.5
        assert traits.humor == 0.5
        assert traits.formality == 0.5
        assert traits.energy == 0.5
        assert traits.empathy == 0.5
        assert traits.assertiveness == 0.5

    def test_custom_traits(self):
        """Test creating traits with custom values."""
        traits = PersonaTraits(
            warmth=0.8,
            humor=0.2,
            formality=0.9,
            energy=0.4,
            empathy=0.7,
            assertiveness=0.6,
        )
        assert traits.warmth == 0.8
        assert traits.humor == 0.2
        assert traits.formality == 0.9
        assert traits.energy == 0.4
        assert traits.empathy == 0.7
        assert traits.assertiveness == 0.6

    def test_invalid_warmth_too_low(self):
        """Test that warmth < 0.0 raises ValueError."""
        with pytest.raises(ValueError, match="warmth must be between 0.0 and 1.0"):
            PersonaTraits(warmth=-0.1)

    def test_invalid_warmth_too_high(self):
        """Test that warmth > 1.0 raises ValueError."""
        with pytest.raises(ValueError, match="warmth must be between 0.0 and 1.0"):
            PersonaTraits(warmth=1.1)

    def test_invalid_humor(self):
        """Test that invalid humor raises ValueError."""
        with pytest.raises(ValueError, match="humor must be between 0.0 and 1.0"):
            PersonaTraits(humor=2.0)

    def test_invalid_formality(self):
        """Test that invalid formality raises ValueError."""
        with pytest.raises(ValueError, match="formality must be between 0.0 and 1.0"):
            PersonaTraits(formality=-0.5)

    def test_invalid_energy(self):
        """Test that invalid energy raises ValueError."""
        with pytest.raises(ValueError, match="energy must be between 0.0 and 1.0"):
            PersonaTraits(energy=1.5)

    def test_invalid_empathy(self):
        """Test that invalid empathy raises ValueError."""
        with pytest.raises(ValueError, match="empathy must be between 0.0 and 1.0"):
            PersonaTraits(empathy=-1.0)

    def test_invalid_assertiveness(self):
        """Test that invalid assertiveness raises ValueError."""
        with pytest.raises(
            ValueError, match="assertiveness must be between 0.0 and 1.0"
        ):
            PersonaTraits(assertiveness=2.5)

    def test_boundary_values(self):
        """Test that boundary values 0.0 and 1.0 are valid."""
        traits = PersonaTraits(
            warmth=0.0,
            humor=1.0,
            formality=0.0,
            energy=1.0,
            empathy=0.0,
            assertiveness=1.0,
        )
        assert traits.warmth == 0.0
        assert traits.humor == 1.0


class TestBlend:
    """Tests for PersonaTraits.blend method."""

    def test_blend_equal_weight(self):
        """Test blending two trait sets with equal weight (0.5)."""
        traits_a = PersonaTraits(
            warmth=0.8, humor=0.6, formality=0.4, energy=0.8, empathy=0.9,
            assertiveness=0.5
        )
        traits_b = PersonaTraits(
            warmth=0.2, humor=0.4, formality=0.6, energy=0.2, empathy=0.1,
            assertiveness=0.5
        )

        blended = traits_a.blend(traits_b, weight=0.5)

        assert blended.warmth == 0.5
        assert blended.humor == 0.5
        assert blended.formality == 0.5
        assert blended.energy == 0.5
        assert blended.empathy == 0.5
        assert blended.assertiveness == 0.5

    def test_blend_weight_toward_a(self):
        """Test blending with weight favoring traits_a."""
        traits_a = PersonaTraits(
            warmth=1.0, humor=1.0, formality=1.0, energy=1.0, empathy=1.0,
            assertiveness=1.0
        )
        traits_b = PersonaTraits(
            warmth=0.0, humor=0.0, formality=0.0, energy=0.0, empathy=0.0,
            assertiveness=0.0
        )

        blended = traits_a.blend(traits_b, weight=0.8)

        assert blended.warmth == 0.8
        assert blended.humor == 0.8
        assert blended.formality == 0.8
        assert blended.energy == 0.8
        assert blended.empathy == 0.8
        assert blended.assertiveness == 0.8

    def test_blend_weight_toward_b(self):
        """Test blending with weight favoring traits_b."""
        traits_a = PersonaTraits(
            warmth=1.0, humor=1.0, formality=1.0, energy=1.0, empathy=1.0,
            assertiveness=1.0
        )
        traits_b = PersonaTraits(
            warmth=0.0, humor=0.0, formality=0.0, energy=0.0, empathy=0.0,
            assertiveness=0.0
        )

        blended = traits_a.blend(traits_b, weight=0.2)

        assert blended.warmth == 0.2
        assert blended.humor == 0.2
        assert blended.formality == 0.2
        assert blended.energy == 0.2
        assert blended.empathy == 0.2
        assert blended.assertiveness == 0.2

    def test_blend_invalid_weight_too_low(self):
        """Test that blend with weight < 0.0 raises ValueError."""
        traits_a = PersonaTraits()
        traits_b = PersonaTraits()

        with pytest.raises(ValueError, match="weight must be between 0.0 and 1.0"):
            traits_a.blend(traits_b, weight=-0.1)

    def test_blend_invalid_weight_too_high(self):
        """Test that blend with weight > 1.0 raises ValueError."""
        traits_a = PersonaTraits()
        traits_b = PersonaTraits()

        with pytest.raises(ValueError, match="weight must be between 0.0 and 1.0"):
            traits_a.blend(traits_b, weight=1.1)

    def test_blend_weight_zero(self):
        """Test blending with weight=0.0 (all traits_b)."""
        traits_a = PersonaTraits(
            warmth=0.8, humor=0.6, formality=0.4, energy=0.8, empathy=0.9,
            assertiveness=0.5
        )
        traits_b = PersonaTraits(
            warmth=0.2, humor=0.4, formality=0.6, energy=0.2, empathy=0.1,
            assertiveness=0.5
        )

        blended = traits_a.blend(traits_b, weight=0.0)

        assert blended.warmth == traits_b.warmth
        assert blended.humor == traits_b.humor
        assert blended.formality == traits_b.formality
        assert blended.energy == traits_b.energy
        assert blended.empathy == traits_b.empathy
        assert blended.assertiveness == traits_b.assertiveness

    def test_blend_weight_one(self):
        """Test blending with weight=1.0 (all traits_a)."""
        traits_a = PersonaTraits(
            warmth=0.8, humor=0.6, formality=0.4, energy=0.8, empathy=0.9,
            assertiveness=0.5
        )
        traits_b = PersonaTraits(
            warmth=0.2, humor=0.4, formality=0.6, energy=0.2, empathy=0.1,
            assertiveness=0.5
        )

        blended = traits_a.blend(traits_b, weight=1.0)

        assert blended.warmth == traits_a.warmth
        assert blended.humor == traits_a.humor
        assert blended.formality == traits_a.formality
        assert blended.energy == traits_a.energy
        assert blended.empathy == traits_a.empathy
        assert blended.assertiveness == traits_a.assertiveness


class TestFromDict:
    """Tests for PersonaTraits.from_dict method."""

    def test_from_dict_all_fields(self):
        """Test creating traits from a complete dictionary."""
        data = {
            "warmth": 0.7,
            "humor": 0.3,
            "formality": 0.6,
            "energy": 0.8,
            "empathy": 0.4,
            "assertiveness": 0.9,
        }
        traits = PersonaTraits.from_dict(data)

        assert traits.warmth == 0.7
        assert traits.humor == 0.3
        assert traits.formality == 0.6
        assert traits.energy == 0.8
        assert traits.empathy == 0.4
        assert traits.assertiveness == 0.9

    def test_from_dict_partial_fields(self):
        """Test creating traits from a partial dictionary (uses defaults)."""
        data = {"warmth": 0.9, "humor": 0.1}
        traits = PersonaTraits.from_dict(data)

        assert traits.warmth == 0.9
        assert traits.humor == 0.1
        assert traits.formality == 0.5
        assert traits.energy == 0.5
        assert traits.empathy == 0.5
        assert traits.assertiveness == 0.5

    def test_from_dict_empty(self):
        """Test creating traits from empty dictionary (all defaults)."""
        traits = PersonaTraits.from_dict({})

        assert traits.warmth == 0.5
        assert traits.humor == 0.5
        assert traits.formality == 0.5
        assert traits.energy == 0.5
        assert traits.empathy == 0.5
        assert traits.assertiveness == 0.5

    def test_from_dict_extra_fields_ignored(self):
        """Test that extra fields in dict are ignored."""
        data = {
            "warmth": 0.6,
            "humor": 0.4,
            "extra_field": "should be ignored",
            "another_extra": 123,
        }
        traits = PersonaTraits.from_dict(data)

        assert traits.warmth == 0.6
        assert traits.humor == 0.4


class TestPresets:
    """Tests for preset persona traits."""

    def test_friendly_host_preset(self):
        """Test FRIENDLY_HOST preset values."""
        assert PersonaTraits.FRIENDLY_HOST.warmth == 0.95
        assert PersonaTraits.FRIENDLY_HOST.humor == 0.80
        assert PersonaTraits.FRIENDLY_HOST.formality == 0.30
        assert PersonaTraits.FRIENDLY_HOST.energy == 0.90
        assert PersonaTraits.FRIENDLY_HOST.empathy == 0.85
        assert PersonaTraits.FRIENDLY_HOST.assertiveness == 0.55

    def test_professional_analyst_preset(self):
        """Test PROFESSIONAL_ANALYST preset values."""
        assert PersonaTraits.PROFESSIONAL_ANALYST.warmth == 0.40
        assert PersonaTraits.PROFESSIONAL_ANALYST.humor == 0.20
        assert PersonaTraits.PROFESSIONAL_ANALYST.formality == 0.95
        assert PersonaTraits.PROFESSIONAL_ANALYST.energy == 0.50
        assert PersonaTraits.PROFESSIONAL_ANALYST.empathy == 0.55
        assert PersonaTraits.PROFESSIONAL_ANALYST.assertiveness == 0.75

    def test_energetic_mc_preset(self):
        """Test ENERGETIC_MC preset values."""
        assert PersonaTraits.ENERGETIC_MC.warmth == 0.85
        assert PersonaTraits.ENERGETIC_MC.humor == 0.90
        assert PersonaTraits.ENERGETIC_MC.formality == 0.20
        assert PersonaTraits.ENERGETIC_MC.energy == 1.00
        assert PersonaTraits.ENERGETIC_MC.empathy == 0.70
        assert PersonaTraits.ENERGETIC_MC.assertiveness == 0.85

    def test_calm_guide_preset(self):
        """Test CALM_GUIDE preset values."""
        assert PersonaTraits.CALM_GUIDE.warmth == 0.80
        assert PersonaTraits.CALM_GUIDE.humor == 0.30
        assert PersonaTraits.CALM_GUIDE.formality == 0.60
        assert PersonaTraits.CALM_GUIDE.energy == 0.40
        assert PersonaTraits.CALM_GUIDE.empathy == 0.95
        assert PersonaTraits.CALM_GUIDE.assertiveness == 0.35
