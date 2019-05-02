for k in {5..10}
do
	python "centrality_based_infl_max.py" $k
done

for k in {5..10}
do
	for m in {3..6}
	do
		python "im1.py" $k $m
	done
done

for k in {5..10}
do
	for m in {3..6}
	do
		python "mim1.py" $k $m
	done
done

for k in {5..10}
do
	for m in {3..6}
	do
		for n in {3..5}
		do
			python "mim2.py" $k $m
		done
	done
done