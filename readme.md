#social-browsing  

lulz
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

**Param** | **Type**   | **DataType** | **Required** | **Default**
----------|------------|--------------|--------------|------------
url       | Data Param | string       | True         | *N/A*      

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
    > **Content:** Empty
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`
    
    OR
    
    > **Code:** 400 BAD REQUEST <br />
    > **Content:** `{ error : "Bad URL" }`

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
    > **Content:** Empty
 
* **Error Response:**

    > **Code:** 401 UNAUTHORIZED <br />
    > **Content:** `{ error : "Log in" }`
    
    OR
    
    > **Code:** 400 BAD REQUEST <br />
    > **Content:** `{ error : "Bad URL" }`

* **Notes:**<br>
  Nothing much

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
            "userid": <string>,
            "time": TimeStamp
        }
        .
        .
        .
    ],
    "hostVisits": [
        {
            "userid": <string>,
            "time": TimeStamp
        }
        .
        .
        .
    ]
}
```
