from .tasks import prepare_csv_file_queue, post_csv_files
import unittest
from .models import Mediator, FilePath

# Create your tests here.
class TestFileHandling(unittest.TestCase):
    FilePath.objects.all().delete()

    # mediator = Mediator.objects.get(id=1)
    # FilePath.objects.create(mediator=mediator, file_path='/Users/user/Documents/EMR/err', path_type='err_dir')
    # FilePath.objects.create(mediator=mediator, file_path='/Users/user/Documents/EMR/in', path_type='in_dir')
    # FilePath.objects.create(mediator=mediator, file_path='/Users/user/Documents/EMR/out', path_type='out_dir')
    # FilePath.objects.create(mediator=mediator, file_path='/Users/user/Documents/EMR/', path_type='root_dir')

    mediator = Mediator.objects.get(id=1)
    FilePath.objects.create(mediator=mediator, file_path='/home/danny/EMR/err', path_type='err_dir')
    FilePath.objects.create(mediator=mediator, file_path='/home/danny/EMR/in', path_type='in_dir')
    FilePath.objects.create(mediator=mediator, file_path='/home/danny/EMR/out', path_type='out_dir')
    FilePath.objects.create(mediator=mediator, file_path='/home/danny/EMR/', path_type='root_dir')

    def test_file_handling(self):

        test_function = prepare_csv_file_queue()
        self.assertEqual(test_function, 200)


    def test_posting_csv(self):

        test_function = post_csv_files()
        self.assertEqual(test_function, 200)







