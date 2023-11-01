import unittest
import main as app

class Test(unittest.TestCase):
    def test_line_cleanup(self):
        line = '[1m  # module.random.random_id.id[0m will be [1m[31mdestroyed[0m'
        expect = 'module.random.random_id.id'
        actual = app.line_cleanup(line)

        print('expect: ' + expect)
        print('actual: ' + actual)
        self.assertEqual(expect, actual)

    def test_destroy_commands(self):    
        lines = ['[1m  # module.random.random_id.id[0m will be [1m[31mdestroyed[0m']
        expect = ['terraform state rm -ignore-remote-version "module.random.random_id.id"']
        actual = app.destroy_commands(lines)
        self.assertEqual(expect, actual)

    def test_create_commands(self):    
        lines = ['[1m  # module.ipam[0].aws_vpc_ipam.main[0m will be created']
        expect = ['terraform import -ignore-remote-version "module.ipam[0].aws_vpc_ipam.main" ""']
        actual = app.create_commands(lines)
        self.assertEqual(expect, actual)
        

if __name__ == '__main__':
    unittest.main()