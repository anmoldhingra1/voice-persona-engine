"""System prompt templates that are modulated by persona traits."""

from dataclasses import dataclass


@dataclass
class PromptTemplate:
    """A prompt template with placeholder values for persona-driven modulation."""

    base: str
    warmth_modifier: dict[str, str]
    humor_modifier: dict[str, str]
    formality_modifier: dict[str, str]
    energy_modifier: dict[str, str]
    empathy_modifier: dict[str, str]
    assertiveness_modifier: dict[str, str]


def get_warmth_descriptor(level: float) -> str:
    """Get a warmth descriptor based on trait level (0.0-1.0)."""
    if level < 0.2:
        return "professional and distant"
    elif level < 0.4:
        return "professional and courteous"
    elif level < 0.6:
        return "friendly and approachable"
    elif level < 0.8:
        return "warm and welcoming"
    else:
        return "exceptionally warm and affectionate"


def get_humor_descriptor(level: float) -> str:
    """Get a humor descriptor based on trait level (0.0-1.0)."""
    if level < 0.2:
        return "avoid humor"
    elif level < 0.4:
        return "occasional light humor"
    elif level < 0.6:
        return "natural, conversational humor"
    elif level < 0.8:
        return "regular witty remarks and clever observations"
    else:
        return "frequent humor and comedic timing"


def get_formality_descriptor(level: float) -> str:
    """Get a formality descriptor based on trait level (0.0-1.0)."""
    if level < 0.2:
        return "very casual, conversational tone"
    elif level < 0.4:
        return "casual and conversational"
    elif level < 0.6:
        return "balanced professional and conversational"
    elif level < 0.8:
        return "formal and professional"
    else:
        return "highly formal and academic"


def get_energy_descriptor(level: float) -> str:
    """Get an energy descriptor based on trait level (0.0-1.0)."""
    if level < 0.2:
        return "calm, measured, and deliberate"
    elif level < 0.4:
        return "relaxed and steady"
    elif level < 0.6:
        return "naturally engaged and present"
    elif level < 0.8:
        return "enthusiastic and dynamic"
    else:
        return "exceptionally vibrant and energetic"


def get_empathy_descriptor(level: float) -> str:
    """Get an empathy descriptor based on trait level (0.0-1.0)."""
    if level < 0.2:
        return "objective and neutral"
    elif level < 0.4:
        return "respectful and aware of audience needs"
    elif level < 0.6:
        return "emotionally intelligent and attentive"
    elif level < 0.8:
        return "deeply empathetic and emotionally tuned"
    else:
        return "exceptionally empathetic and emotionally attuned"


def get_assertiveness_descriptor(level: float) -> str:
    """Get an assertiveness descriptor based on trait level (0.0-1.0)."""
    if level < 0.2:
        return "tentative and deferential"
    elif level < 0.4:
        return "respectfully suggestive"
    elif level < 0.6:
        return "confidently informative"
    elif level < 0.8:
        return "direct and commanding"
    else:
        return "highly assertive and authoritative"


def build_system_prompt(
    warmth: float,
    humor: float,
    formality: float,
    energy: float,
    empathy: float,
    assertiveness: float,
) -> str:
    """
    Build a system prompt dynamically based on persona traits.

    Args:
        warmth: Warmth trait (0.0-1.0)
        humor: Humor trait (0.0-1.0)
        formality: Formality trait (0.0-1.0)
        energy: Energy trait (0.0-1.0)
        empathy: Empathy trait (0.0-1.0)
        assertiveness: Assertiveness trait (0.0-1.0)

    Returns:
        A system prompt string tuned to the persona
    """
    warmth_desc = get_warmth_descriptor(warmth)
    humor_desc = get_humor_descriptor(humor)
    formality_desc = get_formality_descriptor(formality)
    energy_desc = get_energy_descriptor(energy)
    empathy_desc = get_empathy_descriptor(empathy)
    assertiveness_desc = get_assertiveness_descriptor(assertiveness)

    prompt = f"""You are an AI assistant with the following personality characteristics:

Communication Style:
- Tone: {warmth_desc}
- Humor: {humor_desc}
- Register: {formality_desc}
- Presence: {energy_desc}

Interpersonal Approach:
- Empathy: {empathy_desc}
- Assertiveness: {assertiveness_desc}

Guidelines:
- Maintain these personality traits consistently across all responses
- Adapt your language and examples to match the described persona
- Ensure all responses feel authentic to this character
- Balance personality with clarity and helpfulness"""

    return prompt


def get_text_modifiers(
    warmth: float,
    humor: float,
    formality: float,
    energy: float,
    empathy: float,
    assertiveness: float,
) -> dict[str, list[str]]:
    """
    Get linguistic modifiers based on persona traits.

    Returns a dictionary mapping trait names to lists of linguistic modifiers
    that can be applied to text.

    Args:
        warmth: Warmth trait (0.0-1.0)
        humor: Humor trait (0.0-1.0)
        formality: Formality trait (0.0-1.0)
        energy: Energy trait (0.0-1.0)
        empathy: Empathy trait (0.0-1.0)
        assertiveness: Assertiveness trait (0.0-1.0)

    Returns:
        Dictionary of modifier lists keyed by trait name
    """
    warmth_intensifiers = (
        ["really", "truly", "genuinely", "sincerely"] if warmth > 0.6 else []
    )
    warmth_qualifiers = ["perhaps", "maybe", "if I may"] if warmth > 0.7 else []

    humor_additions = (
        ["with a smile", "tongue in cheek", "jokingly"] if humor > 0.6 else []
    )

    formality_contractions = (
        ["I'm", "you're", "don't"]
        if formality < 0.6
        else ["I am", "you are", "do not"]
    )

    energy_intensifiers = (
        ["absolutely", "definitely", "certainly"] if energy > 0.7 else []
    )
    energy_qualifiers = ["quietly", "softly", "gently"] if energy < 0.4 else []

    empathy_phrases = ["I understand", "I see", "that makes sense"] if empathy > 0.6 else []

    assertiveness_qualifiers = (
        ["perhaps", "you might consider"] if assertiveness < 0.4 else []
    )
    assertiveness_imperatives = (
        ["do this", "must happen"] if assertiveness > 0.7 else []
    )

    return {
        "warmth_intensifiers": warmth_intensifiers,
        "warmth_qualifiers": warmth_qualifiers,
        "humor_additions": humor_additions,
        "formality_contractions": formality_contractions,
        "energy_intensifiers": energy_intensifiers,
        "energy_qualifiers": energy_qualifiers,
        "empathy_phrases": empathy_phrases,
        "assertiveness_qualifiers": assertiveness_qualifiers,
        "assertiveness_imperatives": assertiveness_imperatives,
    }
