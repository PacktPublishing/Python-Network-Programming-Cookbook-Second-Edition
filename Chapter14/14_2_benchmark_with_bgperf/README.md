bgperf
========

bgperf is a performance measurement tool for BGP implementation.

* [How to install](#how_to_install)
* [How to use](#how_to_use)
* [How bgperf works](https://github.com/osrg/bgperf/blob/master/docs/how_bgperf_works.md)
* [Benchmark remote target](https://github.com/osrg/bgperf/blob/master/docs/benchmark_remote_target.md)
* [MRT injection](https://github.com/osrg/bgperf/blob/master/docs/mrt.md)

## Prerequisites

* Python 3.5 or later
* Docker

##  <a name="how_to_install">How to install

```bash
$ git clone https://github.com/pradeeban/bgperf
$ cd bgperf
$ pip install -r pip-requirements.txt
$ sudo python3 bgperf.py --help
usage: bgperf.py [-h] [-b BENCH_NAME] [-d DIR]
                 {doctor,prepare,update,bench,config} ...

BGP performance measuring tool

positional arguments:
  {doctor,prepare,update,bench,config}
    doctor              check env
    prepare             prepare env
    update              pull bgp docker images
    bench               run benchmarks
    config              generate config

optional arguments:
  -h, --help            show this help message and exit
  -b BENCH_NAME, --bench-name BENCH_NAME
  -d DIR, --dir DIR
$ sudo python3 bgperf.py prepare
$ sudo python3 bgperf.py doctor
docker version ... ok (1.9.1)
bgperf image ... ok
gobgp image ... ok
bird image ... ok
quagga image ... ok
```

## <a name="how_to_use">How to use

Use `bench` command to start benchmark test.
By default, `bgperf` benchmarks [GoBGP](https://github.com/pradeeban/gobgp).
`bgperf` boots 100 BGP test peers each advertises 100 routes to `GoBGP`.

```bash
$ sudo python3 bgperf.py bench
run tester
tester booting.. (100/100)
run gobgp
elapsed: 16sec, cpu: 0.20%, mem: 580.90MB
elapsed time: 11sec
```

To change a target implementation, use `-t` option.
Currently, `bgperf` supports [BIRD](http://bird.network.cz/) and [Quagga](http://www.nongnu.org/quagga/)
other than GoBGP.

```bash
$ sudo python3 bgperf.py bench -t bird
run tester
tester booting.. (100/100)
run bird
elapsed: 16sec, cpu: 0.00%, mem: 147.55MB
elapsed time: 11sec
$ sudo python3 bgperf.py bench -t quagga
run tester
tester booting.. (100/100)
run quagga
elapsed: 33sec, cpu: 0.02%, mem: 477.93MB
elapsed time: 28sec
```

To change a load, use following options.

* `-n` : the number of BGP test peer (default 100)
* `-p` : the number of prefix each peer advertise (default 100)
* `-a` : the number of as-path filter (default 0)
* `-e` : the number of prefix-list filter (default 0)
* `-c` : the number of community-list filter (default 0)
* `-x` : the number of ext-community-list filter (default 0)

```bash
$ sudo python3 bgperf.py bench -n 200 -p 50
run tester
tester booting.. (200/200)
run gobgp
elapsed: 23sec, cpu: 0.02%, mem: 1.26GB
elapsed time: 18sec
```

For a comprehensive list of options, run `sudo python3 bgperf.py bench --help`.
