import msgpack
import urllib2

def main():
    ids = [3, 2, 24, 7, 9, 4, 109, 20, 10, 11, 12, 13, 97, 22, 106, 23, 19, 21, 14, 16, 17, 102, 105, 93, 104, 103, 15, 95, 5, 18, 6, 8, 1]
    m = msgpack.packb(['test_ov', 'admin', 'admin', 'res.partner', 'read', ids])
    u = urllib2.urlopen('http://localhost:8000/', m)
    s = u.read()
    u.close()
    print(len(m), len(s))
    v = msgpack.unpackb(s)
    print(v)

if __name__ == '__main__':
  main()