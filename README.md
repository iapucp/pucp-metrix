# PUCP-Metrix

A comprehensive set of indicators and metrics for assessing text complexity in Spanish, developed by the Artificial Intelligence Group at PUCP (Pontificia Universidad Católica del Perú).

## Overview

PUCP-Metrix is a Python library that provides an extensive collection of text complexity metrics specifically designed for Spanish texts. It implements various linguistic and psycholinguistic measures inspired by Coh-Metrix, adapted and optimized for Spanish language processing.

## Features

The library calculates over 100 different text complexity metrics organized into several categories:

### 📊 Descriptive Indices
Basic text structure and length statistics:
- **DESPC**: Paragraph count
- **DESPCi**: Paragraph count incidence per 1000 words
- **DESSC**: Sentence count
- **DESSCi**: Sentence count incidence per 1000 words
- **DESWC**: Word count (alphanumeric words)
- **DESWCU**: Unique word count
- **DESWCUi**: Unique word count incidence per 1000 words
- **DESPL**: Average paragraph length (sentences per paragraph)
- **DESPLd**: Standard deviation of paragraph length
- **DESSL**: Average sentence length (words per sentence)
- **DESSLd**: Standard deviation of sentence length
- **DESSNSL**: Average sentence length excluding stopwords
- **DESSNSLd**: Standard deviation of sentence length excluding stopwords
- **DESSLmax**: Maximum sentence length
- **DESSLmin**: Minimum sentence length
- **DESWLsy**: Average syllables per word
- **DESWLsyd**: Standard deviation of syllables per word
- **DESCWLsy**: Average syllables per content word
- **DESCWLsyd**: Standard deviation of syllables per content word
- **DESCWLlt**: Average letters per content word
- **DESCWLltd**: Standard deviation of letters per content word
- **DESWLlt**: Average letters per word
- **DESWLltd**: Standard deviation of letters per word
- **DESWNSLlt**: Average letters per word (excluding stopwords)
- **DESWNSLltd**: Standard deviation of letters per word (excluding stopwords)
- **DESLLlt**: Average letters per lemma
- **DESLLltd**: Standard deviation of letters per lemma

### 📖 Readability Indices
Traditional readability formulas adapted for Spanish:
- **RDFHGL**: Fernández-Huertas Grade Level
- **RDSPP**: Szigriszt-Pazos Perspicuity
- **RDMU**: Readability µ index
- **RDSMOG**: SMOG index
- **RDFOG**: Gunning Fog index
- **RDHS**: Honoré Statistic
- **RDBR**: Brunet index

### 🔗 Syntactic Complexity Indices
Measures of syntactic structure complexity:
- **SYNNP**: Mean number of modifiers per noun phrase
- **SYNLE**: Mean number of words before main verb
- **SYNMEDwrd**: Minimal edit distance of words between adjacent sentences
- **SYNMEDlem**: Minimal edit distance of lemmas between adjacent sentences
- **SYNMEDpos**: Minimal edit distance of POS tags between adjacent sentences
- **SYNCLS1**: Ratio of sentences with 1 clause
- **SYNCLS2**: Ratio of sentences with 2 clauses
- **SYNCLS3**: Ratio of sentences with 3 clauses
- **SYNCLS4**: Ratio of sentences with 4 clauses
- **SYNCLS5**: Ratio of sentences with 5 clauses
- **SYNCLS6**: Ratio of sentences with 6 clauses
- **SYNCLS7**: Ratio of sentences with 7 clauses

### 🎯 Syntactic Pattern Density Indices
Density measures of specific syntactic patterns:
- **DRNP**: Noun phrase density per 1000 words
- **DRNPc**: Noun phrase count
- **DRVP**: Verb phrase density per 1000 words
- **DRVPc**: Verb phrase count
- **DRNEG**: Negation expression density per 1000 words
- **DRNEGc**: Negation expression count
- **DRGER**: Gerund form density per 1000 words
- **DRGERc**: Gerund count
- **DRINF**: Infinitive form density per 1000 words
- **DRINFc**: Infinitive count
- **DRCCONJ**: Coordinating conjunction density per 1000 words
- **DRCCONJc**: Coordinating conjunction count
- **DRSCONJ**: Subordinating conjunction density per 1000 words
- **DRSCONJc**: Subordinating conjunction count

