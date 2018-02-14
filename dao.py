'''
c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
     c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})
        c.execute("DELETE from USERS WHERE id = :id",
                  {'id': _id})
'''