This is my own extension of and exercise from https://app.codecrafters.io/courses/http-server/overview
This program handles sending and receiving data via http.
It can handle concurrent requests by using threading

To run this program, first execute
./your_server.sh
If posting a file, please specify --directory with an absolute path

Some example requests:
curl -v -X POST http://localhost:4221/files/b.txt -H "User-Agent: apple/banana-apple" --data "zivile"
