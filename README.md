# TODO CECILIA keep display visually the last commit number
# TODO CECILIA onmouseclick: commit
# TODO CECILIA qrcode + share + video WHEN?

```
mkdir keys
ssh-keygen -t ed25519 -C "guilherme.silveira@gmail.com" -f keys/id_ed25519
ssh-add keys/id_ed25519
pbcopy < .ssh/id_ed25519.pub
open https://github.com/guilhermesilveira/commiter-results/settings/keys
```

```
cd output
git init
echo "# Main" > README.md
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:guilhermesilveira/commiter-results.git
git push -u origin main
```

```
git tag -d $(git tag -l)
git fetch
git push origin --delete $(git tag -l) 
git tag -d $(git tag -l)



git tag | xargs git tag -d


rm -fr output/.git
rm -f keys/*
```