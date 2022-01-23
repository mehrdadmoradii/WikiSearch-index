from unittest import TestCase
from CicularQueue import CircularQueue


class TestCircularQueue(TestCase):

    def setUp(self) -> None:
        self.queue = CircularQueue()

    def tearDown(self) -> None:
        self.queue = CircularQueue()

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(10)
        self.assertFalse(self.queue.is_empty())
        self.queue.dequeue()
        self.assertTrue(self.queue.is_empty())

    def test_peek(self):
        with self.assertRaises(Exception):
            self.queue.peek()
        self.queue.enqueue(22)
        self.queue.enqueue(33)
        self.assertEqual(self.queue.peek(), 22)

    def test_dequeue(self):
        with self.assertRaises(Exception):
            self.queue.dequeue()
        self.queue.enqueue(0)
        self.assertEqual(self.queue.dequeue(), 0)
        for i in range(10):
            self.queue.enqueue(i)
        for i in range(10):
            self.assertEqual(self.queue.dequeue(), i)


    def test_enqueue(self):
        for i in range(-20, 20, 1):
            self.queue.enqueue(i)
        for i in range(-20, 20, 1):
            self.assertEqual(self.queue.dequeue(), i)
