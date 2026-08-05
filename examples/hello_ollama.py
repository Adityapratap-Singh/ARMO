from armo.executor.ollama_executor import OllamaExecutor
from armo.models import Capability, ModelTier, SubTask


task = SubTask(
    id="demo",
    description="Explain recursion in one short paragraph.",
    capability=Capability.REASONING,
    difficulty=0.2,
)

executor = OllamaExecutor(ModelTier.STRONG)

result = executor.execute(task)

print("\n===== MODEL =====")
print(executor.model)

print("\n===== LATENCY =====")
print(f"{result.latency:.2f}s")

print("\n===== RESPONSE =====")
print(result.output)