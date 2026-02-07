# Forced Alignment using Montreal Forced Aligner (MFA)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Assignment 1 - IIITH Speech Processing Course**
> A comprehensive implementation of forced alignment for speech-text synchronization using the Montreal Forced Aligner toolkit.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Data Preparation](#data-preparation)
- [Running Forced Alignment](#running-forced-alignment)
- [Handling Out-of-Vocabulary Words](#handling-out-of-vocabulary-words)
- [Output Files](#output-files)
- [Dataset Information](#dataset-information)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Overview

**Forced alignment** is the process of automatically synchronizing audio recordings with their corresponding text transcriptions at both word and phoneme levels. This project implements a complete forced alignment pipeline using the Montreal Forced Aligner (MFA), which uses Hidden Markov Model-Gaussian Mixture Model (HMM-GMM) based acoustic models to determine precise temporal boundaries for each linguistic unit in speech.

### What Does Forced Alignment Do?

Given:
- **Audio**: A recording of speech
- **Transcript**: Text of what was said
- **Pronunciation Dictionary**: Phonetic representations of words

The aligner produces:
- **Word boundaries**: Start and end times for each word
- **Phoneme boundaries**: Start and end times for each sound
- **TextGrid files**: Praat-compatible annotation files

### Example

**Input:**
```
Audio: [speaker says "Hello world"]
Transcript: HELLO WORLD
```

**Output (TextGrid):**
```
Words:
  0.00 – 0.45  HELLO
  0.45 – 0.90  WORLD

Phonemes:
  0.00 – 0.10  HH
  0.10 – 0.25  AH
  0.25 – 0.40  L
  0.40 – 0.45  OW
  0.45 – 0.55  W
  0.55 – 0.70  ER
  0.70 – 0.85  L
  0.85 – 0.90  D
```

## Features

✅ Complete MFA setup and installation guide
✅ Automated data preparation pipeline
✅ Out-of-Vocabulary (OOV) word handling using G2P models
✅ Before/after OOV comparison analysis
✅ TextGrid output generation for Praat visualization
✅ Alignment quality metrics and reporting
✅ Reproducible automation scripts
✅ Comprehensive documentation

## Installation

### Prerequisites

- **Operating System**: macOS or Linux (Windows via WSL2)
- **Python**: 3.8 or higher
- **Conda**: Miniconda or Anaconda ([download here](https://docs.conda.io/en/latest/miniconda.html))
- **Praat** (optional, for visualization): [Download Praat](https://www.fon.hum.uva.nl/praat/)

### Method 1: Using Conda (Recommended)

```bash
# Create dedicated conda environment with MFA
conda create -n mfa -c conda-forge montreal-forced-aligner python=3.10 -y

# Activate environment
conda activate mfa

# Verify installation
mfa version
```

### Method 2: Using pip (Alternative)

```bash
# Create virtual environment
python3 -m venv mfa_env
source mfa_env/bin/activate  # On Windows: mfa_env\Scripts\activate

# Install MFA
pip install montreal-forced-aligner

# Verify installation
mfa version
```

### Download Required Models

MFA requires acoustic models, pronunciation dictionaries, and G2P models:

```bash
# Download English US models (ARPAbet phoneme set)
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa model download g2p english_us_arpa

# Verify downloaded models
mfa model list acoustic
mfa model list dictionary
mfa model list g2p
```

**Available Models:**
- `english_us_arpa` - American English with ARPAbet phonemes
- `english_mfa` - English with IPA phonemes
- `english_uk_mfa` - British English

## Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd mfa-forced-alignment

# 2. Activate conda environment
conda activate mfa

# 3. Run complete alignment pipeline (automated)
bash run_mfa_alignment.sh

# 4. View results in Praat
# Open any TextGrid file in: output/ or output_with_oov/
```

**Expected Output:**
- `output/` - TextGrid files before OOV handling
- `output_with_oov/` - TextGrid files after OOV handling
- `oov_report/` - Out-of-vocabulary word analysis

## Data Preparation

### Directory Structure

```
mfa-forced-alignment/
├── wav/                          # Original audio files (6 files)
│   ├── F2BJRLP1.wav             # Broadcast news (~25s)
│   ├── F2BJRLP2.wav             # Broadcast news (~29s)
│   ├── F2BJRLP3.wav             # Broadcast news (~31s)
│   ├── ISLE_SESS0131_BLOCKD02_01_sprt1.wav  # Minimal pair (~4s)
│   ├── ISLE_SESS0131_BLOCKD02_02_sprt1.wav
│   └── ISLE_SESS0131_BLOCKD02_03_sprt1.wav
│
├── transcripts/                  # Original text transcripts
│   ├── ISLE_SESS0131_BLOCKD02_01_sprt1.txt
│   ├── ISLE_SESS0131_BLOCKD02_02_sprt1.txt
│   └── ISLE_SESS0131_BLOCKD02_03_sprt1.txt
│
├── corpus/                       # MFA-ready corpus (auto-generated)
│   ├── F2BJRLP1.wav             # Audio
│   ├── F2BJRLP1.lab             # Matching transcript
│   └── ...
│
├── output/                       # Alignment results (before OOV)
├── output_with_oov/              # Alignment results (after OOV)
├── oov_report/                   # OOV analysis
├── oov_pronunciations.txt        # G2P generated pronunciations
├── custom_oov_dictionary.txt     # Manual OOV pronunciations
├── run_mfa_alignment.sh          # Automation script
├── README.md                     # This file
└── REPORT.md                     # Detailed analysis report
```

### Manual Corpus Preparation

If you need to prepare the corpus manually:

```bash
# Create corpus directory
mkdir -p corpus

# Copy audio files
cp wav/*.wav corpus/

# Copy and rename transcripts to .lab format
for f in transcripts/*.txt; do
  cp "$f" "corpus/$(basename "${f%.*}").lab"
done

# Clean transcripts (ensure single-line format)
for f in corpus/*.lab; do
  tr '\n\r' ' ' < "$f" | sed 's/  */ /g; s/^ *//; s/ *$//' > "$f.tmp"
  mv "$f.tmp" "$f"
done
```

**MFA Requirements:**
- Audio and transcript files must have **matching base names**
- Audio format: WAV (16-bit PCM, mono, 16kHz recommended)
- Transcript format: Plain text (.lab or .txt), single line per file
- Both files must be in the **same directory**

## Running Forced Alignment

### Step-by-Step Manual Workflow

#### 1. Validate Corpus

Check for issues before alignment:

```bash
mfa validate corpus english_us_arpa --output_directory oov_report --clean
```

**This command:**
- ✓ Verifies audio/transcript pairs
- ✓ Checks audio quality (sampling rate, channels)
- ✓ Identifies Out-of-Vocabulary (OOV) words
- ✓ Generates report in `oov_report/`

#### 2. Run Initial Alignment

```bash
mfa align corpus english_us_arpa english_us_arpa output --clean
```

**Command breakdown:**
- `corpus` - Input directory with audio + transcripts
- `english_us_arpa` - Pronunciation dictionary
- `english_us_arpa` - Acoustic model
- `output` - Output directory for TextGrid files
- `--clean` - Clear previous temporary files

**Processing time:** ~30 seconds to 2 minutes depending on data size

#### 3. Inspect Results

```bash
# List generated TextGrid files
ls -lh output/

# View alignment quality metrics
cat output/alignment_analysis.csv
```

### Using the Automation Script

For a complete end-to-end pipeline:

```bash
bash run_mfa_alignment.sh
```

**This script automatically:**
1. ✅ Prepares corpus from raw audio/transcripts
2. ✅ Downloads required MFA models
3. ✅ Validates corpus and identifies OOV words
4. ✅ Runs initial alignment (before OOV handling)
5. ✅ Generates G2P pronunciations for OOV words
6. ✅ Runs final alignment (after OOV handling)

## Handling Out-of-Vocabulary Words

### Problem: OOV Words

Some words may not exist in the standard pronunciation dictionary:
- **Proper nouns**: "Dukakis", "Melnicove"
- **Acronyms**: "WBUR"
- **Numbers**: "800", "1971"
- **Domain-specific terms**: "politicize"

MFA cannot align these words accurately without their pronunciations.

### Solution: G2P + Manual Entries

#### Step 1: Identify OOV Words

After running validation:

```bash
cat oov_report/oovs_found_english_us_arpa.txt
```

**Example output:**
```
dukakis
politicize
maffy
wbur
melnicove
800
35
300
1971
```

#### Step 2: Generate Pronunciations with G2P

G2P (Grapheme-to-Phoneme) model predicts pronunciations:

```bash
mfa g2p oov_report/oovs_found_english_us_arpa.txt \
       english_us_arpa \
       oov_pronunciations.txt
```

**Generated pronunciations:**
```
dukakis     D UW0 K AA1 K IH0 S
politicize  P AH0 L IH1 T IH0 S AY2 Z
maffy       M AE1 F IY0
wbur        W AH0 B ER0
melnicove   M EH1 L N IH0 K OW2 V
```

**Note:** Numbers (e.g., "800") will appear as `<unk>` because G2P cannot handle them.

#### Step 3: Add Manual Pronunciations

For numbers and corrections, manually edit `custom_oov_dictionary.txt`:

```
800   EY1 T HH AH1 N D R AH0 D
35    TH ER1 T IY0 F AY1 V
300   TH R IY1 HH AH1 N D R AH0 D
1971  N AY1 N T IY1 N S EH1 V AH0 N T IY0 W AH1 N
```

**ARPAbet Phoneme Reference:**
- Vowels: `AA, AE, AH, AO, AW, AY, EH, ER, EY, IH, IY, OW, OY, UH, UW`
- Consonants: `B, CH, D, DH, F, G, HH, JH, K, L, M, N, NG, P, R, S, SH, T, TH, V, W, Y, Z, ZH`
- Stress: `0` (no stress), `1` (primary), `2` (secondary)

#### Step 4: Re-run Alignment with OOV Dictionary

```bash
mfa align corpus \
         english_us_arpa \
         english_us_arpa \
         output_with_oov \
         --dictionary_path custom_oov_dictionary.txt \
         --clean
```

Alternatively, merge OOV pronunciations into the existing dictionary:

```bash
cat oov_pronunciations.txt custom_oov_dictionary.txt > merged_dictionary.txt
mfa align corpus merged_dictionary.txt english_us_arpa output_with_oov --clean
```

## Output Files

### TextGrid Files

TextGrid files are Praat-compatible annotation files with two tiers:

1. **Words tier**: Word-level boundaries
2. **Phones tier**: Phoneme-level boundaries

**Example structure:**
```
File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
xmax = 4.13
tiers? <exists>
size = 2

item [1]:
    class = "IntervalTier"
    name = "words"
    intervals: size = 7
    intervals [1]:
        xmin = 0.00
        xmax = 0.44
        text = ""
    intervals [2]:
        xmin = 0.44
        xmax = 0.53
        text = "i"
    ...
```

### Alignment Quality Metrics

`output/alignment_analysis.csv` contains per-file statistics:

| Metric | Description |
|--------|-------------|
| **file** | Audio filename |
| **duration** | Total duration (seconds) |
| **num_words** | Number of words aligned |
| **num_phones** | Number of phonemes |
| **speech_log_likelihood** | Acoustic model confidence (higher = better) |
| **oovs_found** | Number of OOV words |

**Example:**
```csv
file,duration,num_words,num_phones,speech_log_likelihood,oovs_found
F2BJRLP1,25.3,125,487,-45.809,3
ISLE_SESS0131_BLOCKD02_01_sprt1,4.13,5,17,-43.216,0
```

### Opening in Praat

1. Download and install [Praat](https://www.fon.hum.uva.nl/praat/)
2. Open Praat → Read → Open TextGrid file
3. Select `output/F2BJRLP1.TextGrid`
4. Optional: Open corresponding audio file
5. View → Zoom and navigate to inspect alignments

**Praat Shortcuts:**
- `Tab` - Play selection
- `Ctrl+N` - Next boundary
- `Ctrl+B` - Previous boundary
- Mouse drag - Zoom into region

## Dataset Information

### Overview

| File | Duration | Words | Type | Content |
|------|----------|-------|------|---------|
| **F2BJRLP1.wav** | 25.3s | 125 | Broadcast news | Massachusetts Supreme Court judicial selection |
| **F2BJRLP2.wav** | 28.6s | 138 | Broadcast news | Governor Dukakis appointments |
| **F2BJRLP3.wav** | 30.7s | 152 | Broadcast news | Chief Justice Hennessy's legacy |
| **ISLE_SESS0131_01** | 4.13s | 5 | Minimal pair | "I said WHITE not BAIT" |
| **ISLE_SESS0131_02** | 3.98s | 5 | Minimal pair | "I said BET not BAIT" |
| **ISLE_SESS0131_03** | 4.60s | 5 | Minimal pair | "I said BAIT not BEAT" |

### Audio Characteristics

- **Format**: WAV (PCM)
- **Channels**: Mono (1 channel)
- **Sample Rate**: 32,000 Hz
- **Bit Depth**: 16-bit
- **Total Duration**: ~97 seconds

### Transcript Characteristics

- **Format**: Plain text (.txt)
- **Encoding**: UTF-8
- **Case**: Uppercase
- **Punctuation**: Minimal (periods, commas)
- **OOV Words**: 9 unique words across all files

## Project Structure

```
.
├── Assignment.pdf                    # Original assignment description
├── README.md                         # This documentation
├── REPORT.md                         # Detailed analysis report
├── .gitignore                        # Git ignore rules
│
├── run_mfa_alignment.sh              # Automation script
│
├── wav/                              # Original audio files (6 files)
├── transcripts/                      # Original transcripts (3 files)
├── corpus/                           # MFA-ready corpus
│
├── output/                           # Alignment before OOV handling
│   ├── *.TextGrid                   # Praat annotation files
│   └── alignment_analysis.csv       # Quality metrics
│
├── output_with_oov/                  # Alignment after OOV handling
│   ├── *.TextGrid
│   └── alignment_analysis.csv
│
├── oov_report/                       # OOV analysis
│   ├── oovs_found_english_us_arpa.txt
│   └── corpus_data.csv
│
├── oov_pronunciations.txt            # G2P generated
└── custom_oov_dictionary.txt         # Manual entries
```

## Troubleshooting

### Common Issues

#### 1. `mfa: command not found`

**Solution:**
```bash
# Ensure conda environment is activated
conda activate mfa

# Or reinstall MFA
conda install -c conda-forge montreal-forced-aligner -y
```

#### 2. `Model 'english_us_arpa' not found`

**Solution:**
```bash
# Download required models
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa model download g2p english_us_arpa
```

#### 3. `No alignments were generated`

**Possible causes:**
- Audio/transcript mismatch (different content)
- Audio quality issues (too noisy)
- Incorrect file pairing (mismatched names)

**Solution:**
```bash
# Validate corpus first
mfa validate corpus english_us_arpa --output_directory debug

# Check validation report
cat debug/corpus_data.csv
```

#### 4. `Too many OOV words`

**Solution:**
- Use G2P model: `mfa g2p oov_words.txt english_us_arpa output.txt`
- Add custom pronunciations to dictionary
- Consider using a different/larger dictionary

#### 5. `Alignment quality is poor`

**Indicators:**
- Large timing gaps
- Many skipped words
- Very negative log-likelihood scores

**Solutions:**
- Verify transcript accuracy (no typos)
- Check audio quality (sufficient SNR)
- Ensure correct speaker language/accent model
- Try different acoustic models

### Getting Help

- **MFA Documentation**: https://montreal-forced-aligner.readthedocs.io/
- **MFA GitHub Issues**: https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/issues
- **Praat Manual**: https://www.fon.hum.uva.nl/praat/manual/

## Resources

### Official Documentation

- [MFA Documentation](https://montreal-forced-aligner.readthedocs.io/)
- [MFA GitHub Repository](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner)
- [Praat Software](https://www.fon.hum.uva.nl/praat/)
- [ARPAbet Phoneme Set](https://en.wikipedia.org/wiki/ARPABET)

### Academic References

- **MFA Paper**: McAuliffe, M., Socolof, M., Mihuc, S., Wagner, M., & Sonderegger, M. (2017). *Montreal Forced Aligner: Trainable Text-Speech Alignment Using Kaldi*. Interspeech 2017.
- **HMM-GMM Alignment**: Young, S., et al. (2006). *The HTK Book*. Cambridge University Press.

### Useful Tools

- **Praat**: Phonetic analysis and visualization
- **Audacity**: Audio editing and preprocessing
- **SoX**: Command-line audio format conversion

### Video Tutorials

- [MFA Tutorial - Forced Alignment Basics](https://www.youtube.com/results?search_query=montreal+forced+aligner+tutorial)
- [Praat Tutorial - TextGrid Navigation](https://www.youtube.com/results?search_query=praat+textgrid+tutorial)

---

## License

MIT License - see LICENSE file for details

## Citation

If you use this code or methodology in your research, please cite:

```bibtex
@misc{mfa_forced_alignment_2025,
  title={Forced Alignment using Montreal Forced Aligner},
  author={IIITH Speech Processing Assignment},
  year={2025},
  howpublished={\url{https://github.com/yourusername/mfa-forced-alignment}}
}
```

---

**Questions or Issues?** Please open an issue on GitHub or contact the maintainers.

**Last Updated:** February 2025
