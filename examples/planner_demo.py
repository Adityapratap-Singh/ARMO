from armo.planner.prompt_loader import PromptLoader

print("===== SYSTEM =====")
print(PromptLoader.load_system_prompt())

print()

print("===== USER =====")
print(
    PromptLoader.load_user_prompt(
        "Research Tesla and compare it with BYD."
    )
)