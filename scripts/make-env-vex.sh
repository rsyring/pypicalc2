# Usage:
# source scripts/make-env-vex.sh
rmvirtualenv pypicalc2
vex -m --python python3.4 pypicalc2 pip install "git+https://github.com/level12/wheelhouse#egg=Wheelhouse"
vex pypicalc2 wheelhouse install -- -r requirements/dev-env.txt
vex pypicalc2 pip install -e .
vex -r pypicalc2
