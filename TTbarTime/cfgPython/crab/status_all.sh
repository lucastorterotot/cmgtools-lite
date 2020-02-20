
cmd=$(find /home/cms/acarle/ttbarAnalysis/CMSSW_9_4_11_cand1/src/CMGTools/TTbarTime/cfgPython/crab/ -type d -iname \*$1\*)

for dir in $cmd
do
    echo $dir"/*/"
    crab status $dir/*/
done
