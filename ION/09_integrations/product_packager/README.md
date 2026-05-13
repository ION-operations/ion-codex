# ION Product Packager

This integration owns the reproducible builder for the sidecar product package:

```text
/home/sev/ION_PRODUCT_PACKAGE
```

The product package is a generated projection of the live ION repo. It is not a
second source of truth.

```text
live ION repo -> product package builder -> ION_PRODUCT_PACKAGE
```

The first scaffold separates:

- `ION_ENGINE/` - stable law and method projection
- `ION_DATA_SCHEMA/` - portable data zip compatibility contract
- `ION_CUSTOM_GPT_ADAPTER/` - browser-sandbox carrier behavior
- `ION_STARTER_DATA/` - seeded portable continuity state
- `ION_PRODUCT_DOCS/` - operator-facing product instructions

Required generated provenance files:

- `SOURCE_PROVENANCE.json`
- `PRODUCT_SOURCE_MAP.json`
- `BUILD_RECEIPT.json`
- `ION_ENGINE_COVERAGE_MANIFEST.json`

Run from the repo root:

```bash
python3 ION/09_integrations/product_packager/ion_product_package_builder.py --output /home/sev/ION_PRODUCT_PACKAGE
```

The generated package includes its own lightweight validator and starter zip
builder under `tools/`.

The source folder remains `ION_STARTER_DATA/`, but the generated continuity
zip places `ION_DATA_MANIFEST.json` at zip root so a browser AI sandbox can
mount it without searching through an extra wrapper directory.

The engine coverage manifest tracks generated role dossiers, template dossiers,
runtime-mode dossiers, and the runtime boundary matrix so the package is
auditable as a product projection instead of a hand-curated folder.
