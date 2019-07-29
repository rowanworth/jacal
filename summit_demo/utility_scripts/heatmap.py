import glob
import itertools
import multiprocessing
import os
import sys

from matplotlib import pyplot as plt
import numpy as np


def as_int(s):
    if s in ('0', '00', '000'):
        return 0
    if s.startswith('0'):
        return int(s.lstrip('0'))
    return int(s)


def get_time(line):
    parts = line.split()[0:2]
    day = as_int(parts[0].split('-')[2])
    the_time, ms = parts[1].split(',')
    ms = as_int(ms)
    hh, mm, ss = map(lambda x: as_int(x), the_time.split(':'))
    return day * 24 * 3600 + hh * 3600 + mm * 60 + ss + ms/1000.


def get_events(logfile):

    events = []
    with open(logfile) as f:
        for i, line in enumerate(f):
            if i == 0:
                start = get_time(line)
            elif 'Sending visibility block' in line:
                events.append((get_time(line) - start, 'send_vis'))
            elif 'Relaying heap to sink' in line:
                events.append((get_time(line) - start, 'relay_heap'))
            elif 'Creating standard MS' in line:
                events.append((get_time(line) - start, 'ms_creating'))
            elif 'Measurement Set created' in line:
                events.append((get_time(line) - start, 'ms_created'))
            elif 'Writing visibilities to Measurement Set' in line:
                events.append((get_time(line) - start, 'ms_write'))
            elif 'Closing measurement set' in line:
                events.append((get_time(line) - start, 'ms_closing'))
            elif 'Measurement set closed' in line:
                events.append((get_time(line) - start, 'ms_closed'))

    node = int(os.path.basename(os.path.dirname(logfile)))
    return [(node, t, evt) for t, evt in events]


def heatmap(nodes, times, events):
    nodes = np.array(nodes)
    times = np.array(times)
    events = np.array(events)

    unique_nodes = set(nodes)
    node_range = min(unique_nodes), max(unique_nodes) + 1
    n_nodes = node_range[1] - node_range[0]

    fig = plt.figure(figsize=(100, 36))
    ax = fig.add_subplot(1, 1, 1)
    H, xedges, yedges = np.histogram2d(nodes, times, bins=(n_nodes, 1000))
    ax.imshow(H, cmap='hot')
    fig.savefig('heatmap.pdf')

    for evt in ('send_vis', 'ms_write', 'relay_heap'):
        selection = np.where(events == evt)
        fig = plt.figure(figsize=(100, 6 if evt == 'ms_write' else 36))
        ax = fig.add_subplot(1, 1, 1)
        node_bins = n_nodes / 6 if evt == 'ms_write' else n_nodes
        H, xedges, yedges = np.histogram2d(nodes[selection],
                times[selection], bins=(node_bins, 1000))
        ax.imshow(H, cmap='hot')
        ax.set_yticks(np.arange(0, node_bins, 5))
        fig.savefig('heatmap_%s.pdf' % evt)
        fig.savefig('heatmap_%s.png' % evt)


def main(input_dir):

    all_logs = glob.glob(os.path.join(input_dir, '*', 'dlgNM.log'))
    events = multiprocessing.Pool().map(get_events, all_logs)
    events = itertools.chain(*events)
    nodes, times, events = map(list, zip(*events))
    heatmap(nodes, times, events)

main(sys.argv[1])
