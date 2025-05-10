from types import SimpleNamespace

def test_func1():
    return 1

class test_class1:
    val1:1
    val2:2
    def testclass1_func1():
        print("test1class func")

person = {"name":"Alice", "cust_func":test_func1}
person2={"name":"dsfsdfs","cust_func":test_func1}

minpserson=min(person,person2)
print(minpserson["name"])