 
import unittest

def buildConnectionString(p_in):
    if p_in == "err":
        raise AttributeError("err message form wp")
    else:
        return "ok"
         
class GoodInput(unittest.TestCase):
	def testBlank(self): 
		self.assertEqual("ok", buildConnectionString(""))
         
class BadInput(unittest.TestCase):
    def testString(self): 
        self.assertRaises(AttributeError, buildConnectionString, "err")

if __name__ == "__main__": 
	unittest.main()

