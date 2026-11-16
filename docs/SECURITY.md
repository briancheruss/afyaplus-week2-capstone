# Security and privacy design notes

This is a student demonstration and **not certified for real patient data**.

- Input is masked before agent/model invocation. History stores masked text only.
- The reversible map stays in process memory, per session, and is cleared at exit.
- Output de-masking is **off by default** and requires an explicit caller-controlled
  authorization flag. The CLI never enables it.
- The application must not log raw user input, token maps, or model prompts.
- Synthetic manuals only. Never ingest patient files into the vector index.
- Current masking covers common Kenyan phone formats and emails; it does not catch
  names, IDs, insurance member numbers, addresses, or every formatting variation.
- Production deployment would require a DPIA where applicable, lawful basis,
  access controls, encryption, retention/deletion policy, audit logging without PII,
  data subject request handling, vendor/data-transfer assessment, and human review.
- The model is not a clinician and cannot approve claims, prescribe, or diagnose.
- Retrieval is not a substitute for source authority checks or human verification.
- Untrusted source text must not be allowed to change the agent's safety policy.
