#social-browsing  

lulz
The information we'll be maintaining:

  1. Sites visited (userid, url, host, time, timespent)
  2. Comments (userid, url, comment, time)
  3. Messages (senderid, receiverid, html, seen, time)

Messages are the annotations. You read something and annotate and send it to a friend.

---

The client-server communication is RESTful.

The following three are the API end points:

  - **/visited**
  - **/comments**
  - **/messages**

**Notes**:
---
There are 2 types of parameters in the following content. 
"URL Param" and "Data Param". URL Params are passed via 
the url, and Data Params are passed in the body of the 
HTTP request (like how it's done in POST). URL Params 
are of two types again - embed the parameter in the 
path of the url (like `/messages/:messageid`); or, embed 
the parameter in the query string (like `/messages/?limit=10`).
Unless mentioned in the `url` of the API-call, any URL Param 
is a query-string paramater.

**History of currently logged-in user**
----
**URL**   | **Method**
----------|------------
/visited  | **GET**    
  
**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
page      | Url Param  | string       | False        | 1          

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** UserHistory object
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`

* **Notes:**<br>
  Nothing much

----

**Visit a page**
----
**URL**   | **Method**
----------|------------
/visited  | **POST**

**Param**  | **Type**   | **DataType** | **Required** | **Default**
-----------|------------|--------------|--------------|------------
url        | Data Param | string       | True         | *N/A*      

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** PageData object
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`
    
    OR
    
    > **Code:** 400 BAD REQUEST <br />
    > **Content:** `{ error : "Bad URL" }`

* **Notes:**<br>
  The second error occurs when the URL is malformed.

---

**Delete a page-view from history**
----
**URL**            | **Method**
-------------------|------------
/visited:/visitid  | **DELETE**

**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
visitid   | URL Param  | string       | True         | *N/A*      

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** Empty
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`
    
    OR
    
    > **Code:** 404 NOT FOUND <br />
    > **Content:** `{ error : "No entry in history has the given visitid" }`

* **Notes:**<br>
  Nothing much

---


**Comment on a page**
----
**URL**   | **Method**
----------|------------
/comments | **POST**

**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
url       | Data Param | string       | True         | *N/A*      
comment   | Data Param | string       | True         | *N/A*      

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** `{ commentid: "<commentid>" }`
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`
    
    OR
    
    > **Code:** 400 BAD REQUEST <br />
    > **Content:** `{ error : "Bad URL" }`

* **Notes:**<br>
  The server must check if the page on which the client is commenting has been
  visited by the client (Checking this is not a priority, but still, important
  from good-code POV).

  The second error occurs in either of the two cases: <br>
    - The url is malformed. <br>
    - The url hasn't been visited by the client. <br>

---

**Delete a comment**
----
**URL**               | **Method**
----------------------|------------
/comments:/:commentid | **DELETE**

**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
commentid | URL Param  | string       | True         | *N/A*      

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** Empty
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`
    
    OR
    
    > **Code:** 404 NOT FOUND <br />
    > **Content:** `{ error : "comment with given commentid doesn't exist" }`

* **Notes:**<br>
  The 2nd error should be thrown in either of the two cases: <br>
    - The user supplies a non-existing comment id.<br>
    - The user supplies a comment id of a comment that he didn't make.<br>

---

**Send a message**
----
**URL**               | **Method**
----------------------|------------
/messages/:receiverid | **POST**

**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
receiverid| URL Param  | string       | True         | *N/A*      
message   | Data Param | string       | True         | ""
html      | Data Param | string       | True         | ""      
public    | Data Param | bool         | True         | *N/A*

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** `{ messageid: "<messageid>" }`
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`
    
    OR
    
    > **Code:** 400 BAD REQUEST <br />
    > **Content:** `{ error : "Bad receiverid" }`

    OR
    
    > **Code:** 400 BAD REQUEST <br />
    > **Content:** `{ error : "message or html is required" }`

    OR
    
    > **Code:** 400 BAD REQUEST <br />
    > **Content:** `{ error : "public is required" }`

* **Notes:**<br>
  The two parameters `message` and `html` both have been marked as
  "required", however, only one of them is required. The other may
  be empty. This allows users to send normal text messages to 
  each other.

  The `public` paramater, if true, makes the annotations public. So, 
  if someone comes to this url later, and is a friend of the guy
  who makes the doodle, will get an option to see the annotations.

  We will need to make this secure later, because the html we're 
  storing is directly dumped onto the receiver's browser, 
  including the &lt;script&rt; tags. This might have security issues,
  though I haven'thought through it yet.

---

**View messages**
----
**URL**   | **Method**
----------|------------
/messages | **GET**

**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
since     | URL Param  | timestamp    | False        | &lt;current-time&gt;
limit     | URL Param  | integer      | False        | 10

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** an array of PartialMessage objects
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`

* **Notes:**<br>
  Max value of `limit` = 20 (no particular reason. But we need to 
  limit the limit. Sic.)

  The paramaters will be given in the query string.

---

**Open a message**
----
**URL**              | **Method**
---------------------|------------
/messages/:messageid | **POST**

**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
messageid | URL Param  | string       | True         | *N/A*

* **Success Response:**

    > **Code:** 200 <br>
    > **Content:** CompleteMessage
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`

    OR

    > **Code:** 404 NOT FOUND <br />
    > **Content:** `{ error : "message with given messageid doesn't exist" }`

* **Notes:**<br>
  This is a POST request, because it modifies the state - the message 
  opened is marked as seen.

---

DataTypes
---

UserHistory:
```
{
    "userid": <string>,
    "page": <integer>,
    "history": [
        {
            "visitid": <string>
            "url": <string>,
            "host": <string>,
            "time": TimeStamp
        },
        .
        .
        .
    ]
}
```

PageData:
```
{
    "url": <string>,
    "visits": [
        {
            "visitid": <string>
            "userid": <string>,
            "time": TimeStamp
        }
        .
        .
        .
    ],
    "hostVisits": [
        {
            "visitid": <string>,
            "userid": <string>,
            "time": TimeStamp,
            "url": <string>
        }
        .
        .
        .
    ],
    "comments": [
        {
            "commentid": <string>,
            "userid": <string>,
            "time": TimeStamp,
            "comment": <string>
        }
    ]
}
```

PartialMessage:
```
{
    "messageid": <string>,
    "senderid": <string>,
    "receiverid": <string>
    "seen": bool,
    "text": <string>
    "time": TimeStamp
}
```

CompleteMessage:
```
{
    "messageid": <string>,
    "senderid": <string>,
    "receiverid": <string>
    "seen": bool,
    "text": <string>
    "html": <string>
    "time": TimeStamp,
}
```