for fn in */LC_MESSAGES/*.po
do
  nfn=`echo $fn | sed s/.po/.mo/`
  msgfmt -o $nfn $fn
done