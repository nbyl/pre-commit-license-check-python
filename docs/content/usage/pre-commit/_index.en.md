---
title: "pre-commit Hooks"
weight: 20
---

kontrolilo can be used as a [git pre-commit hook](https://pre-commit.com). This will check your package files before committing changes to you repository that contain invalid licenses and enable you to shift your changes even more to the left.

### Installation
Please install pre-commit first according to the [documentation](https://pre-commit.com/#install).

Afterwards put the needed hooks into your `.pre-commit-config.yaml`:

```
---
repos:
  - repo: https://github.com/kontrolilo/kontrolilo
    rev: v2.1.0
    hooks:
      - id: license-check-configuration-lint
      - id: license-check-gradle
      - id: license-check-maven
      - id: license-check-npm
      - id: license-check-pipenv
      - id: license-check-yarn
```

### Available Hooks

{{% children  %}}
