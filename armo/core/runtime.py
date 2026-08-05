while not runtime.finished():

    ready_tasks = scheduler.get_ready_tasks(runtime)

    results = executor.execute(ready_tasks)

    runtime.record(results)

    signals = signal_engine.compute(runtime)

    decision = switching_policy.evaluate(signals)

    runtime.apply(decision)

return runtime.final_result()