#-------------------------------------------------------------------------------
# Name:        filecomparator
# Purpose:
#
# Author:      shenkao.t
#
# Created:     18.02.2014
# Copyright:   (c) shenkao.t 2014
# Licence:     BSD 3-clause
#-------------------------------------------------------------------------------

from multiprocessing import Process, JoinableQueue, Queue


class Node(object):
    """
    Node represents directory in file system
    """
    __slots__ = 'name', 'directories', 'files'

    def __init__(self, name=''):
        """
        Contructor for our nodes
        :param name: name of directory
        :type name: str
        """
        self.name = name # name of directory
        self.directories = {} # child directories of this directory
        self.files = [] # files in this directory


def print_results(file_name, base_n):
    """
    Procedure that saves the results to file
    :param file_name: file's name
    :type file_name: str
    :param base_n: base node to begin with
    :type base_n: Node
    """
    if not isinstance(file_name, basestring):
        raise TypeError('Input correct file name')
    if not isinstance(base_n, Node):
        raise TypeError('You should submit results as Node object ')

    stack = []
    stack.append(('', base_n))

    with open(file_name, 'w') as output_file:
        while len(stack) > 0:
            path, current_node = stack.pop()
            for filen in current_node.files:
                output_file.write(path + current_node.name + '/' + filen + '\n')
                print(path + current_node.name + '/' + filen)
            for k, v in current_node.directories.iteritems():
                stack.append((path + current_node.name + '/',v))


def read_file(queue_transmit,file_name):
    """
    Procedure that reads from file
    :param file_name: file's name to  read
    :type file_name: str
    :param queue_transmit: queue to put splitted line in
    :type queue_transmit: Queue
    """
    if not isinstance(file_name, basestring):
        raise TypeError('Input correct file name')
    if not (isinstance(queue_transmit, (Queue, JoinableQueue))):
        raise TypeError('You should use multiprocessing.Queue or \
                         multiprocessing.JoinableQueue')

    with open(file_name, 'r') as input_file:
        for line in input_file:
            # split input line
            line_splitted = line.strip().split('/')
            queue_transmit.put(line_splitted[1:])
    queue_transmit.put('shit happens')


def find_dissimilarities(queue_transmit):
    """
    Procedure that creates some kind of tree to store new and deleted files
    :param queue_transmit: queue to get data from
    :type queue_transmit: Queue
    :return base_node: base node of out 'tree'
    :rtype base_node: Node
    """
    if not (isinstance(queue_transmit, (Queue, JoinableQueue))):
        raise TypeError('You should use multiprocessing.Queue or \
                         multiprocessing.JoinableQueue')

    stop = []
    base_node = Node('') # I don't name it root node to avoid ambiguities

    while len(stop) < 2:
        current_node = base_node
        data_to_get = queue_transmit.get()
        if data_to_get == 'shit happens':
            stop.append('shit happens')
            continue
        elif len(data_to_get) == 0:
            continue
        else:
            for elem in data_to_get[:-1]: # iterate through directories
                if elem not in current_node.directories:
                    # create node for previously unseen directory
                    current_node.directories[elem] = Node(elem)
                current_node = current_node.directories[elem]

            try:
                # if such file has been already seen, delete it
                current_node.files.remove(data_to_get[-1])
            except ValueError:
                # add new file
                current_node.files.append(data_to_get[-1])
    return base_node


def main(filenames):
    """
    Main function.
    :param filenames: file names
    :type filenames: tuple
    """
    if not isinstance(filenames, tuple):
        raise TypeError("Files' names must be present like tuple")
    if len(filenames) <> 3:
        raise StandardError("Number of files' names must be three")

    queue_j = JoinableQueue()
    process_list = []

    for filen in filenames[:-1]:
        p = Process(target=read_file, args=(queue_j, filen))
        process_list.append(p)

    for p in process_list:
        p.start()

    base_n = find_dissimilarities(queue_j)

    for p in process_list:
        p.join()

    print_results(filenames[-1], base_n)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print(' You should specify 2 input file names and 1 output file name')
        sys.exit(1)
    else:
        main(tuple(sys.argv[1:4]))