# add book function
def addBook(mysql,bookID,title,genre,fname,lname,year,price,country,stock):
    cur = mysql.connection.cursor()
    try:
        # if publisher country is not present in Publishers table then add record
        cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
        publisherID = list(cur.fetchall())
        if not publisherID:
            cur.execute("INSERT INTO Publishers(country) VALUES (%s)",(country,))
            cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
            publisherID = list(cur.fetchall())

        # if author name is not present in Authors table then add record
        cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
        authorID = list(cur.fetchall())
        if not authorID:
            cur.execute("INSERT INTO Authors(firstName,lastName) VALUES (%s,%s)",(fname,lname,))
            cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
            authorID = list(cur.fetchall())

        # add book in Books table
        cur.execute("INSERT INTO Books(bookID,authorID,publisherID,title,genre,publicationYear,price) VALUES (%s,%s,%s,%s,%s,%s,%s)",(bookID,authorID,publisherID,title,genre,year,price))
        
        # add book stock in Inventory
        cur.execute("INSERT INTO Inventory (bookID,totalStock,soldStock) VALUES(%s,%s,%s)",(bookID,stock,0))

        result = 1 # book added successfully
    
    except:
        result = 0 # book failed to add
    
    mysql.connection.commit()
    cur.close()

    return result

# update book function
# update book function
def updateBook(mysql, bookID, price1, price2,quantity):
    cur = mysql.connection.cursor()
    try:
        # Update price of the book
        cur.execute("UPDATE Books SET price = %s WHERE bookID = %s AND price = %s", (price2, bookID, price1))
        cur.execute("UPDATE inventory SET totalStock =%s where bookID= %s",(quantity,bookID))
        result = 1  # Book updated successfully
    except Exception as e:
        print(f"Error updating book: {e}")
        result = 0  # Book failed to update

    mysql.connection.commit()
    cur.close()
    return result



def deleteBook(mysql, bookID):
    cur = mysql.connection.cursor()
    try:
        # Delete from Inventory first due to foreign key constraints
        cur.execute("DELETE FROM Inventory WHERE bookID = %s", (bookID,))
        cur.execute("DELETE FROM Books WHERE bookID = %s", (bookID,))
        result = 1  # Book deleted successfully
    except:
        result = 0  # Failed to delete the book

    mysql.connection.commit()
    cur.close()

    return result

# book stock function
def inventory(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,b.title,i.totalStock,i.soldStock FROM Books as b,Inventory as i WHERE b.bookID=i.bookID")
    bookData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return bookData

# book details function
def bookDetail(mysql,subject):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,b.title,b.genre,b.price,b.publicationYear,a.firstName,a.lastName,p.country FROM Books as b JOIN Authors as a ON b.authorID = a.authorID JOIN Publishers as p on b.publisherID = p.publisherID WHERE b.bookID = %s",(subject,))
    bookData = list(cur.fetchone())
    mysql.connection.commit()
    cur.close()
    return bookData

# calcuate total cost of books
def totalBookPrice(mysql,bookID,quantity):
    cur = mysql.connection.cursor()
    cur.execute("SELECT bookID,price,title from Books where bookID = %s",(bookID,))
    bookData = list(cur.fetchone())
    mysql.connection.commit()
    cur.close()
    return bookData
