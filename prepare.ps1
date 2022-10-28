$env:KMP_DUPLICATE_LIB_OK = $true
code .
cd .\src
conda activate paddle_env
echo $env:KMP_DUPLICATE_LIB_OK
