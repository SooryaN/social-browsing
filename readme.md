The information we'll be maintaining:

  1. Sites visited (userid, url, host, time)
  2. Comments (userid, url, comment, time)
  3. Messages (senderid, receiverid, html, time)

Messages are the annotations. You read something and annotate and send it to a friend.

---

The client-server communication is RESTful.

The following three are the API end points:

  - **/visited**
  - **/comments**
  - **/messages**

End point | Method | Params | Returns | Comments
----------|--------|--------|---------|---------
/visited/ | GET    | *None* | History | Lol     

