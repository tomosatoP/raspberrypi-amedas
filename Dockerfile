FROM tomosatop/poetry

WORKDIR /amedas
COPY pyproject.toml* poetry.lock* ./
RUN if [ -f pyproject.toml ]; then poetry install --no-root --only main; fi

ENTRYPOINT ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["src.app.main:app"]
