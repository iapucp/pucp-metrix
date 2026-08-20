# PUCP-Metrix

Paper: [https://aclanthology.org/2026.eacl-demo.28/](https://aclanthology.org/2026.eacl-demo.28/)

A comprehensive set of indicators and metrics for assessing text complexity in Spanish, developed by the Artificial Intelligence Group at PUCP (Pontificia Universidad Católica del Perú).

## Overview

PUCP-Metrix is a Python library that provides an extensive collection of text complexity metrics specifically designed for Spanish texts. It implements various linguistic and psycholinguistic measures inspired by Coh-Metrix, adapted and optimized for Spanish language processing.

## Features

The library calculates over 100 different text complexity metrics. You can find all metric descriptions at [metrics.md](metrics.md).

## Installation

### Prerequisites

- Python 3.12 or higher

### Install the package

```bash
# Using UV (recommended)
uv add iapucp-metrix

# Or using pip
pip install iapucp-metrix
```

### Install Spanish language model

After installing the package, you need to install the required Spanish spaCy model:

```bash
# For pip users
python -m spacy download es_core_news_lg

# For uv users
uv pip install es_core_news_lg@https://github.com/explosion/spacy-models/releases/download/es_core_news_lg-3.8.0/es_core_news_lg-3.8.0-py3-none-any.whl
```

## Quick Start

```python
from iapucp_metrix.analyzer import Analyzer

# Initialize analyzer
analyzer = Analyzer()

# Process multiple texts efficiently
texts = [
    "Primer texto para analizar...",
    "Segundo texto con contenido diferente...",
    "Tercer texto para completar el análisis..."
]

# Compute metrics with multiprocessing
metrics_list = analyzer.compute_metrics(
    texts, 
    workers=4,     # Use 4 CPU cores
    batch_size=2   # Process 2 texts per batch
)

# Process results
for i, metrics in enumerate(metrics_list):
    print(f"Text {i+1}:")
    print(f"  Readability (Fernández-Huertas): {metrics['RDFHGL']:.2f}")
```

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/your-org/pucp-metrix.git
cd pucp-metrix

# Install dependencies
uv sync

# Install the Spanish model
./install_es_core_news

# Run tests
uv run pytest
```

## Citation

If you use this work, please cite:

```bibtex
@inproceedings{luis-cabezudo-2026-pucp,
    title = "{PUCP}-Metrix: An Open-source and Comprehensive Toolkit for Linguistic Analysis of {S}panish Texts",
    author = "Luis, Javier Alonso Villegas  and
      Cabezudo, Marco Antonio Sobrevilla",
    editor = "Croce, Danilo  and
      Leidner, Jochen  and
      Moosavi, Nafise Sadat",
    booktitle = "Proceedings of the 19th Conference of the {E}uropean Chapter of the {A}ssociation for {C}omputational {L}inguistics (Volume 3: System Demonstrations)",
    month = mar,
    year = "2026",
    address = "Rabat, Marocco",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.eacl-demo.28/",
    doi = "10.18653/v1/2026.eacl-demo.28",
    pages = "407--416",
    ISBN = "979-8-89176-382-1",
    abstract = "Linguistic features remain essential for interpretability and tasks that involve style, structure, and readability, but existing Spanish tools offer limited coverage. We present PUCPMetrix, an open-source and comprehensive toolkit for linguistic analysis of Spanish texts. PUCP-Metrix includes 182 linguistic metrics spanning lexical diversity, syntactic and semantic complexity, cohesion, psycholinguistics, and readability. It enables fine-grained, interpretable text analysis. We evaluate its usefulness on Automated Readability Assessment and Machine-Generated Text Detection, showing competitive performance compared to an existing repository and strong neural baselines. PUCP-Metrix offers a comprehensive and extensible resource for Spanish, supporting diverse NLP applications."
}
```

## Applications

We've started exploring the use of linguistic features in other tasks. You can find a list of papers where PUCP-Metrix has been used:
- Machine-generated Text Detection in Spanish (http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/article/view/6843)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
