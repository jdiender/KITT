import sys;
from defsignals import signal;

def main() -> int:
    s = signal([0, 1, 2])
    s.naive_plot()
    s = signal([9, 9, 9])
    s.naive_plot()
    return 0;

if __name__ == "__main__":
    sys.exit(main())
