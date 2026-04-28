#!/bin/bash
#SBATCH --job-name=Qwen3_Para4B    # Job name
#SBATCH -p gpu --gres=gpu:1
#SBATCH --mem=128G
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -t 24:00:00

DEVELOPER_DIR="/oscar/data/sbach/zning3/Rerank_Strategies"
CONDA_ENV="caig_conda"

module load miniforge3/25.3.0-3
source ${MAMBA_ROOT_PREFIX}/etc/profile.d/conda.sh

conda activate "$CONDA_ENV"

# Fix ColBERT C++ extension compilation issues
export COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True
export COLBERT_LOAD_TORCH_EXTENSION=0  # Disable JIT compilation to avoid freezing
export TORCH_EXTENSIONS_DIR="/tmp/$USER/torch_extensions"  # Use safe cache directory

# Run the Python script using the developer's directory
echo "Starting"
# python "$DEVELOPER_DIR/Qwen_PointSix.py"
# python "$DEVELOPER_DIR/Qwen_FourBil.py"
python "$DEVELOPER_DIR/Qwen_EightBil.py"

# Check exit status
if [ $? -eq 0 ]; then
    echo "DONE"
else
    echo "Indexing failed with exit code $?"
    exit 1
fi
