from pkgutil import get_data
import mysql.connector


class Connector:
    def __init__(self, database : str) -> None:
        """
        This function accepts one parameter, database :str
        Initiates self.db and self.mycursor
        return None
        """
        self.db = mysql.connector.connect(host="localhost", user="root", passwd="root", database=database)
        self.mycursor = self.db.cursor()

    def execution(self, query : str):
        """
        This function accepts one parameter, query :str.
        Uses mycursor.execute and db.commit if necessary
        return self.mycursor 
        """
        self.mycursor.execute(query)
        try:
            self.db.commit()
        except:
            pass
        return self.mycursor

    def get_data(self, table : str, columns="*", column="", values="") -> list:
        """
        This function accepts one parameter, table :str.
        Uses sql query SELECT and get the desiered data from the columns, columns in values
        return a list of the selected data
        """
        acc_list = []
        if column != "" and values != "":
            self.mycursor.execute(f"SELECT {columns} FROM {table} WHERE {column} IN ('{values}')")
        else:
            self.mycursor.execute(f"SELECT {columns} FROM {table}")
        for x in self.mycursor:
            acc_list.append(x)
        return acc_list

    def add_data(self, table : str, columns : list, values : list) -> None:
        """
        This function accepts 3 parameter, table :str - columns  :list - values :list.
        Uses sql query INSERT and adds each values in the right columns of the table
        return None since sql query INSERT returns None
        """
        str_columns = ""
        for column in columns:
            str_columns += column + ", "
        str_columns = str_columns[:-2] # remove the ", " from the en
        
        query = f"INSERT INTO {table} ({str_columns}) VALUES ("
        for i in range(len(values)):
            query += f"'{values[i]}',"
        query = query[:-1] + ")"
        return self.execution(query)
    
    def delete_data(self, table:str, column="", value=""):
        """
        This function accepts 1 parameter, table :str and 2 optional parameters, column :str - value :str.
        Uses sql query DELETE FROM 
        return str error if parameters not respected, None if successful
        """
        Q1 = f"DELETE FROM {table}"
        if column != "" and value != "":
            Q1 = Q1 + f" WHERE {column} IN ({value})"
        elif column != "" and value=="":
            return "Error, column value missing"
        elif column == "" and value != "":
            return "Error, column missing"
        return self.execution(Q1)

    def sort_data(self, table : str, bycolumn : int, column="", values="") -> list:
        """
        This function accepts 2 parameters, 2 optional parameters 
        sorts the data and ranks them
        returns a list 
        """
        data_list = self.get_data(table, column=column, values=values)
        data_list.sort(key = lambda a: a[bycolumn])
        try:
            for i in range(len(data_list)):
                self.execution(f"UPDATE {table} SET rank = {i+1} WHERE Id = {data_list[i][0]}")
        except:
            pass
        return data_list


connector = Connector("faceposition")
def get_score_history(user : str):
    user_id = connector.get_data("accounts", "Id", "UserName", user)[0][0]
    data_list = connector.get_data("scores", "Game, Score", "UserId", str(user_id))
    return data_list


def add_score(user : str, game : str, score : float) -> None:
    user_id = connector.get_data("accounts", "Id", "UserName", user)[0][0]
    connector.add_data("scores", ("UserId", "Game", "Score"), (user_id, game, score))
    connector.sort_data("scores", 3)
    return 
