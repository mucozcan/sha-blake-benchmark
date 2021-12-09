## Performance comparison SHA256 with BLAKE2b on PoW

### Linux Installation

Install Poetry, the dependency management tool.
```
pip3 install poetry
```

Clone the repository
```
git clone https://github.com/mucozcan/sha-blake-benchmark.git
```

Install dependencies
```
cd sha-blake-benchmark
poetry install
```

Run the server
```
cd sha-blake-benchmark
poetry run uvicorn server:app --reload --port 4544
```

Go to http://localhost:4544/docs
