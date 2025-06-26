import unittest
from src.chapter_16.object_pool import ObjectPool, PooledObject

class TestObjectPool(unittest.TestCase):
    def setUp(self):
        self.pool = ObjectPool(lambda: PooledObject(42), max_size=3)

    def test_acquire_and_release(self):
        obj1 = self.pool.acquire()
        obj2 = self.pool.acquire()
        self.assertIsNotNone(obj1)
        self.assertIsNotNone(obj2)
        self.assertTrue(obj1.in_use)
        self.assertTrue(obj2.in_use)
        self.assertEqual(self.pool.available(), 1)
        self.pool.release(obj1)
        self.assertFalse(obj1.in_use)
        self.assertEqual(self.pool.available(), 2)

    def test_pool_exhaustion(self):
        objs = [self.pool.acquire() for _ in range(3)]
        self.assertEqual(self.pool.available(), 0)
        self.assertIsNone(self.pool.acquire())
        for obj in objs:
            self.pool.release(obj)
        self.assertEqual(self.pool.available(), 3)

    def test_release_and_reacquire(self):
        obj = self.pool.acquire()
        self.pool.release(obj)
        obj2 = self.pool.acquire()
        self.assertIs(obj, obj2)

    def test_all_objects_unique(self):
        objs = [self.pool.acquire() for _ in range(3)]
        self.assertEqual(len(set(id(obj) for obj in objs)), 3)

if __name__ == "__main__":
    unittest.main(verbosity=2) 