"""Core PersonaEngine for managing and applying AI personas."""

from dataclasses import dataclass
from typing import Optional

from persona.prompts import build_system_prompt, get_text_modifiers
from persona.traits import PersonaTraits


@dataclass
class Persona:
    """
    Represents a complete persona with name and traits.

    Attributes:
        name: Unique identifier for the persona
        traits: PersonaTraits defining the personality dimensions
    """

    name: str
    traits: PersonaTraits

    def to_dict(self) -> dict:
        """
        Convert persona to dictionary representation.

        Returns:
            Dictionary with name and traits data
        """
        return {
            "name": self.name,
            "traits": {
                "warmth": self.traits.warmth,
                "humor": self.traits.humor,
                "formality": self.traits.formality,
                "energy": self.traits.energy,
                "empathy": self.traits.empathy,
                "assertiveness": self.traits.assertiveness,
            },
        }


class PersonaEngine:
    """
    Engine for creating, managing, and applying AI personas.

    The PersonaEngine allows you to define personas with trait vectors,
    apply them to LLM outputs, and generate personality-modulated system prompts.

    Example:
        engine = PersonaEngine()
        friendly = engine.create_persona(
            "friendly_host",
            PersonaTraits.FRIENDLY_HOST
        )
        system_prompt = engine.generate_system_prompt(friendly)
    """

    def __init__(self) -> None:
        """Initialize the PersonaEngine."""
        self._personas: dict[str, Persona] = {}

    def create_persona(
        self,
        name: str,
        traits: PersonaTraits,
        overwrite: bool = False,
    ) -> Persona:
        """
        Create a new persona.

        Args:
            name: Unique identifier for the persona
            traits: PersonaTraits defining personality dimensions
            overwrite: If False, raises ValueError if persona exists

        Returns:
            The created Persona instance

        Raises:
            ValueError: If persona with that name already exists (unless overwrite=True)
        """
        if name in self._personas and not overwrite:
            msg = f"Persona '{name}' already exists. Set overwrite=True to replace."
            raise ValueError(msg)

        persona = Persona(name=name, traits=traits)
        self._personas[name] = persona
        return persona

    def get_persona(self, name: str) -> Optional[Persona]:
        """
        Retrieve an existing persona by name.

        Args:
            name: Name of the persona to retrieve

        Returns:
            The Persona if found, None otherwise
        """
        return self._personas.get(name)

    def list_personas(self) -> list[str]:
        """
        List all registered persona names.

        Returns:
            List of persona names
        """
        return list(self._personas.keys())

    def delete_persona(self, name: str) -> bool:
        """
        Delete a persona.

        Args:
            name: Name of the persona to delete

        Returns:
            True if deleted, False if persona didn't exist
        """
        if name in self._personas:
            del self._personas[name]
            return True
        return False

    def apply_persona(
        self,
        text: str,
        persona: Persona,
        enhance: bool = True,
    ) -> str:
        """
        Apply a persona to text by enhancing it with personality traits.

        Args:
            text: Input text to transform
            persona: Persona to apply
            enhance: If True, enhances text linguistically based on traits

        Returns:
            Transformed text with persona applied

        Example:
            engine = PersonaEngine()
            friendly = engine.create_persona("friendly", PersonaTraits.FRIENDLY_HOST)
            result = engine.apply_persona("Thank you for joining.", friendly)
        """
        if not enhance:
            return text

        traits = persona.traits
        _ = get_text_modifiers(
            warmth=traits.warmth,
            humor=traits.humor,
            formality=traits.formality,
            energy=traits.energy,
            empathy=traits.empathy,
            assertiveness=traits.assertiveness,
        )

        result = text

        # Apply energy-based transformations
        if traits.energy > 0.7:
            result = result.replace(".", "!")
            result = result.replace("Thank you", "Thank you so much")
        elif traits.energy < 0.3:
            result = result.replace("!", ".")

        # Apply warmth-based transformations
        if traits.warmth > 0.7:
            result = result.replace("here", "here with us")
            result = result.replace(".", ". We're glad you're here.")

        # Apply formality-based contractions
        if traits.formality < 0.5:
            replacements = {
                "do not": "don't",
                "cannot": "can't",
                "will not": "won't",
                "is not": "isn't",
                "are not": "aren't",
                "I am": "I'm",
                "you are": "you're",
            }
            for formal, casual in replacements.items():
                result = result.replace(formal, casual)

        return result

    def generate_system_prompt(self, persona: Persona) -> str:
        """
        Generate an LLM system prompt tailored to the persona.

        Args:
            persona: Persona to generate prompt for

        Returns:
            System prompt string ready for use with LLMs

        Example:
            engine = PersonaEngine()
            analyst = engine.create_persona(
                "analyst", PersonaTraits.PROFESSIONAL_ANALYST
            )
            prompt = engine.generate_system_prompt(analyst)
            # Use prompt with Claude, GPT-4, etc.
        """
        return build_system_prompt(
            warmth=persona.traits.warmth,
            humor=persona.traits.humor,
            formality=persona.traits.formality,
            energy=persona.traits.energy,
            empathy=persona.traits.empathy,
            assertiveness=persona.traits.assertiveness,
        )

    def blend_personas(
        self,
        persona_a: Persona,
        persona_b: Persona,
        weight: float = 0.5,
        save_as: Optional[str] = None,
    ) -> Persona:
        """
        Blend two personas together.

        Creates a new persona with trait values interpolated between two input personas.

        Args:
            persona_a: First persona to blend
            persona_b: Second persona to blend
            weight: Weight for persona_a (0.0 = all B, 1.0 = all A)
            save_as: Optional name to save the blended persona

        Returns:
            New blended Persona instance

        Raises:
            ValueError: If weight is outside 0.0-1.0 range

        Example:
            blended = engine.blend_personas(
                professional_analyst,
                friendly_host,
                weight=0.6,
                save_as="friendly_analyst"
            )
        """
        blended_traits = persona_a.traits.blend(persona_b.traits, weight)

        blend_name = save_as or f"{persona_a.name}_blend_{persona_b.name}"

        blended_persona = Persona(name=blend_name, traits=blended_traits)

        if save_as:
            self._personas[save_as] = blended_persona

        return blended_persona

    def get_persona_info(self, name: str) -> Optional[dict]:
        """
        Get detailed information about a persona.

        Args:
            name: Name of the persona

        Returns:
            Dictionary with persona details, or None if not found
        """
        persona = self.get_persona(name)
        if not persona:
            return None

        return {
            "name": persona.name,
            "traits": {
                "warmth": persona.traits.warmth,
                "humor": persona.traits.humor,
                "formality": persona.traits.formality,
                "energy": persona.traits.energy,
                "empathy": persona.traits.empathy,
                "assertiveness": persona.traits.assertiveness,
            },
        }
