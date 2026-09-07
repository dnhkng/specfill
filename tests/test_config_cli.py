"""The `specfill config` subcommands, driven through their handler functions."""

from specfill.app import _config_set, _config_show
from specfill.config import default_settings, load_settings


def test_config_set_reasoning_effort(capsys):
    assert _config_set(default_settings("openai"), "reasoning-effort", "high") == 0
    assert capsys.readouterr().out.strip() == "reasoning-effort = high"
    saved = load_settings()
    assert saved is not None
    assert saved.reasoning_effort == "high"


def test_config_set_rejects_unknown_reasoning_effort(capsys):
    assert _config_set(default_settings("openai"), "reasoning-effort", "ultra") == 1
    assert "unknown reasoning effort 'ultra'" in capsys.readouterr().err
    assert load_settings() is None  # nothing written


def test_config_show_lists_reasoning_effort(capsys):
    settings = default_settings("anthropic").model_copy(update={"reasoning_effort": "low"})
    assert _config_show(settings) == 0
    out = capsys.readouterr().out
    assert "reasoning-effort:  low" in out
    assert "provider:          anthropic" in out
