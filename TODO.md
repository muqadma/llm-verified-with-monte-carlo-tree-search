# TODOs

- [x] Support other verifiers in addition to Dafny:
  - [x] Coq
    - [ ] The current system struggles with Coq proofs.
- [ ] Support other LLM infrastructures in addition to Hugging Face:
  - [ ] [Ollama](https://ollama.ai)
- [ ] Support test cases.
- [ ] Design a steerable interaction to give human or tool feedback to the LLM.
  - [x] Confirm completion at each step, and add a comment to steer.
  - [ ] Edit entire text, e.g. to add imports.
  - [ ] Give the verifier feedback.
    - [x] Rudimentary display of goal context in case of error (Coq only).
- [ ] Design higher level steerable schemes:
  - [ ] Synthesize Coq proofs.
- [ ] The LLM can get stuck repeating the same completion over and over again, if it doesn't have a diverse set of outputs.
- [x] Design a reinforcement learning scheme, whereas the LLM learns from trial.
  - [ ] Evaluate whether the model after PPO suffers degradation for some tasks, even unrelated.
  - [ ] Force the PPO solution to converge to an optimal known one, using it entirely for training rather than discovery.
- [x] Get wandb to work.
- [ ] Maybe add a per language blacklist, so that we can rule out uses of `Admitted` in Coq.
- [x] Refactor the shared arguments between llm.py and ppo.py.
- [ ] Glitch: sometimes, the code is not in triple quotes, causing long running completion generations.
- [ ] Why Coq is much harder than Dafny:
  - [ ] Dafny has more automation.
  - [ ] Coq can have idempotent tactics (like `simpl`) which can be repeated uselessly indefinitely.
