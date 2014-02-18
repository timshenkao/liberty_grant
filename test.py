from unittest import TestCase, main
import filecomparator


class TestNode(TestCase):

    def setUp(self):
        self.n = filecomparator.Node('sbin')

    def test_init(self):
        self.assertEqual(self.n.name,'sbin','Error when initializing Node')

class TestPrintResults(TestCase):

    def setUp(self):
        self.n = filecomparator.Node('sbin')

    def test_print_filename(self):
        self.assertRaises(TypeError, filecomparator.print_results, 7777,
            self.n)

    def test_print_node(self):
        self.assertRaises(TypeError, filecomparator.print_results, 'file1.txt',
            7777)


class TestReadFile(TestCase):

    def test_filename(self):
        self.assertRaises(TypeError, filecomparator.read_file, 100000, 10)


class TestFindDissimilarities(TestCase):

    def setUp(self):
        from multiprocessing import JoinableQueue
        self.q = JoinableQueue()

    def test_queue_type(self):
        self.assertRaises(TypeError, filecomparator.find_dissimilarities, 5)

    def test_queue_immediate_end(self):
        self.n = filecomparator.Node('')
        for _ in xrange(2):
            self.q.put('shit happens')
        self.assertEqual(self.n.name,
            filecomparator.find_dissimilarities(self.q).name)
        self.assertEqual(self.n.directories,
            filecomparator.find_dissimilarities(self.q).directories)
        self.assertEqual(self.n.files,
            filecomparator.find_dissimilarities(self.q).files)

    def test_queue_empty(self):
        self.q.put('')
        self.assertRaises(IndexError, filecomparator.find_dissimilarities,
                            self.q)


class TestMain(TestCase):

    def test_filenames(self):
        self.assertRaises(TypeError, filecomparator.main, [])

    def test_number_filenames(self):
        self.assertRaises(StandardError, filecomparator.main, (1,1,1,1))


if __name__ == '__main__':
    main()