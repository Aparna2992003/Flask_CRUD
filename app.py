import math
from flask import Flask, request, jsonify,render_template,json
import psycopg2
from psycopg2 import pool



app = Flask(__name__)
@app.route('/')
def home():
    return "Details of an employee"
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "hello"


@app.route('/employee', methods=['POST'])
def create_employee():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}),400
        file = request.files['file']
        record=json.load(file)
        connection = psycopg2.connect(
             host = DB_HOST, dbname = DB_NAME, user = DB_USER, password = DB_PASS)
        cursor = connection.cursor()
        for user in record:
            cursor.execute("""INSERT INTO users (id, first_name, last_name, company_name, city, state, zip, email, web,age) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                returning id, first_name, last_name, company_name, city, state, zip, email, web,age""",(user['id'],user['first_name'],user['last_name'],user['company_name'],user['city'],user['state'],user['zip'],user['email'], user['web'],user['age'],))
            
        connection.commit()
        print("Record inserted successfully")
        cursor.close()
        return jsonify({'message':'Employee created successfully'}),201
    except Exception as e:
           return jsonify({'error':str(e)}),500
    

@app.route('/get_employee/<id>', methods=['GET'])
def get_employee(id):
    try:
       
        connection = psycopg2.connect(
             host = DB_HOST, dbname = DB_NAME, user = DB_USER, password = DB_PASS)
        cursor = connection.cursor()
        
        cursor.execute("""SELECT * FROM users WHERE id = %s""",(id, ))
        employ = cursor.fetchone()
 
        print({'message':'Employee with the mentioned id is returned successfully'})
        
        employee_list = []
        if employ:
            return jsonify({"id": employ[0], "first_name": employ[1], "last_name": employ[2], "company_name": employ[3], "city": employ[4], "state": employ[5], "zip": employ[6], "email": employ[7], "web": employ[8], "age": employ[9]})
           
        else:
            return jsonify({'message':'Employee with the mentioned id is not found'}),404

            
        connection.commit()
       
        cursor.close()
        
    except Exception as e:
           return jsonify({'error':str(e)}),500
    


    
@app.route('/put_employee/<id>', methods=['PUT'])
def put_employee(id):
    try:
        
        data=request.json
        connection = psycopg2.connect(
             host = DB_HOST, dbname = DB_NAME, user = DB_USER, password = DB_PASS)
        cursor = connection.cursor()
        
        cursor.execute("""UPDATE users SET first_name = %s, last_name = %s, company_name = %s, city = %s, state = %s, zip = %s, email = %s, web = %s, age = %s 
                       WHERE id = %s """ 
                       ,(data['first_name'],
                         data['last_name'],
                         data['company_name'],
                         data['city'],
                         data['state'],
                         data['zip'],
                         data['email'],
                         data['web'],
                         data['age'],id,))
        connection.commit()
        cursor.close()
        
        return jsonify({'message':'User updated successfully'})

            
      
        
    except Exception as e:
           return jsonify({'error':str(e)}),500
    

@app.route('/delete_employee/<id>', methods=['DELETE'])
def delete_employee(id):
    try:
        
        connection = psycopg2.connect(
             host = DB_HOST, dbname = DB_NAME, user = DB_USER, password = DB_PASS)
        cursor = connection.cursor()
        
        cursor.execute("""DELETE FROM users WHERE id = %s""",(id,))
        connection.commit()
        cursor.close()
        
        return jsonify({'message':'User deleted successfully'})
        
    except Exception as e:
           return jsonify({'error':str(e)}),500
    
    
@app.route('/patch_employee/<id>', methods=['PATCH'])
def patch_employee(id):
    try:
        data = request.get_json()
        connection = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = connection.cursor()
        
      
        update_key=[]
        update_value=[]
        for key, value in data.items():
            update_key.append(f"{key}= %s")
            update_value.append(value)
        update_value.append(id)
        
        update_query=f"UPDATE users SET {','.join(update_key)} WHERE id = %s"
        cursor.execute(update_query, tuple(update_value))
        
        connection.commit()
        cursor.close()
        
        return jsonify({'message': 'User updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
          

@app.route('/get_employee_summary', methods=['GET'])
def get_employee_summary():
    try:
       
        connection = psycopg2.connect(
             host = DB_HOST, dbname = DB_NAME, user = DB_USER, password = DB_PASS)
        cursor = connection.cursor()
        
        cursor.execute("""SELECT city , COUNT(*) FROM users GROUP BY city""")
        city_count = cursor.fetchall()

        cursor.execute("""SELECT AVG(age) FROM users """)
        age= cursor.fetchone()[0]
        
 
       
        
            
        connection.commit()
       
        cursor.close()

        statistics = {
             "count_by_city": {city: count for city, count in city_count},
             "average_age": round(age,2)
        }
        return jsonify(statistics),200
        
    except Exception as e:
           return jsonify({'error':str(e)}),500
    



@app.route('/api/users', methods=['GET'])
def list_users():
    try:
        connection = psycopg2.connect(
             host = DB_HOST, dbname = DB_NAME, user = DB_USER, password = DB_PASS)
        cursor = connection.cursor()

       
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 5, type=int)
        search = request.args.get('search', None, type=str)
        sort = request.args.get('sort', 'id', type=str)

       
        offset = (page - 1) * limit

        
        query = "SELECT id, first_name, last_name, age FROM users"
        conditions = []
        params = []

        
        if search:
            conditions.append("(LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s)")
            params.extend([f"%{search.lower()}%", f"%{search.lower()}%"])

       
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        
        order = "ASC"
        if sort.startswith("-"):
            sort = sort[1:]  
            order = "DESC"

        query += f" ORDER BY {sort} {order} LIMIT %s OFFSET %s"
        params.extend([limit, offset])

      
        cursor.execute(query, params)
        users = cursor.fetchall()

       
        user_list = [
            {"id": row[0], "first_name": row[1], "last_name": row[2], "age": row[3]}
            for row in users
        ]

       
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        total_pages = math.ceil(total_users / limit)

        cursor.close()
        connection.close()

        return jsonify({
            "page": page,
            "total_pages": total_pages,
            "total_users": total_users,
            "users": user_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
