# PUCP-Metrix

A comprehensive set of indicators and metrics for assessing text complexity in Spanish, developed by the Artificial Intelligence Group at PUCP (Pontificia Universidad Católica del Perú).

## Overview

PUCP-Metrix is a Python library that provides an extensive collection of text complexity metrics specifically designed for Spanish texts. It implements various linguistic and psycholinguistic measures inspired by Coh-Metrix, adapted and optimized for Spanish language processing.

## Features

The library calculates over 100 different text complexity metrics organized into several categories:

### 📊 Descriptive Indices
- **Text structure**: Paragraph count, sentence count, word count
- **Length statistics**: Average sentence length, paragraph length, word length
- **Syllable analysis**: Syllables per word, syllables per content word

### 📖 Readability Indices
- **Fernández-Huertas Grade Level**: Spanish adaptation of readability formulas
- **Szigriszt-Pazos Perspicuity**: Spanish readability measure
- **SMOG Index**: Simple Measure of Gobbledygook
- **Gunning Fog Index**: Readability assessment
- **Brunet Index**: Vocabulary richness measure
- **Honoré Statistic**: Vocabulary diversity measure

### 🔗 Syntactic Complexity
- **Noun phrase complexity**: Analysis of noun phrase structures
- **Verb phrase patterns**: Verb phrase identification and analysis
- **Words before main verb**: Syntactic complexity measure
- **Syntactic pattern density**: Various syntactic structure densities

### 🌐 Cohesion Indices
- **Referential cohesion**: Pronoun usage, noun overlap, argument overlap
- **Semantic cohesion**: LSA-based semantic similarity measures
- **Connective analysis**: Causal, logical, adversative, temporal, and additive connectives

### 📝 Lexical Diversity
- **Type-Token Ratio (TTR)**: Various TTR measures

### 🧠 Psycholinguistic Indices
- **Word frequency**: Based on Spanish corpora
- **Word information**: Information-theoretic measures
- **Psycholinguistic properties**: Age of acquisition, familiarity, concreteness

### 🎯 Textual Simplicity
- **Content word density**: Ratio of content words to total words
- **Informative word analysis**: Identification and analysis of informative words

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
# Using the provided script
./install_es_core_news

# Or manually
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
