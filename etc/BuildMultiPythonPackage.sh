#!/bin/bash

# List of supported Python versions
SUPPORTED_VERSIONS=("3.7" "3.8" "3.9" "3.10" "3.11" "3.12" "3.13")

# Define build function that accepts Python version as parameter
build_for_python() {
  local VERSION=$1
  echo "Building for Python $VERSION..."
  
  # Create and activate conda environment
  conda create -n py${VERSION//./} python=$VERSION -y
  source /opt/conda/bin/activate py${VERSION/./}
  
  PYTHON=$(which python)
  PY_INC=$(python -c "from sysconfig import get_paths as gp; print(gp()['include'])")
  
  # Build directory
  mkdir -p build_$VERSION
  cd build_$VERSION
  
  cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DPython3_EXECUTABLE=$PYTHON \
    -DPython3_INCLUDE_DIR=$PY_INC \
    -DPython3_FIND_FRAMEWORK=NEVER \
    -DPython3_FIND_STRATEGY=LOCATION \
    -DSWIG_EXECUTABLE=/usr/local/bin/swig \
    -DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} -DBOOST_CSTDFLOAT_NO_LIBQUADMATH_SUPPORT"
  
  make -j$(nproc)

  cd python/openroad-full/
  
  PY_ABI_TAG=$(python -c "import sys; print(f'cp{sys.version_info.major}{sys.version_info.minor}')")
  
  python setup.py bdist_wheel --python-tag=$PY_ABI_TAG
  
  auditwheel repair --disable-isa-ext-check dist/*.whl -w /io/dist

  cd ../../..
  
  # Deactivate conda environment
  conda deactivate
}

# Show usage information
show_usage() {
  echo "Usage: $0 <Python version>"
  echo "Example: $0 3.9"
  echo "Supported Python versions: ${SUPPORTED_VERSIONS[*]}"
}

# Main program
main() {
  # Check if version parameter is provided
  if [ $# -eq 0 ]; then
    echo "Error: No Python version specified"
    show_usage
    exit 1
  fi
  
  VERSION=$1
  
  # Check if the version is supported
  local version_supported=false
  for supported_version in "${SUPPORTED_VERSIONS[@]}"; do
    if [ "$VERSION" == "$supported_version" ]; then
      version_supported=true
      break
    fi
  done
  
  if [ "$version_supported" = false ]; then
    echo "Error: Unsupported Python version: $VERSION"
    show_usage
    exit 1
  fi
  
  # Run build for the specified Python version
  build_for_python $VERSION
}

# Run main program with all command line arguments
main "$@"