### 🌐 Connective Indices
Analysis of discourse connectives:
- **CNCAll**: All connectives incidence per 1000 words
- **CNCCaus**: Causal connectives incidence per 1000 words
- **CNCLogic**: Logical connectives incidence per 1000 words
- **CNCADC**: Adversative connectives incidence per 1000 words
- **CNCTemp**: Temporal connectives incidence per 1000 words
- **CNCAdd**: Additive connectives incidence per 1000 words

### 🔗 Referential Cohesion Indices
Measures of referential overlap between sentences:
- **CRFNO1**: Noun overlap between adjacent sentences
- **CRFAO1**: Argument overlap between adjacent sentences
- **CRFSO1**: Stem overlap between adjacent sentences
- **CRFCWO1**: Content word overlap between adjacent sentences (mean)
- **CRFCWO1d**: Content word overlap between adjacent sentences (std dev)
- **CRFANP1**: Anaphore overlap between adjacent sentences
- **CRFNOa**: Noun overlap between all sentences
- **CRFAOa**: Argument overlap between all sentences
- **CRFSOa**: Stem overlap between all sentences
- **CRFCWOa**: Content word overlap between all sentences (mean)
- **CRFCWOad**: Content word overlap between all sentences (std dev)
- **CRFANPa**: Anaphore overlap between all sentences

### 🌊 Semantic Cohesion Indices
LSA-based semantic similarity measures:
- **SECLOSadj**: LSA overlap between adjacent sentences (mean)
- **SECLOSadjd**: LSA overlap between adjacent sentences (std dev)
- **SECLOSall**: LSA overlap between all sentences (mean)
- **SECLOSalld**: LSA overlap between all sentences (std dev)
- **SECLOPadj**: LSA overlap between adjacent paragraphs (mean)
- **SECLOPadjd**: LSA overlap between adjacent paragraphs (std dev)
- **SECLOSgiv**: LSA overlap between given and new sentences (mean)
- **SECLOSgivd**: LSA overlap between given and new sentences (std dev)

### 📝 Lexical Diversity Indices
Various measures of vocabulary richness:
- **LDTTRa**: Type-token ratio for all words
- **LDTTRcw**: Type-token ratio for content words
- **LDTTRno**: Type-token ratio for nouns
- **LDTTRvb**: Type-token ratio for verbs
- **LDTTRadv**: Type-token ratio for adverbs
- **LDTTRadj**: Type-token ratio for adjectives
- **LDTTRLa**: Type-token ratio for all lemmas
- **LDTTRLno**: Type-token ratio for noun lemmas
- **LDTTRLvb**: Type-token ratio for verb lemmas
- **LDTTRLadv**: Type-token ratio for adverb lemmas
- **LDTTRLadj**: Type-token ratio for adjective lemmas
- **LDTTRLpron**: Type-token ratio for pronouns
- **LDTTRLrpron**: Type-token ratio for relative pronouns
- **LDTTRLipron**: Type-token ratio for indefinite pronouns
- **LDTTRLifn**: Type-token ratio for functional words
- **LDMLTD**: Measure of Textual Lexical Diversity (MTLD)
- **LDVOCd**: Vocabulary Complexity Diversity (VoCD)
- **LDMaas**: Maas index
- **LDDno**: Noun density
- **LDDvb**: Verb density
- **LDDadv**: Adverb density
- **LDDadj**: Adjective density

### 📊 Word Information Indices
Incidence of different word types:
- **WRDCONT**: Content word incidence per 1000 words
- **WRDCONTc**: Content word count
- **WRDNOUN**: Noun incidence per 1000 words
- **WRDNOUNc**: Noun count
- **WRDVERB**: Verb incidence per 1000 words
- **WRDVERBc**: Verb count
- **WRDADJ**: Adjective incidence per 1000 words
- **WRDADJc**: Adjective count
- **WRDADV**: Adverb incidence per 1000 words
- **WRDADVc**: Adverb count
- **WRDPRO**: Personal pronoun incidence per 1000 words
- **WRDPROc**: Personal pronoun count
- **WRDPRP1s**: First person singular pronoun incidence per 1000 words
- **WRDPRP1sc**: First person singular pronoun count
- **WRDPRP1p**: First person plural pronoun incidence per 1000 words
- **WRDPRP1pc**: First person plural pronoun count
- **WRDPRP2s**: Second person singular pronoun incidence per 1000 words
- **WRDPRP2sc**: Second person singular pronoun count
- **WRDPRP2p**: Second person plural pronoun incidence per 1000 words
- **WRDPRP2pc**: Second person plural pronoun count
- **WRDPRP3s**: Third person singular pronoun incidence per 1000 words
- **WRDPRP3sc**: Third person singular pronoun count
- **WRDPRP3p**: Third person plural pronoun incidence per 1000 words
- **WRDPRP3pc**: Third person plural pronoun count

