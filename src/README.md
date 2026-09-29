# Source Layout

Implementation modules will be organized around the following boundaries:

```text
src/
├── identity/      # face detection / verification integration
├── content/       # sensitive-content detection
├── policy/        # privacy risk and action policy
├── shield/        # mask / blur / lock actions
└── events/        # privacy event logging
```

The current repository documents the architecture before claiming completed implementation. As components are implemented, each module should include reproducible setup and test instructions.
