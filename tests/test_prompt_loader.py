from armo.planner.prompt_loader import PromptLoader


def test_system_prompt():
    prompt = PromptLoader.load_system_prompt()

    assert len(prompt) > 0


def test_user_prompt():
    prompt = PromptLoader.load_user_prompt("Hello")

    assert "Hello" in prompt