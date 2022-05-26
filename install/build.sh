mkdir output
pushd output || exit 1

git init -b main
echo "# Main" > README.md
git branch -M main
git add README.md
git commit -m "first commit"
git config --global user.email "anonymous.refactorer@gmail.com"
git config --global user.name "Anonymous Refactorer"
git remote add origin git@github.com:guilhermesilveira/commiter-results.git
git push -u origin main

popd || exit 1

pip install -U pip
pip install -r requirements.txt
