# Build Handbook PDF

The renderer joins the documentation in a stable order: repository README,
methodology, guides, then architecture.

```powershell
uv run --with-requirements build-pipeline/requirements.txt python build-pipeline/generate_pdf.py
```

The default output is `output/pdf/indiekator-docs.pdf`. Pass `--output PATH`
to use another location. Generated output and temporary rendered pages are
ignored by Git.