### 🎯 Textual Simplicity Indices
Measures of sentence length distribution:
- **TSSRsh**: Ratio of short sentences (< 11 words)
- **TSSRmd**: Ratio of medium sentences (11-12 words)
- **TSSRlg**: Ratio of long sentences (13-14 words)
- **TSSRxl**: Ratio of very long sentences (≥ 15 words)

### 📈 Word Frequency Indices
Measures based on word frequency in Spanish corpora:
- **WFRCno**: Rare noun count
- **WFRCnoi**: Rare noun incidence per 1000 words
- **WFRCvb**: Rare verb count
- **WFRCvbi**: Rare verb incidence per 1000 words
- **WFRCadj**: Rare adjective count
- **WFRCadji**: Rare adjective incidence per 1000 words
- **WFRCadv**: Rare adverb count
- **WFRCadvi**: Rare adverb incidence per 1000 words
- **WFRCcw**: Rare content word count
- **WFRCcwi**: Rare content word incidence per 1000 words
- **WFRCcwd**: Distinct rare content word count
- **WFRCcwdi**: Distinct rare content word incidence per 1000 words
- **WFMcw**: Mean frequency of content words
- **WFMw**: Mean frequency of all words
- **WFMrw**: Mean frequency of rarest words per sentence
- **WFMrcw**: Mean frequency of rarest content words per sentence

### 🧠 Psycholinguistic Indices
Measures based on psycholinguistic properties of words:

**Concreteness measures:**
- **PSYC**: Overall concreteness ratio
- **PSYC0**: Very low concreteness ratio (1-2.5)
- **PSYC1**: Low concreteness ratio (2.5-4)
- **PSYC2**: Medium concreteness ratio (4-5.5)
- **PSYC3**: High concreteness ratio (5.5-7)

**Imageability measures:**
- **PSYIM**: Overall imageability ratio
- **PSYIM0**: Very low imageability ratio (1-2.5)
- **PSYIM1**: Low imageability ratio (2.5-4)
- **PSYIM2**: Medium imageability ratio (4-5.5)
- **PSYIM3**: High imageability ratio (5.5-7)

**Familiarity measures:**
- **PSYFM**: Overall familiarity ratio
- **PSYFM0**: Very low familiarity ratio (1-2.5)
- **PSYFM1**: Low familiarity ratio (2.5-4)
- **PSYFM2**: Medium familiarity ratio (4-5.5)
- **PSYFM3**: High familiarity ratio (5.5-7)

**Age of Acquisition measures:**
- **PSYAoA**: Overall age of acquisition ratio
- **PSYAoA0**: Very early acquisition ratio (1-2.5)
- **PSYAoA1**: Early acquisition ratio (2.5-4)
- **PSYAoA2**: Medium acquisition ratio (4-5.5)
- **PSYAoA3**: Late acquisition ratio (5.5-7)

**Arousal measures:**
- **PSYARO**: Overall arousal ratio
- **PSYARO0**: Very low arousal ratio (1-3)
- **PSYARO1**: Low arousal ratio (3-5)
- **PSYARO2**: Medium arousal ratio (5-7)
- **PSYARO3**: High arousal ratio (7-9)

**Valence measures:**
- **PSYVAL**: Overall valence ratio
- **PSYVAL0**: Very negative valence ratio (1-4)
- **PSYVAL1**: Negative valence ratio (3-5)
- **PSYVAL2**: Positive valence ratio (5-7)
- **PSYVAL3**: Very positive valence ratio (7-9)

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
