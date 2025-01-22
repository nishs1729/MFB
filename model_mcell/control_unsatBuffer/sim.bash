for fname in `ls | grep xmain_n | grep nAZ_3`; do 
    echo $fname
    seq 300 | parallel -j35 mcell32 ${fname} -seed {} -logfreq 10000
done
