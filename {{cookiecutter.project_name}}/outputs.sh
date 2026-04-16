# Construct the full s3 path
working_dir="$(pwd)"
project_repo=${working_dir##*/}
current_branch="$(git rev-parse --abbrev-ref HEAD)"
s3_full_path="s3://data-reporting-datakit-output-v2-prod/${project_repo}/${current_branch}/"

echo "This operation will write the following files to \n${s3_full_path}:\n"
# print list of files in ./outputs/
find ./outputs -type f

# Only warn about overwriting if there are files at the s3 path
num_files=$(aws s3 ls ${s3_full_path} | wc -l)
if [ $num_files -gt 0 ]
then
    echo "\nThere are already some files at this s3 path.\nAny s3 files below with the same name as the ones stored locally will be overwritten by this operation:\n"
    aws s3 ls ${s3_full_path} --recursive
    echo "\nIf you do not wish to overwrite files with the same name, switch to a new branch and run the outputs-push command again."
    echo "Would you like to proceed with the operation, even though it may overwrite files?"
# Otherwise, just ask if user would like to proceed
else
    echo "Would you like to proceed with this write operation?"
fi

select yn in "Yes" "No"; do
    case $yn in
        Yes)
            upload_output=`aws s3 cp outputs/ "${s3_full_path}" --recursive`
            break
            ;;
        No) 
            exit
            ;;
    esac
done

web_index_path="https://washpost.arcpublishing.com/datakit/${project_repo}/${current_branch}/index.html"
if command -v python &>/dev/null; then
    echo "Updating outputs index page... $web_index_path"
    python outputs_index.py ${project_repo}
else
    echo "Python not found, so project index.html file was not updated."
fi
html_path=`echo ${upload_output} | sed 's/upload:/\nupload:/g' | sed 's#outputs\\/##g' | grep '\.html' | head -1 | cut -d ' ' -f 2`

web_quarto_path="https://washpost.arcpublishing.com/datakit/${project_repo}/${current_branch}/${html_path}"
echo "Your Quarto files are likely available at $web_quarto_path"
