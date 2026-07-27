# Feature architecture

Each product capability owns its UI, domain queries, mutations, schemas, route adapters and tests. Features may import shared components and domain types but never reach into another feature's internals.

Recommended internal layout:

```text
feature/
  api/
  components/
  hooks/
  schemas/
  services/
  types/
  utils/
  index.ts
```

Cross-feature journeys are composed at route level. Authentication and authorization are enforced at middleware and API boundaries rather than inside visual components.
