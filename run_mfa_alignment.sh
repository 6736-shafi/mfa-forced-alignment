#!/bin/bash
# run_mfa_alignment.sh - Script to run complete MFA alignment pipeline

set -e

# Configuration
CORPUS_DIR="corpus"
OUTPUT_DIR="output"
OUTPUT_OOV_DIR="output_with_oov"
OOV_REPORT_DIR="oov_report"
ACOUSTIC_MODEL="english_us_arpa"
DICTIONARY="english_us_arpa"
G2P_MODEL="english_us_arpa"

echo "=========================================="
echo "MFA Forced Alignment Pipeline"
echo "=========================================="

# Step 1: Create corpus directory structure
echo "[1/6] Preparing corpus..."
mkdir -p "$CORPUS_DIR"
cp wav/*.wav "$CORPUS_DIR/"

# Copy and convert transcripts to .lab format
for f in transcripts/*.TXT transcripts/*.txt; do
    [ -f "$f" ] && cp "$f" "$CORPUS_DIR/$(basename "${f%.*}").lab"
done

# Clean transcripts (single line format)
for f in "$CORPUS_DIR"/*.lab; do
    tr '\n\r' ' ' < "$f" | sed 's/  */ /g; s/^ *//; s/ *$//' > "$f.tmp"
    mv "$f.tmp" "$f"
done

echo "   Corpus prepared with $(ls -1 $CORPUS_DIR/*.wav 2>/dev/null | wc -l) audio files"

# Step 2: Download models (if needed)
echo "[2/6] Checking MFA models..."
mfa model download acoustic "$ACOUSTIC_MODEL" 2>/dev/null || true
mfa model download dictionary "$DICTIONARY" 2>/dev/null || true
mfa model download g2p "$G2P_MODEL" 2>/dev/null || true

# Step 3: Validate corpus and check OOV
echo "[3/6] Validating corpus and checking OOV words..."
mkdir -p "$OOV_REPORT_DIR"
mfa validate "$CORPUS_DIR" "$DICTIONARY" --output_directory "$OOV_REPORT_DIR" --clean

# Step 4: Run initial alignment (before OOV handling)
echo "[4/6] Running forced alignment (before OOV handling)..."
mfa align "$CORPUS_DIR" "$DICTIONARY" "$ACOUSTIC_MODEL" "$OUTPUT_DIR" --clean

# Step 5: Generate G2P pronunciations for OOV words
echo "[5/6] Generating G2P pronunciations for OOV words..."
if [ -f "$OOV_REPORT_DIR/oovs_found_${DICTIONARY}.txt" ]; then
    mfa g2p "$OOV_REPORT_DIR/oovs_found_${DICTIONARY}.txt" "$G2P_MODEL" oov_pronunciations.txt
    echo "   G2P pronunciations saved to oov_pronunciations.txt"
fi

# Step 6: Re-run alignment (after OOV handling)
echo "[6/6] Running forced alignment (after OOV handling)..."
mfa align "$CORPUS_DIR" "$DICTIONARY" "$ACOUSTIC_MODEL" "$OUTPUT_OOV_DIR" --clean

echo ""
echo "=========================================="
echo "Pipeline Complete!"
echo "=========================================="
echo "TextGrid outputs:"
echo "  - Before OOV: $OUTPUT_DIR/"
echo "  - After OOV:  $OUTPUT_OOV_DIR/"
echo "OOV Report:     $OOV_REPORT_DIR/"
echo ""
