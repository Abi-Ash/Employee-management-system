from flask import Flask, render_template, request, redirect
from db import get_connection


app = Flask(__name__)

@app.route("/setup")
def setup_database():

    conn = get_connection()

    cursor = conn.cursor()

    with open("queries.sql", "r") as file:

        sql_queries = file.read()

    queries = sql_queries.split(";")

    for query in queries:

        if query.strip():

            cursor.execute(query)

    conn.commit()

    return "Database Setup Completed"


# home route
@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # stored procedure
    cursor.callproc("GetAllEmployees")
    
    employees = []
    
    for result in cursor.stored_results():
        employees = result.fetchall()
        
        conn.close()
        
        return render_template("index.html", employees=employees)
    

# add employee route 
@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        salary = request.form["salary"]
        
        
        # Validation
        if len(name) < 3:
            return "Name must contain minimum 3 characters"

        if int(salary) < 1000:
            return "Salary must be greater than 1000"
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # CHECK DUPLICATE EMAIL

        cursor.execute(
            "SELECT * FROM employees WHERE email=%s",
            (email,)
        )

        existing_employee = cursor.fetchone()

        if existing_employee:

            error = "Email already exists!"

            conn.close()

            return render_template(
                "add.html",
                error=error
            )
        
        # insert new emp
        
        query = """ 
        INSERT INTO employees(name, email, department, salary) VALUES(%s, %s, %s, %s)
        """
       
        values = (name, email, department, salary)
        
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
        
        return redirect("/")
    
    return render_template("add.html")


#update route 
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        salary = request.form["salary"]
        
        query = """
        UPDATE employees SET name=%s, email=%s, department=%s, salary=%s WHERE id=%s
        """
        
        values = (name, email, department, salary, id)
        
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
        
        return redirect("/")
    
    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    
    conn.close()
    
    return render_template("edit.html", employee=employee)


#delete route
@app.route("/delete/<int:id>")
def delete_employee(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

# search
@app.route("/search")
def search_employee():

    email = request.args.get("email")

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT * FROM employees
    WHERE email=%s
    """

    cursor.execute(query, (email,))

    employees = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        employees=employees
    )



if __name__ == "__main__":
    app.run(debug=True)