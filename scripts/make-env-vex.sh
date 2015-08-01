# Usage:
# source scripts/make-env-vex.sh
rmvirtualenv bookorders
vex -m --python python3.4 bookorders pip install "git+https://github.com/level12/wheelhouse#egg=Wheelhouse"
vex hllapi wheelhouse install -- -r requirements/dev-env.txt
vex hllapi pip install -e .
vex -r bookorders
