local("cd api/ && make dep")
docker_build('opengui-api', './api')
docker_build('opengui-gui', './gui')

k8s_yaml(kustomize('kubernetes/tilt'))

k8s_resource('api', port_forwards=['17971:80', '17939:5678'])
k8s_resource('gui', port_forwards=['7971:80'], resource_deps=['api'])
