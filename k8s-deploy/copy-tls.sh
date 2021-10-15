secret_name=$1
src=$2
dest=$3
kubectl get secret "${secret_name}" -n "${src}" -o yaml \
	| sed s/"namespace: ${src}"/"namespace: ${dest}"/\
	| kubectl apply -n ${dest} -f -
