# Installation Guide - Montreal Forced Aligner

Complete installation instructions for setting up the MFA forced alignment environment.

## Quick Installation (Recommended)

### For macOS/Linux

```bash
# 1. Install Miniconda (if not already installed)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh

# 2. Clone this repository
git clone <your-repo-url>
cd mfa-forced-alignment

# 3. Create conda environment from file
conda env create -f environment.yml

# 4. Activate environment
conda activate mfa

# 5. Download required models
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa model download g2p english_us_arpa

# 6. Verify installation
mfa version
```

## Manual Installation

### Step 1: Install Conda

**Option A: Miniconda (Lightweight)**
- Download from: https://docs.conda.io/en/latest/miniconda.html
- Follow platform-specific instructions

**Option B: Anaconda (Full distribution)**
- Download from: https://www.anaconda.com/download
- Includes additional scientific packages

### Step 2: Create Environment

```bash
# Create fresh environment with MFA
conda create -n mfa -c conda-forge montreal-forced-aligner python=3.10 -y

# Activate the environment
conda activate mfa
```

### Step 3: Download Models

```bash
# Acoustic models
mfa model download acoustic english_us_arpa

# Pronunciation dictionaries
mfa model download dictionary english_us_arpa

# G2P models
mfa model download g2p english_us_arpa

# List downloaded models
mfa model list
```

### Step 4: Verify Installation

```bash
# Check MFA version
mfa version

# Should output something like: 2.x.x

# Test with help command
mfa align --help
```

## Alternative: pip Installation

If you prefer pip over conda:

```bash
# Create virtual environment
python3 -m venv mfa_env
source mfa_env/bin/activate  # On Windows: mfa_env\Scripts\activate

# Install MFA
pip install montreal-forced-aligner

# Download models (same as above)
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa model download g2p english_us_arpa
```

## Installing Praat (Optional)

For visualizing TextGrid files:

### macOS
```bash
# Using Homebrew
brew install --cask praat

# Or download from official site
# https://www.fon.hum.uva.nl/praat/
```

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install praat

# Or build from source
```

### Windows
- Download installer from: https://www.fon.hum.uva.nl/praat/
- Run the .exe installer

## Troubleshooting

### Issue: `mfa: command not found`

**Solution:**
```bash
# Ensure conda environment is activated
conda activate mfa

# If still not found, reinstall
conda install -c conda-forge montreal-forced-aligner -y
```

### Issue: `libsndfile` or `libflac` errors

**Solution (macOS):**
```bash
brew install libsndfile flac
```

**Solution (Linux):**
```bash
sudo apt-get install libsndfile1 libflac-dev
```

### Issue: Model download fails

**Solution:**
```bash
# Try with verbose output
mfa model download acoustic english_us_arpa --verbose

# Or manually download from GitHub
# https://github.com/MontrealCorpusTools/mfa-models/releases
```

### Issue: Permission errors on macOS

**Solution:**
```bash
# Grant terminal full disk access
# System Preferences → Security & Privacy → Privacy → Full Disk Access
# Add Terminal.app or your terminal emulator
```

## System Requirements

- **OS**: macOS 10.14+, Linux (Ubuntu 18.04+), Windows 10+ (via WSL2)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 2 GB for MFA + models
- **Python**: 3.8 to 3.11 (3.10 recommended)

## Environment Variables

Optional environment variables for customization:

```bash
# Set MFA model directory (default: ~/.mfa)
export MFA_ROOT_DIR=/path/to/custom/location

# Set temporary directory
export TMPDIR=/path/to/tmp

# Increase verbosity
export MFA_VERBOSE=1
```

## Updating MFA

```bash
# Update to latest version
conda activate mfa
conda update -c conda-forge montreal-forced-aligner

# Or with pip
pip install --upgrade montreal-forced-aligner
```

## Uninstallation

```bash
# Remove conda environment
conda deactivate
conda env remove -n mfa

# Remove model files (optional)
rm -rf ~/.mfa
```

## Additional Resources

- **MFA Documentation**: https://montreal-forced-aligner.readthedocs.io/
- **GitHub Repository**: https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner
- **Model Zoo**: https://github.com/MontrealCorpusTools/mfa-models

## Getting Help

If you encounter issues:

1. Check the official documentation
2. Search GitHub issues: https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/issues
3. Post on the discussion forum

---

**Last Updated**: February 2025
