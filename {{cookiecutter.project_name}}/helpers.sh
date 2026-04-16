# Writes all contents of outputs/ directory to s3 bucket for easy sharing with newsroom colleagues
# s3 path will be data-reporting-datakit-output-v2-prod/{repo-name}/{current-branch-name}/
alias outputs-push="chmod +x ./outputs.sh && ./outputs.sh"

# Help message for these commands. Excludes some that are meant to be used
# only internally by this script
alias datakit-help="echo
echo \"datakit helper commands\"
echo \"======================\"
echo \"outputs-push - write all contents of the outputs/ directory to s3\"
"
