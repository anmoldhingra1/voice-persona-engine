"""Persona trait definitions and preset configurations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PersonaTraits:
    """
    Defines the personality dimensions for a persona.

    Each trait is a float between 0.0 and 1.0 that modulates the linguistic
    and stylistic characteristics of generated text.

    Attributes:
        warmth: How friendly and approachable (0.0=cold, 1.0=extremely warm)
        humor: Level of wit and comedic timing (0.0=no humor, 1.0=very funny)
        formality: Professional vs. casual language (0.0=casual, 1.0=formal)
        energy: Enthusiasm and dynamism (0.0=lethargic, 1.0=highly energetic)
        empathy: Emotional attunement to audience (0.0=detached, 1.0=deeply empathetic)
        assertiveness: Confidence and directness (0.0=tentative, 1.0=highly assertive)
    """

    warmth: float = 0.5
    humor: float = 0.5
    formality: float = 0.5
    energy: float = 0.5
    empathy: float = 0.5
    assertiveness: float = 0.5

    def __post_init__(self) -> None:
        """Validate that all traits are in the valid range."""
        traits = {
            "warmth": self.warmth,
            "humor": self.humor,
            "formality": self.formality,
            "energy": self.energy,
            "empathy": self.empathy,
            "assertiveness": self.assertiveness,
        }
        for name, value in traits.items():
            if not 0.0 <= value <= 1.0:
                msg = f"{name} must be between 0.0 and 1.0, got {value}"
                raise ValueError(msg)

    def blend(self, other: PersonaTraits, weight: float) -> PersonaTraits:
        """
        Blend two trait sets together.

        Args:
            other: The other PersonaTraits to blend with
            weight: Weight for this traits (0.0 = all other, 1.0 = all self)

        Returns:
            A new PersonaTraits with blended values

        Raises:
            ValueError: If weight is not between 0.0 and 1.0
        """
        if not 0.0 <= weight <= 1.0:
            msg = f"weight must be between 0.0 and 1.0, got {weight}"
            raise ValueError(msg)

        other_weight = 1.0 - weight
        return PersonaTraits(
            warmth=self.warmth * weight + other.warmth * other_weight,
            humor=self.humor * weight + other.humor * other_weight,
            formality=self.formality * weight + other.formality * other_weight,
            energy=self.energy * weight + other.energy * other_weight,
            empathy=self.empathy * weight + other.empathy * other_weight,
            assertiveness=self.assertiveness * weight
            + other.assertiveness * other_weight,
        )

    @classmethod
    def from_dict(cls, data: dict) -> PersonaTraits:
        """
        Create PersonaTraits from a dictionary.

        Args:
            data: Dictionary with trait keys and float values

        Returns:
            A new PersonaTraits instance
        """
        return cls(
            **{k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        )


# Preset personas for common use cases

PersonaTraits.FRIENDLY_HOST = PersonaTraits(
    warmth=0.95,
    humor=0.80,
    formality=0.30,
    energy=0.90,
    empathy=0.85,
    assertiveness=0.55,
)
"""A warm, enthusiastic host perfect for podcasts, streaming, or live presentations."""

PersonaTraits.PROFESSIONAL_ANALYST = PersonaTraits(
    warmth=0.40,
    humor=0.20,
    formality=0.95,
    energy=0.50,
    empathy=0.55,
    assertiveness=0.75,
)
"""A measured, data-driven analyst focused on accuracy and precision."""

PersonaTraits.ENERGETIC_MC = PersonaTraits(
    warmth=0.85,
    humor=0.90,
    formality=0.20,
    energy=1.00,
    empathy=0.70,
    assertiveness=0.85,
)
"""High-energy master of ceremonies with comedic flair and audience engagement."""

PersonaTraits.CALM_GUIDE = PersonaTraits(
    warmth=0.80,
    humor=0.30,
    formality=0.60,
    energy=0.40,
    empathy=0.95,
    assertiveness=0.35,
)
"""A serene, empathetic guide focused on understanding and careful explanation."""
