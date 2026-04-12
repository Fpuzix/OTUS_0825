from typing import Optional


def create_customer(connection, customer_data: dict) -> int:
    query = """
        INSERT INTO oc_customer (
            customer_group_id,
            store_id,
            language_id,
            firstname,
            lastname,
            email,
            telephone,
            password,
            custom_field,
            newsletter,
            ip,
            status,
            safe,
            token,
            code,
            date_added
        )
        VALUES (
            %(customer_group_id)s,
            %(store_id)s,
            %(language_id)s,
            %(firstname)s,
            %(lastname)s,
            %(email)s,
            %(telephone)s,
            %(password)s,
            %(custom_field)s,
            %(newsletter)s,
            %(ip)s,
            %(status)s,
            %(safe)s,
            %(token)s,
            %(code)s,
            NOW()
        )
    """
    with connection.cursor() as cursor:
        cursor.execute(query, customer_data)
        connection.commit()
        return cursor.lastrowid


def get_customer_by_id(connection, customer_id: int) -> Optional[dict]:
    query = "SELECT * FROM oc_customer WHERE customer_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (customer_id,))
        return cursor.fetchone()


def update_customer(connection, customer_id: int, new_data: dict) -> int:
    query = """
        UPDATE oc_customer
        SET firstname = %(firstname)s,
            lastname = %(lastname)s,
            email = %(email)s,
            telephone = %(telephone)s
        WHERE customer_id = %(customer_id)s
    """
    params = {
        "customer_id": customer_id,
        "firstname": new_data["firstname"],
        "lastname": new_data["lastname"],
        "email": new_data["email"],
        "telephone": new_data["telephone"],
    }
    with connection.cursor() as cursor:
        affected = cursor.execute(query, params)
        connection.commit()
        return affected


def delete_customer(connection, customer_id: int) -> int:
    query = "DELETE FROM oc_customer WHERE customer_id = %s"
    with connection.cursor() as cursor:
        affected = cursor.execute(query, (customer_id,))
        connection.commit()
        return affected
