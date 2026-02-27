"""Pytest configuration and shared fixtures."""

import pytest

from persona import PersonaEngine, PersonaTraits


@pytest.fixture
def engine():
    """Provide a fresh PersonaEngine instance for each test."""
    return PersonaEngine()


@pytest.fixture
def friendly_host_traits():
    """Provide FRIENDLY_HOST traits."""
    return PersonaTraits.FRIENDLY_HOST


@pytest.fixture
def professional_analyst_traits():
    """Provide PROFESSIONAL_ANALYST traits."""
    return PersonaTraits.PROFESSIONAL_ANALYST


@pytest.fixture
def energetic_mc_traits():
    """Provide ENERGETIC_MC traits."""
    return PersonaTraits.ENERGETIC_MC


@pytest.fixture
def calm_guide_traits():
    """Provide CALM_GUIDE traits."""
    return PersonaTraits.CALM_GUIDE


@pytest.fixture
def custom_traits():
    """Provide custom traits for testing."""
    return PersonaTraits(
        warmth=0.6,
        humor=0.4,
        formality=0.7,
        energy=0.5,
        empathy=0.8,
        assertiveness=0.3,
    )
