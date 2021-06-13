#!/bin/bash

gnuplot -e "set terminal png size 1600, 1200;\
    set key font ', 20';\
    set tics font ', 20';\
    set output 'plot_cost';\
    plot\
    'stats.txt' u 1:4 w l lw 2 lc 3 t 'train cost',\
    'stats.txt' u 1:8 w l lw 2 lc 6 t 'test cost',
    'stats.txt' u 1:2 w l lw 3 lc 2 t 'avg train cost',\
    'stats.txt' u 1:6 w l lw 3 lc 7 t 'avg test cost'"
    
gnuplot -e "set terminal png size 1600, 1200;\
    set key font ', 20';\
    set tics font ', 20';\
    set output 'plot_winrate';\
    plot \
    'stats.txt' u 1:5 w l lw 2 lc 3 t 'train win rate',\
    'stats.txt' u 1:9 w l lw 2 lc 6 t 'test win rate',
    'stats.txt' u 1:3 w l lw 3 lc 2 t 'avg train win rate',\
    'stats.txt' u 1:7 w l lw 3 lc 7 t 'avg test win rate'"
