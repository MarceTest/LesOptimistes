import sqlparse
import _more as more

class Parser:

    def parse(self, query, classe):
        parsed = sqlparse.parse(query)[0]
        cmd = None
        select_columns = []
        table_names = []  # List to store multiple table names
        where_clause = None
        is_select_clause = False  # Flag to track if we're in the SELECT clause
        is_from_clause = False  # Flag to track if we're in the FROM clause
        
        for token in parsed.tokens:
            # Check if it's a DML command (e.g., SELECT)
            if token.ttype and "DML" in str(token.ttype):
                cmd = token.value
                if cmd.upper() == "SELECT":
                    is_select_clause = True  # We're in the SELECT clause

            # Extract column names in the SELECT clause
            if is_select_clause:
                if isinstance(token, sqlparse.sql.IdentifierList):
                    for identifier in token.get_identifiers():
                        select_columns.append(identifier.value)
                    is_select_clause = False  # Reset after processing SELECT columns
                elif isinstance(token, sqlparse.sql.Identifier):
                    select_columns.append(token.value)
                    is_select_clause = False  # Reset after processing SELECT columns
                elif token.value.strip() == "*":  # Handle wildcard
                    select_columns.append("*")
                    is_select_clause = False
            
            # Detect FROM clause
            if token.match(sqlparse.tokens.Keyword, 'FROM'):
                is_from_clause = True  # Next token(s) should be table names
                continue
            
            # Extract multiple table names after FROM
            if is_from_clause:
                if isinstance(token, sqlparse.sql.IdentifierList):
                    for identifier in token.get_identifiers():
                        table_names.append(identifier.get_real_name())
                    is_from_clause = False  # Reset after processing tables
                elif isinstance(token, sqlparse.sql.Identifier):
                    table_names.append(token.get_real_name())
                    is_from_clause = False  # Reset after processing table name
            
            # Detect WHERE clause
            if isinstance(token, sqlparse.sql.Where):
                where_clause = token.value
            
        formatted_query = more.Query(cmd, select_columns, table_names, classe, where_clause)
                
        return formatted_query


if __name__ == "__main__" :
    print("test parser")